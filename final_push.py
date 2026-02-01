#!/usr/bin/env python3
"""
Script final para preparar y hacer push de todos los cambios a GitHub
"""

import os
import subprocess
import sys

def run_command(command, description, allow_fail=False):
    """Ejecuta un comando y maneja errores"""
    print(f"\n🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True,
                              capture_output=True, text=True)
        print(f"✅ {description} - Completado")
        return True
    except subprocess.CalledProcessError as e:
        if allow_fail:
            print(f"⚠️  {description} - Continuando (permitido fallar)")
            return True
        else:
            print(f"❌ Error en {description}: {e}")
            if e.stdout:
                print(f"STDOUT: {e.stdout}")
            if e.stderr:
                print(f"STDERR: {e.stderr}")
            return False

def main():
    print("🚀 PREPARACIÓN FINAL PARA PUSH A GITHUB")
    print("="*60)
    print("Este script preparará y subirá todos los cambios")
    print()

    # Verificar que estamos en un repo git
    if not os.path.exists('.git'):
        print("❌ No es un repositorio Git. Ejecuta 'git init' primero.")
        return

    # Verificar archivos importantes
    required_files = [
        'README.md',
        'LICENSE',
        '.gitignore',
        'api/requirements.txt'
    ]

    missing_files = []
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)

    if missing_files:
        print("❌ Archivos faltantes:")
        for file in missing_files:
            print(f"   • {file}")
        return

    print("✅ Todos los archivos requeridos están presentes")

    # Verificar estado de git
    run_command("git status --porcelain", "Verificar estado del repositorio", allow_fail=True)

    # Agregar todos los archivos
    files_to_add = [
        'README.md',
        'LICENSE',
        '.gitignore',
        '.gitattributes',
        '.env.example',
        'install.py',
        'verify_setup.py',
        'clean_repository.py',
        'prepare_for_github.py',
        'fix_after_pull.py',
        'resolve_merge_conflicts.py',
        'push_readme.py',
        'check_readme.py',
        'final_push.py',
        'api/requirements.txt',
        'web/composer.json',
        '.github/README.md'
    ]

    for file in files_to_add:
        if os.path.exists(file):
            run_command(f"git add {file}", f"Agregar {file}")

    # Verificar si hay cambios para commitear
    try:
        result = subprocess.run("git diff --cached --name-only",
                              shell=True, capture_output=True, text=True)
        if not result.stdout.strip():
            print("\n⚠️  No hay cambios para commitear")
            print("Los archivos ya están actualizados")
            return
    except:
        pass

    # Hacer commit
    commit_message = "docs: Complete README with installation guide and model download links"
    if not run_command(f'git commit -m "{commit_message}"',
                      "Crear commit con README actualizado"):
        return

    # Verificar remote
    try:
        result = subprocess.run("git remote -v", shell=True,
                              capture_output=True, text=True)
        if "origin" not in result.stdout:
            print("\n⚠️  Configurando remote origin...")
            run_command("git remote add origin https://github.com/KevinGil12C/diffusion_generator.git",
                       "Agregar remote origin")

        # Verificar que el remote sea correcto
        if "KevinGil12C/diffusion_generator" not in result.stdout:
            print("⚠️  Remote incorrecto. Corrigiendo...")
            run_command("git remote set-url origin https://github.com/KevinGil12C/diffusion_generator.git",
                       "Corregir URL del remote")

    except:
        print("⚠️  Error al verificar remote")

    # Hacer push
    if not run_command("git push origin main",
                      "Subir cambios a GitHub"):
        print("\n💡 Si hay problemas con el push:")
        print("   • Verifica que tienes permisos en el repositorio")
        print("   • Si la rama es 'master', usa: git push origin master")
        print("   • Para forzar push: git push origin main --force-with-lease")
        return

    print("\n" + "="*60)
    print("🎉 ¡PUSH COMPLETADO EXITOSAMENTE!")
    print("="*60)

    print("\n📋 Cambios subidos:")
    print("   ✅ README.md completo con documentación detallada")
    print("   ✅ Scripts de instalación y verificación")
    print("   ✅ Configuración de Git (.gitignore, .gitattributes)")
    print("   ✅ Licencia MIT actualizada")
    print("   ✅ Todos los enlaces de descarga incluidos")

    print("\n🔗 Ver el resultado en:")
    print("   https://github.com/KevinGil12C/diffusion_generator")

    print("\n📖 El README ahora incluye:")
    print("   • Instalación automática con script")
    print("   • Todos los enlaces de descarga de modelos")
    print("   • Guía completa de presets optimizados")
    print("   • Solución de problemas detallada")
    print("   • Arquitectura técnica documentada")
    print("   • Créditos y información del desarrollador")

    print("\n💡 Para verificar que todo funciona:")
    print("   git clone https://github.com/KevinGil12C/diffusion_generator.git")
    print("   cd diffusion_generator")
    print("   python install.py")

if __name__ == "__main__":
    main()