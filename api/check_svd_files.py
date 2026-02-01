import os
import glob

def check_svd_components():
    base_dir = "models/svd_xt_config"

    components = {
        "unet": os.path.join(base_dir, "unet"),
        "vae": os.path.join(base_dir, "vae"),
        "image_encoder": os.path.join(base_dir, "image_encoder")
    }

    print("=== VERIFICACIÓN DE COMPONENTES SVD ===\n")

    for component_name, component_path in components.items():
        print(f"📁 {component_name.upper()}:")
        print(f"   Ruta: {component_path}")

        if os.path.exists(component_path):
            files = os.listdir(component_path)
            print(f"   ✅ Directorio existe - {len(files)} archivos:")

            for file in files:
                file_path = os.path.join(component_path, file)
                size_mb = os.path.getsize(file_path) / (1024 * 1024)
                print("2d"
        else:
            print("   ❌ Directorio NO existe")

        print()

    # Buscar archivos .safetensors en cualquier lugar
    print("🔍 BUSCANDO ARCHIVOS .safetensors:")
    safetensors_files = glob.glob("models/**/*.safetensors", recursive=True)
    if safetensors_files:
        for file in safetensors_files:
            size_mb = os.path.getsize(file) / (1024 * 1024)
            print(".1f"
    else:
        print("   ❌ No se encontraron archivos .safetensors")

    print("\n=== RESULTADO ===")
    unet_model = os.path.exists(os.path.join(components["unet"], "diffusion_pytorch_model.bin")) or \
                 os.path.exists(os.path.join(components["unet"], "diffusion_pytorch_model.safetensors"))
    vae_model = os.path.exists(os.path.join(components["vae"], "diffusion_pytorch_model.bin")) or \
                os.path.exists(os.path.join(components["vae"], "diffusion_pytorch_model.safetensors"))

    if unet_model and vae_model:
        print("✅ COMPONENTES COMPLETOS - El video real debería funcionar!")
    else:
        print("❌ COMPONENTES INCOMPLETOS - Usará fallback de video")
        if not unet_model:
            print("   - Falta: UNet model")
        if not vae_model:
            print("   - Falta: VAE model")

if __name__ == "__main__":
    check_svd_components()