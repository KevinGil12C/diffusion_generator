#!/usr/bin/env python3
"""
Script para resolver conflictos de merge automáticamente
"""

import os
import re

def resolve_merge_conflicts():
    print("🔧 RESOLVIENDO CONFLICTOS DE MERGE")
    print("="*50)

    # Archivos a verificar
    files_to_check = [
        'README.md',
        '.gitignore',
        '.gitattributes',
        'LICENSE',
        'api/requirements.txt',
        'api/start_backend.bat',
        'api/repair_and_start.bat'
    ]

    conflicts_resolved = 0

    for file_path in files_to_check:
        if not os.path.exists(file_path):
            print(f"⚠️  Archivo no encontrado: {file_path}")
            continue

        print(f"\n📄 Procesando: {file_path}")

        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Buscar marcadores de conflicto
        conflict_pattern = r'<<<<<<< HEAD\s*(.*?)\s*=======\s*(.*?)\s*>>>>>>> \w+'
        conflicts = re.findall(conflict_pattern, content, re.DOTALL)

        if conflicts:
            print(f"   🔍 Encontrados {len(conflicts)} conflictos")

            # Resolver conflictos - mantener la versión HEAD (local)
            for head_version, remote_version in conflicts:
                # Para URLs, mantener la versión con .git si existe
                if 'github.com' in head_version and 'github.com' in remote_version:
                    if '.git' in head_version:
                        resolved = head_version
                    else:
                        resolved = remote_version
                # Para nombres de directorio, mantener "diffusion_generator"
                elif 'cd ' in head_version and 'cd ' in remote_version:
                    if 'diffusion_generator' in head_version:
                        resolved = head_version
                    else:
                        resolved = remote_version
                # Para otros casos, mantener HEAD
                else:
                    resolved = head_version

                # Reemplazar el conflicto con la versión resuelta
                conflict_marker = f'<<<<<<< HEAD\n{head_version}\n=======\n{remote_version}\n>>>>>>> '
                content = content.replace(conflict_marker, resolved)
                conflicts_resolved += 1
                print(f"   ✅ Resuelto conflicto")

            # Guardar el archivo corregido
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)

            print(f"   💾 Archivo guardado: {file_path}")
        else:
            print(f"   ✅ Sin conflictos")

    print(f"\n📊 RESUMEN:")
    print(f"   • Archivos revisados: {len(files_to_check)}")
    print(f"   • Conflictos resueltos: {conflicts_resolved}")

    if conflicts_resolved > 0:
        print("
🎯 PRÓXIMOS PASOS:"        print("   1. Revisa los archivos modificados")
        print("   2. Ejecuta: git add .")
        print("   3. Ejecuta: git commit -m 'Resolve merge conflicts'")
        print("   4. Ejecuta: git push")
    else:
        print("
✅ No hay conflictos pendientes"        print("   Tu repositorio está sincronizado!")

if __name__ == "__main__":
    resolve_merge_conflicts()