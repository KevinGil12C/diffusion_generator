import os
import requests
import json
from huggingface_hub import snapshot_download

CONFIG_DIR = "models/svd_xt_config"
MODEL_DIR = "models/svd_xt_components"
BASE_URL = "https://huggingface.co/stabilityai/stable-video-diffusion-img2vid-xt/resolve/main"

# Structure needed for diffusers loading
files_to_download = [
    # Config files
    "model_index.json",
    "scheduler/scheduler_config.json",
    "feature_extractor/preprocessor_config.json",
    "image_encoder/config.json",
    "unet/config.json",
    "vae/config.json"
]

def download_file(path):
    url = f"{BASE_URL}/{path}"
    target_path = os.path.join(CONFIG_DIR, path)
    os.makedirs(os.path.dirname(target_path), exist_ok=True)

    print(f"Downloading {path}...")
    try:
        resp = requests.get(url, timeout=30)
        if resp.status_code == 200:
            with open(target_path, "wb") as f:
                f.write(resp.content)
            print("OK.")
        else:
            print(f"Failed: {resp.status_code}")
    except Exception as e:
        print(f"Error: {e}")

def download_svd_components():
    """Download the missing SVD components from HuggingFace"""
    print("Downloading SVD components from HuggingFace...")

    try:
        # Download the full SVD-XT model components
        snapshot_download(
            repo_id="stabilityai/stable-video-diffusion-img2vid-xt",
            local_dir=MODEL_DIR,
            local_dir_use_symlinks=False,
            ignore_patterns=["*.md", "*.txt", "*.git*"]
        )
        print("Successfully downloaded SVD components!")

        # Copy configs to our config directory
        import shutil
        config_files = [
            "model_index.json",
            "scheduler/scheduler_config.json",
            "feature_extractor/preprocessor_config.json",
            "image_encoder/config.json",
            "unet/config.json",
            "vae/config.json"
        ]

        for config_file in config_files:
            src = os.path.join(MODEL_DIR, config_file)
            dst = os.path.join(CONFIG_DIR, config_file)
            if os.path.exists(src):
                os.makedirs(os.path.dirname(dst), exist_ok=True)
                shutil.copy2(src, dst)
                print(f"Copied {config_file}")

        print("SVD components setup complete!")

    except Exception as e:
        print(f"Error downloading components: {e}")
        print("Falling back to manual download...")
        for f in files_to_download:
            download_file(f)

if __name__ == "__main__":
    print("Starting SVD components download...")
    download_svd_components()
    print("Done. You can now restart the backend.")
