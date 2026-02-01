import os

def verify_svd_files():
    print("=== VERIFICACIÓN DE ARCHIVOS SVD ===\n")

    base_path = "models/svd_xt_config"

    components = {
        "unet": os.path.join(base_path, "unet"),
        "vae": os.path.join(base_path, "vae"),
        "image_encoder": os.path.join(base_path, "image_encoder")
    }

    all_components_ready = True

    for name, path in components.items():
        print(f"📁 {name.upper()}:")
        print(f"   Ruta: {path}")

        if os.path.exists(path):
            files = [f for f in os.listdir(path) if not f.startswith('.')]
            print(f"   ✅ Directorio existe - {len(files)} archivos")

            model_files = [f for f in files if 'diffusion_pytorch_model' in f or 'model.safetensors' in f]
            if model_files:
                for model_file in model_files:
                    file_path = os.path.join(path, model_file)
                    size_mb = os.path.getsize(file_path) / (1024 * 1024)
                    print(".1f"            else:
                print("   ⚠️  No hay archivo de modelo"
                if name in ["unet", "vae"]:
                    all_components_ready = False
        else:
            print("   ❌ Directorio NO existe"
            if name in ["unet", "vae"]:
                all_components_ready = False

        print()

    print("=== RESULTADO ===")
    if all_components_ready:
        print("✅ TODOS LOS COMPONENTES LISTOS")
        print("🎬 El video real con SVD debería funcionar!")
        print("\nPara probar:")
        print('POST /generate con mode="img2vid" y model_name="svd_xt.safetensors"')
    else:
        print("❌ COMPONENTES INCOMPLETOS")
        print("📼 Se usará el sistema de fallback (video con img2img)")
        print("\nFaltan:")
        unet_path = os.path.join(base_path, "unet")
        vae_path = os.path.join(base_path, "vae")

        unet_files = [f for f in os.listdir(unet_path) if 'diffusion_pytorch_model' in f or 'model.safetensors' in f] if os.path.exists(unet_path) else []
        vae_files = [f for f in os.listdir(vae_path) if 'diffusion_pytorch_model' in f or 'model.safetensors' in f] if os.path.exists(vae_path) else []

        if not unet_files:
            print("  - UNet model (diffusion_pytorch_model.bin o .safetensors)")
        if not vae_files:
            print("  - VAE model (diffusion_pytorch_model.bin o .safetensors)")

if __name__ == "__main__":
    verify_svd_files()