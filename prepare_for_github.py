#!/usr/bin/env python3
"""
Script para preparar el repositorio antes de subir a GitHub
"""

import os
import subprocess

def main():
    print("🚀 PREPARACIÓN FINAL PARA GITHUB")
    print("="*50)

    # Ejecutar limpieza
    print("1. Ejecutando limpieza del repositorio...")
    try:
        subprocess.run(["python", "clean_repository.py"], check=True)
        print("   ✅ Limpieza completada")
    except subprocess.CalledProcessError:
        print("   ❌ Error en limpieza")

    # Verificar setup
    print("\n2. Verificando configuración...")
    try:
        result = subprocess.run(["python", "verify_setup.py"],
                              capture_output=True, text=True, timeout=30)
        if "completo" in result.stdout.lower():
            print("   ✅ Verificación exitosa")
        else:
            print("   ⚠️  Verificación con advertencias")
    except Exception as e:
        print(f"   ❌ Error en verificación: {e}")

    # Verificar archivos importantes
    print("\n3. Verificando archivos importantes...")
    required_files = [
        "README.md",
        "LICENSE",
        ".gitignore",
        ".gitattributes",
        "api/requirements.txt",
        "web/composer.json"
    ]

    for file in required_files:
        if os.path.exists(file):
            print(f"   ✅ {file}")
        else:
            print(f"   ❌ {file} - FALTANTE")

    print("\n4. Información del repositorio:")
    print("   📦 Nombre: diffusion_generator")
    print("   👤 Usuario: KevinGil12C")
    print("   🔗 URL: https://github.com/KevinGil12C/diffusion_generator")

    print("\n📝 PRÓXIMOS PASOS:")
    print("   1. Crear repositorio en GitHub: KevinGil12C/diffusion_generator")
    print("   2. Ejecutar los comandos:")
    print("      git init")
    print("      git add .")
    print("      git commit -m \"Initial commit: AI Image Studio\"")
    print("      git branch -M main")
    print("      git remote add origin https://github.com/KevinGil12C/diffusion_generator.git")
    print("      git push -u origin main")

    print("\n🎉 ¡REPOSITORIO LISTO PARA GITHUB!")

if __name__ == "__main__":
    main()