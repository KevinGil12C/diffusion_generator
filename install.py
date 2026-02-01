#!/usr/bin/env python3
"""
AI Image Studio - Installation Script
Guía paso a paso para configurar el proyecto
"""

import os
import sys
import subprocess
import platform
import shutil

def print_header(text):
    print("\n" + "="*60)
    print(f" {text}")
    print("="*60)

def print_step(step, text):
    print(f"\n[{step}] {text}")

def check_python_version():
    """Verificar versión de Python"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ ERROR: Se requiere Python 3.8 o superior")
        print(f"   Versión actual: {version.major}.{version.minor}.{version.micro}")
        return False
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} - OK")
    return True

def check_disk_space():
    """Verificar espacio en disco disponible"""
    try:
        stat = os.statvfs('.')
        free_gb = (stat.f_bavail * stat.f_frsize) / (1024**3)
        if free_gb < 20:
            print(f"⚠️  ADVERTENCIA: Solo {free_gb:.1f}GB libres. Se necesitan ~20GB para modelos.")
            return False
        print(f"✅ Espacio disponible: {free_gb:.1f}GB - OK")
        return True
    except:
        print("⚠️  No se pudo verificar espacio en disco")
        return True

def install_python_dependencies():
    """Instalar dependencias de Python"""
    print_step("3", "Instalando dependencias de Python...")

    try:
        # Actualizar pip
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pip"],
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        # Instalar requirements
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "api/requirements.txt"],
                            stdout=subprocess.DEVNULL)

        print("✅ Dependencias de Python instaladas correctamente")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error instalando dependencias: {e}")
        return False

def create_directory_structure():
    """Crear estructura de directorios"""
    print_step("4", "Creando estructura de directorios...")

    directories = [
        "api/models/checkpoints",
        "api/models/svd_xt_config/unet",
        "api/models/svd_xt_config/vae",
        "api/models/svd_xt_config/image_encoder",
        "web/public/outputs"
    ]

    for dir_path in directories:
        os.makedirs(dir_path, exist_ok=True)
        # Crear .gitkeep
        gitkeep_path = os.path.join(dir_path, ".gitkeep")
        with open(gitkeep_path, 'w') as f:
            f.write("# Este directorio se mantiene vacío intencionalmente\n")

    print("✅ Estructura de directorios creada")

def create_env_file():
    """Crear archivo .env básico"""
    print_step("5", "Creando configuración básica...")

    if not os.path.exists('.env'):
        shutil.copy('.env.example', '.env')
        print("✅ Archivo .env creado desde .env.example")
    else:
        print("⚪ Archivo .env ya existe")

def show_download_instructions():
    """Mostrar instrucciones de descarga"""
    print_header("📥 DESCARGA DE MODELOS REQUERIDA")

    print("Los modelos de IA son archivos pesados y deben descargarse manualmente:")
    print()

    models = {
        "SD 1.5 Pruned": "https://civitai.com/models/2583/sd15-pruned",
        "Realistic Vision V6.0": "https://civitai.com/models/4201/realistic-vision-v60-b1",
        "CyberRealistic V9.0": "https://civitai.com/models/4429/cyberrealistic",
        "Pony Diffusion V6 XL": "https://civitai.com/models/257749/pony-diffusion-v6-xl",
        "HentaiMix XL": "https://civitai.com/models/119199/hentaimix-xl",
        "SVD": "https://civitai.com/models/108189/stable-video-diffusion",
        "SVD-XT": "https://civitai.com/models/101774/stable-video-diffusion-xt"
    }

    print("📁 MODELOS PRINCIPALES (poner en api/models/checkpoints/):")
    for name, url in models.items():
        print(f"   • {name}")
        print(f"     {url}")

    print()
    print("📁 COMPONENTES SVD (poner en api/models/svd_xt_config/):")
    svd_components = {
        "UNet model": "https://huggingface.co/stabilityai/stable-video-diffusion-img2vid-xt/resolve/main/unet/diffusion_pytorch_model.bin",
        "VAE model": "https://huggingface.co/stabilityai/stable-video-diffusion-img2vid-xt/resolve/main/vae/diffusion_pytorch_model.bin",
        "Image Encoder": "https://huggingface.co/stabilityai/stable-video-diffusion-img2vid-xt/resolve/main/image_encoder/model.safetensors"
    }

    for name, url in svd_components.items():
        print(f"   • {name}")
        print(f"     {url}")

    print()
    print("💡 CONSEJOS:")
    print("   • Usa un gestor de descargas para archivos grandes")
    print("   • Verifica que los archivos no estén corruptos")
    print("   • Los archivos .safetensors son más seguros")

def show_startup_instructions():
    """Mostrar instrucciones para iniciar"""
    print_header("🚀 CÓMO INICIAR")

    print("Una vez descargados todos los modelos:")
    print()
    print("1. Iniciar el servidor:")
    print("   cd api")
    print("   python main.py")
    print()
    print("2. Abrir en navegador:")
    print("   http://127.0.0.1:8000")
    print()
    print("3. ¡Disfrutar!")
    print()
    print("📊 MONITOREO:")
    print("   • Logs: api/server_log.txt")
    print("   • Errores: api/latest_error.txt")

def main():
    print_header("🎨 AI IMAGE STUDIO - INSTALACIÓN")

    # Verificar sistema operativo
    os_name = platform.system()
    print(f"Sistema operativo: {os_name}")

    # Paso 1: Verificar Python
    print_step("1", "Verificando Python...")
    if not check_python_version():
        return

    # Paso 2: Verificar espacio
    print_step("2", "Verificando espacio en disco...")
    check_disk_space()

    # Paso 3: Instalar dependencias
    if not install_python_dependencies():
        return

    # Paso 4: Crear estructura
    create_directory_structure()

    # Paso 5: Crear configuración
    create_env_file()

    # Mostrar instrucciones finales
    show_download_instructions()
    show_startup_instructions()

    print_header("✅ INSTALACIÓN COMPLETADA")
    print("¡Sigue las instrucciones de descarga y estarás listo!")

if __name__ == "__main__":
    main()