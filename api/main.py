import os
import sys
import torch
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
import safetensors
import diffusers
try:
    import psutil
except ImportError:
    print("WARNING: psutil not available, memory monitoring disabled")
    psutil = None

# DEBUG LOGGER
with open("debug_env.txt", "w") as f:
    f.write(f"Python Executable: {sys.executable}\n")
    f.write(f"Python Version: {sys.version}\n")
    f.write(f"Diffusers Version: {diffusers.__version__}\n")
    f.write(f"Diffusers Path: {diffusers.__file__}\n")
    from diffusers import StableVideoDiffusionPipeline, DiffusionPipeline
    f.write(f"SVD has from_single_file: {hasattr(StableVideoDiffusionPipeline, 'from_single_file')}\n")
    f.write(f"DiffusionPipeline has from_single_file: {hasattr(DiffusionPipeline, 'from_single_file')}\n")

from diffusers import (
    StableDiffusionPipeline, 
    StableDiffusionXLPipeline, 
    StableVideoDiffusionPipeline,
    FluxPipeline,
    DPMSolverMultistepScheduler,
    DiffusionPipeline
)

from PIL import Image
from fastapi.middleware.cors import CORSMiddleware
import base64
from io import BytesIO
import traceback

class GenerateRequest(BaseModel):
    mode: str = "txt2img"
    prompt: Optional[str] = ""
    negative_prompt: Optional[str] = ""
    model_name: str
    steps: int = 20
    cfg: float = 7.0
    width: int = 512
    height: int = 512
    init_image: Optional[str] = None
    seed: Optional[int] = -1
    strength: Optional[float] = 0.75

import uuid

app = FastAPI(title="Diffusion Lite API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

MODEL_PATH = "../models/checkpoints"
OUTPUT_PATH = "../web/public/outputs"
os.makedirs(OUTPUT_PATH, exist_ok=True)

# Global variable to store the active pipeline to avoid reloading
current_pipe = None
current_model_name = ""
current_mode = ""

# Memory management for CPU with limited RAM
import gc
import psutil

def get_memory_usage():
    """Get current memory usage in MB"""
    process = psutil.Process()
    return process.memory_info().rss / (1024 * 1024)

def check_memory_available(required_mb=1024):
    """Check if we have enough memory available"""
    if psutil is None:
        return True  # Assume OK if psutil not available

    memory = psutil.virtual_memory()
    available_mb = memory.available / (1024 * 1024)
    total_mb = memory.total / (1024 * 1024)

    print(f"Memory: {available_mb:.0f}MB available / {total_mb:.0f}MB total")
    return available_mb > required_mb

def force_memory_cleanup():
    """Force garbage collection and memory cleanup"""
    if current_pipe is not None:
        try:
            # Move to CPU and clear CUDA cache if available
            current_pipe.to("cpu")
            if hasattr(current_pipe, "vae"):
                current_pipe.vae.to("cpu")
            if hasattr(current_pipe, "unet"):
                current_pipe.unet.to("cpu")
        except:
            pass

    # Force garbage collection
    gc.collect()

    # Clear any cached tensors
    if hasattr(torch, 'cuda') and torch.cuda.is_available():
        torch.cuda.empty_cache()
    elif hasattr(torch, 'mps') and torch.backends.mps.is_available():
        torch.mps.empty_cache()

    print(f"Memory cleanup completed. Current usage: {get_memory_usage():.1f} MB")

@app.get("/")
async def root():
    return {"status": "online", "message": "Diffusion Lite API is running"}

def generate_fallback_video(init_img, req, generator):
    """Generate a simple video by creating multiple img2img frames with variations"""
    print("Generating fallback video using img2img frames...")

    # Check memory before loading fallback model
    print(f"Memory before fallback model: {get_memory_usage():.1f} MB")
    if not check_memory_available(3000):  # Need at least 3GB free for safety
        print("ERROR: Not enough memory for video generation (need 3GB free)")
        print("Try closing other applications or use image generation instead")
        return []

    # Load a lightweight model for img2img (we'll use SD 1.5 since it's lighter)
    fallback_model = load_model("v1-5-pruned-emaonly.safetensors", "img2img")
    if fallback_model is None:
        print("ERROR: Could not load fallback model")
        return []
    if fallback_model is None:
        raise HTTPException(status_code=500, detail="No suitable model available for video generation")

    frames = []
    # Ultra-reduced frames for memory efficiency
    num_frames = 4  # Only 4 frames for very low memory usage

    print(f"Memory after model load: {get_memory_usage():.1f} MB")

    # Create variations by slightly changing the seed and prompt
    base_seed = 42  # Use fixed seed for consistency

    for i in range(num_frames):
        print(f"Generating frame {i+1}/{num_frames}... (Memory: {get_memory_usage():.1f} MB)")

        # Check memory before each frame
        if not check_memory_available(800):  # Need at least 800MB free per frame
            print("WARNING: Low memory during frame generation, stopping to prevent crash")
            break

        # Vary the seed slightly for each frame
        frame_seed = base_seed + i * 100
        frame_generator = torch.Generator(device="cpu").manual_seed(frame_seed)

        # Simple motion variation (reduced complexity)
        motion_words = ["moving", "dynamic", "flowing", "animated"]
        frame_prompt = f"{req.prompt}, {motion_words[i % len(motion_words)]}"

        # Generate frame with minimal settings for memory
        strength = 0.6  # Fixed strength for consistency

        frame = fallback_model(
            prompt=frame_prompt,
            negative_prompt=req.negative_prompt or "",
            image=init_img,
            num_inference_steps=6,  # Very low steps for speed/memory
            guidance_scale=min(5.0, req.cfg),  # Reduced guidance for memory
            strength=strength,
            generator=frame_generator,
            width=256,  # Even smaller resolution
            height=256
        ).images[0]

        frames.append(frame)

        # Force cleanup after each frame
        if i < num_frames - 1:  # Don't cleanup on last frame
            gc.collect()

    print(f"Generated {len(frames)} frames. Final memory: {get_memory_usage():.1f} MB")

    print(f"Generated {len(frames)} frames for fallback video")
    return frames

def load_model(model_name: str, mode: str = "txt2img"):
    global current_pipe, current_model_name, current_mode
    
    # We need to reload if model OR mode (task) changed
    # Correct task detection: check for video first
    if "vid" in mode:
        task = "img2vid"
    elif "img2img" in mode:
        task = "img2img"
    else:
        task = "txt2img"

    if current_model_name == model_name and current_pipe is not None and current_mode == mode:
        print(f"Using cached pipeline for {model_name} in {mode} mode")
        return current_pipe

    print(f"Loading model: {model_name} for {task}...")
    checkpoint_path = os.path.join(MODEL_PATH, model_name)
    
    if not os.path.exists(checkpoint_path):
        print(f"Warning: {checkpoint_path} not found. Using placeholder logic.")
        return None

    device = "cpu"
    from diffusers import (
        StableDiffusionImg2ImgPipeline,
        StableDiffusionXLImg2ImgPipeline,
        FluxImg2ImgPipeline
    )

    # MANUAL MIXIN PATCH
    try:
        from diffusers.loaders import FromSingleFileMixin
    except ImportError:
        # Fallback for older/different structures
        try:
             from diffusers.loaders.single_file import FromSingleFileMixin
        except ImportError:
             FromSingleFileMixin = object # Mock if completely missing (will fail later but avoids import error)

    if "flux" in model_name.lower():
        cls = FluxImg2ImgPipeline if task == "img2img" else FluxPipeline
        pipe = cls.from_single_file(checkpoint_path, torch_dtype=torch.float32)
    elif "xl" in model_name.lower() or "pony" in model_name.lower() or "hentaimix" in model_name.lower():
        cls = StableDiffusionXLImg2ImgPipeline if task == "img2img" else StableDiffusionXLPipeline
        pipe = cls.from_single_file(checkpoint_path, torch_dtype=torch.float32)
    elif "svd" in model_name.lower():
        # Force Mixin if method is missing
        if not hasattr(StableVideoDiffusionPipeline, 'from_single_file'):
            print("PATCH: Applying FromSingleFileMixin manually to SVD...")
            class CustomSVD(StableVideoDiffusionPipeline, FromSingleFileMixin):
                pass
            LoaderClass = CustomSVD
        else:
            LoaderClass = StableVideoDiffusionPipeline
            
        # Determine correct config repo or LOCAL PATH to avoid auto-guessing SD2.1 (which causes 401)
        # Verify if manual config download exists
        local_config_path = "models/svd_xt_config"
        if os.path.exists(local_config_path) and os.path.exists(os.path.join(local_config_path, "model_index.json")):
            config_repo = local_config_path
            print(f"Loading SVD with LOCAL CONFIG from: {config_repo}")
        elif "xt" in model_name.lower():
            config_repo = "stabilityai/stable-video-diffusion-img2vid-xt"
        else:
            config_repo = "stabilityai/stable-video-diffusion-img2vid"
            
        if "http" in config_repo or "stability" in config_repo:
             print(f"Loading SVD with REMOTE CONFIG from: {config_repo}")
        

        try:
            # Check if we have the required SVD components
            config_dir_abs = os.path.abspath("models/svd_xt_config")

            def check_component_available(component_path, possible_names):
                """Check if any of the possible model files exist"""
                for name in possible_names:
                    if os.path.exists(os.path.join(component_path, name)):
                        return True
                return False

            # Check for UNet and VAE components (both .bin and .safetensors formats)
            unet_path = os.path.join(config_dir_abs, "unet")
            vae_path = os.path.join(config_dir_abs, "vae")

            unet_available = check_component_available(unet_path, ["diffusion_pytorch_model.bin", "diffusion_pytorch_model.safetensors"])
            vae_available = check_component_available(vae_path, ["diffusion_pytorch_model.bin", "diffusion_pytorch_model.safetensors"])

            if unet_available and vae_available:
                print("Found SVD components! Attempting to load complete SVD pipeline...")

                # Try loading with components
                try:
                    # Load image encoder explicitly since it's needed
                    img_enc_path = os.path.join(config_dir_abs, "image_encoder")
                    if os.path.exists(img_enc_path):
                        from transformers import CLIPVisionModelWithProjection
                        image_encoder = CLIPVisionModelWithProjection.from_pretrained(
                            img_enc_path,
                            torch_dtype=torch.float32,
                            local_files_only=True
                        )
                        print("Image encoder loaded successfully")
                    else:
                        print("Image encoder not found, skipping SVD loading")
                        pipe = None

                    if 'image_encoder' in locals():
                        pipe = LoaderClass.from_single_file(
                            checkpoint_path,
                            config=config_dir_abs,
                            torch_dtype=torch.float32,
                            image_encoder=image_encoder,
                            local_files_only=True
                        )
                        print("✅ SVD Pipeline loaded successfully with components!")
                    else:
                        pipe = None

                except Exception as component_error:
                    print(f"Component loading failed: {component_error}")
                    pipe = None
            else:
                print("SVD components not found. Will use fallback video generation.")
                pipe = None

            # If we couldn't load SVD, return None for fallback
            if pipe is None:
                print("SVD loading failed. Will use fallback video generation.")
                return None

        except Exception as e:
            print(f"SVD loading failed completely: {e}")
            print("SVD is not available. Will use fallback video generation.")
            # Return None to indicate SVD is not available
            # Don't cache None values
            return None
    else:
        cls = StableDiffusionImg2ImgPipeline if task == "img2img" else StableDiffusionPipeline
        pipe = cls.from_single_file(checkpoint_path, torch_dtype=torch.float32, local_files_only=True)
        
        # REGRESSION FIX: Diffusers 0.36.0 sometimes loads SD1.5 UNets with 'addition_embed_type="text_time"'
        # This causes the UNet to expect 'added_cond_kwargs' (SDXL feature) which this pipeline doesn't provide.
        # We manually strip this config to prevent the crash.
        if hasattr(pipe, "unet") and getattr(pipe.unet.config, "addition_embed_type", None) is not None:
             print(f"WARNING: Mismatched UNet config detected ({pipe.unet.config.addition_embed_type}). Forcing to None for stability.")
             pipe.unet.config.addition_embed_type = None

    if pipe is not None:  # Only set attributes if pipe is loaded
        pipe._task = task # Custom attribute to track
        pipe.to(device)

        # CPU optimizations for Ryzen 5 5600G
        if hasattr(pipe, "enable_attention_slicing"):
            pipe.enable_attention_slicing("max")  # Maximize CPU efficiency
        if hasattr(pipe, "enable_vae_slicing"):
            pipe.enable_vae_slicing()

        # Additional CPU optimizations
        if hasattr(pipe, "enable_vae_tiling"):
            pipe.enable_vae_tiling()  # Reduce VAE memory usage

        # For CPU, use float32 but with memory optimizations
        if device == "cpu":
            # Enable model CPU offload if available (moves parts of model to CPU dynamically)
            if hasattr(pipe, "enable_model_cpu_offload"):
                try:
                    pipe.enable_model_cpu_offload()
                    print("Enabled model CPU offload for memory efficiency")
                except Exception as e:
                    print(f"CPU offload not available: {e}")

            # Enable sequential CPU offload as fallback
            elif hasattr(pipe, "enable_sequential_cpu_offload"):
                try:
                    pipe.enable_sequential_cpu_offload()
                    print("Enabled sequential CPU offload")
                except Exception as e:
                    print(f"Sequential CPU offload failed: {e}")

        # Only update cache if we successfully loaded a pipeline
        current_pipe = pipe
        current_model_name = model_name
        current_mode = mode

    return pipe

@app.post("/generate")
@app.post("/generate")
async def generate(req: GenerateRequest):
    try:
        pipe = load_model(req.model_name, req.mode)
        
        # Check for placeholder mode or fallback video generation
        if pipe is None:
            if "vid" in req.mode:
                # Try fallback video generation
                try:
                    print("Attempting fallback video generation...")
                    init_img = None
                    if req.init_image:
                        header, encoded = req.init_image.split(",", 1)
                        init_img = Image.open(BytesIO(base64.b64decode(encoded))).convert("RGB")
                        # Resize for CPU efficiency
                        init_img = init_img.resize((384, 384), resample=Image.LANCZOS)

                    fallback_frames = generate_fallback_video(init_img, req, torch.Generator(device="cpu").manual_seed(42))

                    if not fallback_frames:
                        print("No frames generated, using placeholder")
                        return {"status": "success", "url": "outputs/placeholder.png", "type": "image"}

                    filename = f"{uuid.uuid4()}.mp4"
                    from diffusers.utils import export_to_video

                    # Resize frames to very small size for video export (memory efficient)
                    print(f"Resizing {len(fallback_frames)} frames for video export...")
                    resized_frames = []
                    for frame in fallback_frames:
                        resized_frame = frame.resize((160, 160), Image.LANCZOS)
                        resized_frames.append(resized_frame)

                    print(f"Exporting video with {len(resized_frames)} frames...")
                    export_to_video(resized_frames, os.path.join(OUTPUT_PATH, filename), fps=2)  # Very slow FPS
                    return {"status": "success", "url": f"outputs/{filename}", "type": "video", "seed": 42}
                except Exception as fallback_error:
                    print(f"Fallback video generation failed: {fallback_error}")
                    import traceback
                    traceback.print_exc()
                    return {"status": "success", "url": "outputs/placeholder.png", "type": "image"}
            else:
                return {"status": "success", "url": "outputs/placeholder.png", "type": "image"}

        # Handle image inputs for I2I or Img2Vid
        init_img = None
        if req.init_image:
            header, encoded = req.init_image.split(",", 1)
            init_img = Image.open(BytesIO(base64.b64decode(encoded))).convert("RGB")
            
            # RESIZE LOGIC
            # SVD needs specific dimensions (usually 1024x576), so we force it for video
            if "vid" in req.mode:
                # Force 1024x576 for SVD stability
                init_img = init_img.resize((1024, 576), resample=Image.LANCZOS)
            else:
                # For Image models, just cap max size to prevent OOM
                max_dim = 768
                w, h = init_img.size
                if w > max_dim or h > max_dim:
                    ratio = min(max_dim / w, max_dim / h)
                    w = int(w * ratio)
                    h = int(h * ratio)
                
                # Ensure multiple of 8
                w, h = map(lambda x: x - x % 8, (w, h))
                init_img = init_img.resize((w, h), resample=Image.LANCZOS)

        filename = f"{uuid.uuid4()}"
        gen_type = "image"
        
        seed_used = req.seed if (req.seed is not None and req.seed != -1) else int(torch.randint(0, 2**32 - 1, (1,)).item())
        generator = torch.Generator(device="cpu").manual_seed(seed_used)

        with torch.no_grad():
            if req.mode == "img2img":
                result = pipe(
                    prompt=req.prompt,
                    negative_prompt=req.negative_prompt,
                    image=init_img,
                    num_inference_steps=req.steps,
                    guidance_scale=req.cfg,
                    strength=req.strength,
                    generator=generator
                ).images[0]
                filename += ".png"
                result.save(os.path.join(OUTPUT_PATH, filename))
                
            elif "vid" in req.mode:
                gen_type = "video"

                if pipe is None:
                    # Fallback: Generate video by creating multiple frames with img2img
                    print("Using fallback video generation (img2img frames)...")
                    frames = generate_fallback_video(init_img, req, generator)
                    filename += ".mp4"
                    from diffusers.utils import export_to_video
                    export_to_video(frames, os.path.join(OUTPUT_PATH, filename), fps=4)  # Slower fps for CPU
                else:
                    # Use actual SVD
                    from diffusers.utils import export_to_video
                    frames = pipe(init_img, decode_chunk_size=2, generator=generator).frames[0]
                    filename += ".mp4"
                    export_to_video(frames, os.path.join(OUTPUT_PATH, filename), fps=7)
                
            else: # txt2img
                result = pipe(
                    prompt=req.prompt,
                    negative_prompt=req.negative_prompt,
                    num_inference_steps=req.steps,
                    guidance_scale=req.cfg,
                    width=req.width,
                    height=req.height,
                    generator=generator
                ).images[0]
                filename += ".png"
                result.save(os.path.join(OUTPUT_PATH, filename))
        
        # Fix URL to be relative for frontend
        return {
            "status": "success", 
            "url": f"outputs/{filename}",
            "type": gen_type,
            "seed": seed_used
        }

    except Exception as e:
        import traceback
        err_msg = traceback.format_exc()
        # Log to file for agent to read
        with open("latest_error.txt", "w") as f:
            f.write(err_msg)
        print(err_msg)
        return {"status": "error", "message": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
