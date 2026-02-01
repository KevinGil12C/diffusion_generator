#!/usr/bin/env python3
"""
AI Image Studio - Setup Verification Script
Verifica que todo esté configurado correctamente
"""

import os
import sys
import subprocess
import importlib.util

def print_header(text):
    print("\n" + "="*60)
    print(f" {text}")
    print("="*60)

def print_check(name, status, details=""):
    status_icon = "✅" if status else "❌"
    print("20")
    if details and not status:
        print(f"       {details}")

def check_python_requirements():
    """Verificar versión de Python y dependencias críticas"""
    print_header("🐍 VERIFICACIÓN DE PYTHON")

    # Python version
    version = sys.version_info
    python_ok = version.major >= 3 and version.minor >= 8
    print_check("Python 3.8+", python_ok, f"Versión actual: {version.major}.{version.minor}.{version.micro}")

    # Critical imports
    critical_modules = ['torch', 'diffusers', 'fastapi', 'PIL']
    for module in critical_modules:
        try:
            if module == 'PIL':
                import PIL
            else:
                importlib.import_module(module)
            print_check(f"Módulo {module}", True)
        except ImportError:
            print_check(f"Módulo {module}", False, "Ejecuta: pip install -r api/requirements.txt")

    return python_ok

def check_directory_structure():
    """Verificar estructura de directorios"""
    print_header("📁 VERIFICACIÓN DE DIRECTORIOS")

    required_dirs = [
        "api/models/checkpoints",
        "api/models/svd_xt_config/unet",
        "api/models/svd_xt_config/vae",
        "api/models/svd_xt_config/image_encoder",
        "web/public/outputs"
    ]

    all_dirs_ok = True
    for dir_path in required_dirs:
        exists = os.path.exists(dir_path)
        print_check(f"Directorio {dir_path}", exists)
        if not exists:
            all_dirs_ok = False

    return all_dirs_ok

def check_models():
    """Verificar modelos descargados"""
    print_header("🤖 VERIFICACIÓN DE MODELOS")

    model_checks = [
        ("SD 1.5 Pruned", "api/models/checkpoints/v1-5-pruned-emaonly.safetensors"),
        ("Realistic Vision", "api/models/checkpoints/realisticVisionV60B1_v51HyperVAE.safetensors"),
        ("SVD-XT", "api/models/checkpoints/svd_xt.safetensors"),
        ("UNet SVD", "api/models/svd_xt_config/unet/diffusion_pytorch_model.bin"),
        ("VAE SVD", "api/models/svd_xt_config/vae/diffusion_pytorch_model.bin"),
        ("Image Encoder", "api/models/svd_xt_config/image_encoder/model.safetensors")
    ]

    models_found = 0
    total_models = len(model_checks)

    for name, path in model_checks:
        exists = os.path.exists(path)
        if exists:
            size_mb = os.path.getsize(path) / (1024 * 1024)
            print_check(f"{name}", True, f"{size_mb:.0f} MB")
            models_found += 1
        else:
            print_check(f"{name}", False, "Descarga requerida")

    print(f"\n📊 Modelos encontrados: {models_found}/{total_models}")
    if models_found == 0:
        print("💡 Ejecuta: python install.py  (para ver enlaces de descarga)")
    elif models_found < total_models:
        print("⚠️  Algunos modelos faltan. El sistema usará fallbacks.")

    return models_found > 0

def check_configuration():
    """Verificar archivos de configuración"""
    print_header("⚙️ VERIFICACIÓN DE CONFIGURACIÓN")

    config_files = [
        (".env", ".env.example"),
        ("api/requirements.txt", ""),
        ("web/composer.json", ""),
        ("README.md", "")
    ]

    all_config_ok = True
    for config_file, template in config_files:
        exists = os.path.exists(config_file)
        print_check(f"Archivo {config_file}", exists)
        if not exists and template:
            print(f"       💡 Copia {template} a {config_file}")
            all_config_ok = False

    return all_config_ok

def check_php_setup():
    """Verificar setup de PHP/Symfony (opcional)"""
    print_header("🐘 VERIFICACIÓN DE PHP (OPCIONAL)")

    try:
        result = subprocess.run(['php', '--version'],
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            version_line = result.stdout.split('\n')[0]
            print_check("PHP instalado", True, version_line)
        else:
            print_check("PHP instalado", False, "PHP no encontrado")
            return False
    except (subprocess.TimeoutExpired, FileNotFoundError):
        print_check("PHP instalado", False, "PHP no encontrado en PATH")
        return False

    # Check Composer
    try:
        result = subprocess.run(['composer', '--version'],
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            version_line = result.stdout.split('\n')[0]
            print_check("Composer", True, version_line)
        else:
            print_check("Composer", False, "Composer no encontrado")
    except (subprocess.TimeoutExpired, FileNotFoundError):
        print_check("Composer", False, "Composer no encontrado en PATH")

    return True

def show_next_steps(models_ok, config_ok):
    """Mostrar próximos pasos"""
    print_header("🚀 PRÓXIMOS PASOS")

    if not models_ok:
        print("1. 📥 DESCARGAR MODELOS:")
        print("   • Ejecuta: python install.py")
        print("   • Sigue los enlaces de descarga")
        print("   • Coloca archivos en las carpetas correctas")
        print()

    if not config_ok:
        print("2. ⚙️ CONFIGURAR ENTORNO:")
        print("   • Copia .env.example a .env")
        print("   • Ajusta configuración si es necesario")
        print()

    print("3. ▶️ INICIAR SERVIDOR:")
    print("   cd api")
    print("   python main.py")
    print()

    print("4. 🌐 ACCEDER:")
    print("   Abre: http://127.0.0.1:8000")
    print()

    if models_ok and config_ok:
        print("🎉 ¡TODO LISTO! El sistema está completamente configurado.")
    else:
        print("⚠️  Completa los pasos anteriores antes de usar.")

def main():
    print_header("🔍 VERIFICACIÓN DE SETUP - AI IMAGE STUDIO")

    # Verificar componentes
    python_ok = check_python_requirements()
    dirs_ok = check_directory_structure()
    models_ok = check_models()
    config_ok = check_configuration()
    check_php_setup()  # Opcional

    # Resumen
    print_header("📊 RESUMEN DE VERIFICACIÓN")

    checks = [
        ("Python y dependencias", python_ok),
        ("Estructura de directorios", dirs_ok),
        ("Modelos descargados", models_ok),
        ("Archivos de configuración", config_ok)
    ]

    for name, status in checks:
        print_check(name, status)

    # Calcular estado general
    overall_ok = python_ok and dirs_ok and config_ok

    if overall_ok and models_ok:
        print("\n🎉 SETUP COMPLETO - Todo está listo para usar!")
    elif overall_ok and not models_ok:
        print("\n⚠️  SETUP BÁSICO OK - Solo faltan modelos")
    else:
        print("\n❌ SETUP INCOMPLETO - Revisa los errores arriba")

    show_next_steps(models_ok, config_ok)

if __name__ == "__main__":
    main()