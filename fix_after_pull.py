#!/usr/bin/env python3
"""
Script para arreglar problemas después de un git pull
"""

import os
import shutil

def fix_pull_issues():
    print("🔧 ARREGLANDO PROBLEMAS DESPUÉS DE GIT PULL")
    print("="*50)

    # Verificar archivos importantes que podrían haberse sobrescrito
    critical_files = [
        "README.md",
        "api/main.py",
        "web/templates/generator/index.html.twig",
        ".gitignore",
        ".env.example"
    ]

    print("📁 Verificando archivos críticos...")
    for file in critical_files:
        if os.path.exists(file):
            print(f"   ✅ {file} existe")
        else:
            print(f"   ❌ {file} FALTANTE - Necesita restaurarse")

    # Verificar si hay archivos de respaldo
    backup_files = [f for f in os.listdir('.') if f.endswith('.bak') or f.endswith('.orig')]
    if backup_files:
        print(f"\n📋 Archivos de respaldo encontrados: {len(backup_files)}")
        for backup in backup_files:
            print(f"   • {backup}")

    # Verificar modelos (deberían estar vacíos)
    models_dir = "api/models"
    if os.path.exists(models_dir):
        checkpoints = os.path.join(models_dir, "checkpoints")
        if os.path.exists(checkpoints):
            files = os.listdir(checkpoints)
            if files:
                print(f"\n⚠️  ADVERTENCIA: Hay {len(files)} archivos en checkpoints")
                print("   Los modelos deberían descargarse manualmente")
            else:
                print("\n✅ Directorio checkpoints vacío (correcto)")

    print("\n🔄 SOLUCIONES RECOMENDADAS:")
    print()
    print("1. SI HAY ARCHIVOS SOBRESCRITOS:")
    print("   git checkout HEAD -- archivo_sobrescrito")
    print("   # O restaura desde backup si existe")
    print()
    print("2. SI HAY CONFLICTOS:")
    print("   git status  # Ver archivos con conflictos")
    print("   # Edita los archivos y resuelve conflictos")
    print("   git add archivo_resuelto")
    print("   git commit")
    print()
    print("3. SI QUIERES REVERTIR EL PULL:")
    print("   git reset --hard HEAD~1  # Deshace el último commit")
    print("   # O para revertir completamente:")
    print("   git reset --hard origin/main  # Si hay rama remota")
    print()
    print("4. PARA LIMPIAR Y RECONFIGURAR:")
    print("   python clean_repository.py")
    print("   python verify_setup.py")
    print()
    print("5. PARA VOLVER A PREPARAR:")
    print("   python prepare_for_github.py")
    print()

    print("❓ ¿QUÉ PROBLEMA TIENES ESPECÍFICAMENTE?")
    print("   • ¿Archivos sobrescritos?")
    print("   • ¿Conflictos de merge?")
    print("   • ¿Archivos faltantes?")
    print("   • ¿Modelos eliminados?")

if __name__ == "__main__":
    fix_pull_issues()