#!/usr/bin/env python3
"""
Script para hacer commit y push del README actualizado a GitHub
"""

import subprocess
import sys

def run_command(command, description):
    """Ejecuta un comando y maneja errores"""
    print(f"\n🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True,
                              capture_output=True, text=True)
        print(f"✅ {description} - Completado")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error en {description}: {e}")
        if e.stdout:
            print(f"STDOUT: {e.stdout}")
        if e.stderr:
            print(f"STDERR: {e.stderr}")
        return False

def main():
    print("🚀 PUSH README ACTUALIZADO A GITHUB")
    print("="*50)
    print("Este script actualizará el README en GitHub")
    print()

    # Verificar estado de git
    print("1. Verificando estado del repositorio...")
    if not run_command("git status --porcelain", "Verificar cambios pendientes"):
        print("No hay cambios para commitear")
        return

    # Agregar README
    if not run_command("git add README.md", "Agregar README.md"):
        return

    # Hacer commit
    commit_msg = "docs: Update README with complete installation guide"
    if not run_command(f'git commit -m "{commit_msg}"', "Crear commit"):
        return

    # Verificar si hay remote configurado
    try:
        result = subprocess.run("git remote -v", shell=True, capture_output=True, text=True)
        if "origin" not in result.stdout:
            print("\n⚠️  No hay remote 'origin' configurado")
            print("Ejecuta estos comandos manualmente:")
            print("git remote add origin https://github.com/KevinGil12C/diffusion_generator.git")
            print("git push -u origin main")
            return
    except:
        pass

    # Hacer push
    if not run_command("git push origin main", "Subir cambios a GitHub"):
        print("\n💡 Si hay problemas con el push:")
        print("   • Asegúrate de tener permisos en el repositorio")
        print("   • Verifica que la rama sea 'main' no 'master'")
        print("   • Usa: git push -u origin main --force-with-lease")
        return

    print("\n🎉 ¡README ACTUALIZADO EXITOSAMENTE!")
    print("\n📋 Resumen de cambios:")
    print("   ✅ README.md actualizado con documentación completa")
    print("   ✅ Instrucciones de instalación detalladas")
    print("   ✅ Guías de descarga de modelos")
    print("   ✅ Solución de problemas incluida")
    print()
    print("🔗 Ver el resultado en:")
    print("   https://github.com/KevinGil12C/diffusion_generator")
    print()
    print("📖 El README ahora incluye:")
    print("   • Guía de instalación automática")
    print("   • Todos los enlaces de descarga")
    print("   • Configuraciones optimizadas")
    print("   • Solución de problemas completa")

if __name__ == "__main__":
    main()