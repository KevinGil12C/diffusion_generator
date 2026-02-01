#!/usr/bin/env python3
"""
Script para limpiar el repositorio eliminando archivos pesados
antes de subir a GitHub
"""

import os
import shutil

def clean_repository():
    print("🧹 LIMPIANDO REPOSITORIO PARA GITHUB")
    print("="*50)

    files_to_remove = [
        # Modelos pesados
        "api/models",
        "web/public/outputs",

        # Logs y archivos temporales
        "api/server_log.txt",
        "api/latest_error.txt",
        "api/debug_env.txt",

        # Scripts de debug
        "api/debug_svd_load.py",
        "api/test_video.py",
        "api/test_simple.py",
        "api/test_memory.py",
        "api/verify_svd.py",
        "api/check_svd_files.py",

        # Scripts de test
        "web/test_presets.py",
        "web/test_clothing_change.py",
    ]

    directories_to_remove = [
        "api/venv",
        "api/__pycache__",
        "web/var",
        "web/vendor",
        "web/node_modules",
    ]

    print("📁 Eliminando archivos pesados...")
    for file_path in files_to_remove:
        if os.path.exists(file_path):
            try:
                if os.path.isfile(file_path):
                    os.remove(file_path)
                    print(f"   ✅ Eliminado: {file_path}")
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
                    print(f"   ✅ Eliminada carpeta: {file_path}")
            except Exception as e:
                print(f"   ❌ Error eliminando {file_path}: {e}")
        else:
            print(f"   ⚪ No existe: {file_path}")

    print("\n📂 Eliminando directorios temporales...")
    for dir_path in directories_to_remove:
        if os.path.exists(dir_path):
            try:
                shutil.rmtree(dir_path)
                print(f"   ✅ Eliminada: {dir_path}")
            except Exception as e:
                print(f"   ❌ Error eliminando {dir_path}: {e}")
        else:
            print(f"   ⚪ No existe: {dir_path}")

    # Crear directorios necesarios vacíos
    print("\n📂 Creando estructura de directorios...")
    dirs_to_create = [
        "api/models",
        "api/models/checkpoints",
        "api/models/svd_xt_config",
        "api/models/svd_xt_config/unet",
        "api/models/svd_xt_config/vae",
        "api/models/svd_xt_config/image_encoder",
        "web/public/outputs",
    ]

    for dir_path in dirs_to_create:
        os.makedirs(dir_path, exist_ok=True)
        # Crear .gitkeep para mantener directorios vacíos en git
        gitkeep_path = os.path.join(dir_path, ".gitkeep")
        with open(gitkeep_path, 'w') as f:
            f.write("# Este directorio se mantiene vacío intencionalmente\n")
        print(f"   ✅ Creado: {dir_path}/")

    print("\n✅ LIMPIEZA COMPLETADA")
    print("\n📋 ARCHIVOS A DESCARGAR MANUALMENTE:")
    print("="*50)
    print("📁 MODELOS (poner en api/models/checkpoints/):")
    print("   • v1-5-pruned-emaonly.safetensors")
    print("   • realisticVisionV60B1_v51HyperVAE.safetensors")
    print("   • cyberrealistic_v90.safetensors")
    print("   • ponyDiffusionV6XL_v6StartWithThisOne.safetensors")
    print("   • hentaiMixXLRoadTo_v50.safetensors")
    print("   • svd_xt.safetensors")
    print("   • svd.safetensors")
    print()
    print("📁 COMPONENTES SVD (poner en api/models/svd_xt_config/):")
    print("   • unet/diffusion_pytorch_model.bin")
    print("   • vae/diffusion_pytorch_model.bin")
    print("   • image_encoder/model.safetensors")
    print("   • image_encoder/config.json")
    print("   • unet/config.json")
    print("   • vae/config.json")
    print("   • model_index.json")
    print()
    print("🔗 ENLACES DE DESCARGA:")
    print("   https://civitai.com/ (para modelos)")
    print("   https://huggingface.co/stabilityai/ (para SVD)")
    print()
    print("🚀 PRÓXIMOS PASOS:")
    print("   1. Ejecutar: pip install -r requirements.txt")
    print("   2. Descargar modelos manualmente")
    print("   3. Ejecutar: python api/main.py")
    print()
    print("✨ Repositorio listo para GitHub!")

if __name__ == "__main__":
    clean_repository()