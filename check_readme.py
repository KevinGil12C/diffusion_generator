#!/usr/bin/env python3
"""
Script para verificar que el README esté completo antes de subir a GitHub
"""

def check_readme_content():
    """Verifica que el README tenga todo el contenido necesario"""
    print("📖 VERIFICANDO CONTENIDO DEL README")
    print("="*40)

    try:
        with open('README.md', 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        print("❌ README.md no encontrado")
        return False

    # Lista de elementos requeridos
    required_elements = [
        ("Título principal", "# AI Image Studio 🎨"),
        ("URL del repo correcta", "https://github.com/KevinGil12C/diffusion_generator.git"),
        ("Instalación automática", "python install.py"),
        ("Sección de descarga de modelos", "## 📥 Descarga de Modelos"),
        ("Enlaces de Civitai", "civitai.com/models/2583"),
        ("Enlaces de HuggingFace", "huggingface.co/stabilityai"),
        ("Guía de presets", "## 📚 Guía de Presets"),
        ("Cambiar Ropa preset", "### 🎨 Cambiar Ropa"),
        ("Cambiar Pose preset", "### 💃 Cambiar Pose"),
        ("Solución de problemas", "## 🐛 Solución de Problemas"),
        ("Créditos correctos", "KevinGil12C"),
        ("Tabla de contenidos", "## 📋 Tabla de Contenidos")
    ]

    missing_elements = []
    found_elements = []

    for name, text in required_elements:
        if text in content:
            found_elements.append(f"✅ {name}")
        else:
            missing_elements.append(f"❌ {name}")

    print("Elementos encontrados:")
    for element in found_elements:
        print(f"   {element}")

    if missing_elements:
        print("\nElementos faltantes:")
        for element in missing_elements:
            print(f"   {element}")
        return False

    # Verificar longitud mínima
    lines = content.split('\n')
    if len(lines) < 200:
        print(f"\n⚠️  README muy corto ({len(lines)} líneas). Debería tener ~300+ líneas.")
        return False

    print("
📊 Estadísticas del README:"    print(f"   • Líneas totales: {len(lines)}")
    print(f"   • Caracteres: {len(content)}")
    print(f"   • Palabras: {len(content.split())}")

    # Contar secciones principales
    sections = content.count('## ')
    print(f"   • Secciones: {sections}")

    return True

def check_urls():
    """Verifica que todas las URLs sean correctas"""
    print("\n🔗 VERIFICANDO URLs")

    try:
        with open('README.md', 'r', encoding='utf-8') as f:
            content = f.read()
    except FileNotFoundError:
        return False

    # URLs que deben estar presentes
    required_urls = [
        "https://github.com/KevinGil12C/diffusion_generator.git",
        "https://civitai.com/models/2583",
        "https://huggingface.co/stabilityai",
        "https://python.org",
        "https://fastapi.tiangolo.com",
        "https://stability.ai"
    ]

    missing_urls = []
    for url in required_urls:
        if url in content:
            print(f"   ✅ {url}")
        else:
            missing_urls.append(url)
            print(f"   ❌ {url}")

    if missing_urls:
        print(f"\n❌ Faltan {len(missing_urls)} URLs")
        return False

    return True

def main():
    print("🔍 VERIFICACIÓN COMPLETA DEL README")
    print("="*50)

    content_ok = check_readme_content()
    urls_ok = check_urls()

    print("\n" + "="*50)
    print("📋 RESULTADO FINAL:")

    if content_ok and urls_ok:
        print("🎉 ¡README COMPLETO Y CORRECTO!")
        print("\n✅ Listo para subir a GitHub")
        print("\nPara subir ejecuta:")
        print("   python push_readme.py")
        return True
    else:
        print("❌ README INCOMPLETO")
        print("\n🔧 Revisa los elementos faltantes arriba")
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)