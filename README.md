# AI Image Studio 🎨

**Herramienta Profesional de Edición Fotográfica con IA**

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green.svg)](https://fastapi.tiangolo.com)
[![Stable Diffusion](https://img.shields.io/badge/Stable_Diffusion-2.1+-purple.svg)](https://stability.ai)

---

## 📋 Tabla de Contenidos
- [🚀 Características](#-características)
- [🛠️ Instalación](#️-instalación)
- [📥 Descarga de Modelos](#-descarga-de-modelos)
- [🎯 Uso](#-uso)
- [🔧 Configuración](#-configuración)
- [📚 Guía de Presets](#-guía-de-presets)
- [🐛 Solución de Problemas](#-solución-de-problemas)
- [📄 Licencia](#-licencia)

---

## 🚀 Características

### 🎨 Herramientas de Edición Profesional
- **Cambiar Ropa**: Edición fotográfica precisa con preservación facial máxima
- **Cambiar Pose**: Modificación de poses manteniendo identidad completa
- **Estilo Anime**: Conversión profesional a arte anime
- **Fotorealismo**: Mejora de calidad fotográfica hiperrealista
- **Animación**: Generación de video optimizada para CPU
- **Contenido Viral**: Ediciones divertidas y memes

### 🧠 Inteligencia Artificial
- **Selección Automática de Modelos**: El sistema elige el mejor modelo para cada tarea
- **Optimización de Memoria**: Funciona en hardware limitado (16GB RAM)
- **Preservación Facial**: Tecnología avanzada para mantener identidad
- **Fallback Inteligente**: Sistema de respaldo automático

### 💻 Interfaz Profesional
- **Proporciones Optimizadas**: Botones para 1:1, 9:16, 16:9, 21:9
- **Presets Pre-configurados**: Configuraciones optimizadas por caso de uso
- **Vista en Tiempo Real**: Previsualización instantánea
- **Responsive Design**: Funciona en desktop y mobile

---

## 🛠️ Instalación

### Prerrequisitos
- **Python 3.8+** 🐍
- **16GB RAM** (mínimo recomendado)
- **Git** 📦

### Instalación Automática (Recomendado)
```bash
# Clonar y configurar automáticamente
git clone https://github.com/KevinGil12C/diffusion_generator.git
cd diffusion_generator
python install.py
```

### Instalación Manual
```bash
# 1. Clonar el repositorio
git clone https://github.com/KevinGil12C/diffusion_generator.git
cd diffusion_generator

# 2. Verificar requisitos
python -c "import sys; print('Python:', sys.version_info[:2]); import psutil; print('RAM:', psutil.virtual_memory().total//(1024**3), 'GB')"

# 3. Instalar dependencias de Python
cd api
pip install -r requirements.txt

# 4. Limpiar y verificar setup
cd ..
python clean_repository.py
python verify_setup.py
```

Esto preparará la estructura de directorios y verificará que todo esté configurado correctamente.

### Preparación Final para GitHub

Antes de subir a GitHub, ejecuta:

```bash
python prepare_for_github.py
```

Este script limpiará, verificará y te dará las instrucciones exactas para el commit inicial.

---

## 📥 Descarga de Modelos

### 🚨 IMPORTANTE
Los modelos de IA son archivos pesados (2-10GB cada uno) y **NO se incluyen** en el repositorio para evitar límites de GitHub. Debes descargarlos manualmente.

### 📁 Estructura Requerida
```
api/models/
├── checkpoints/           # Modelos principales
│   ├── v1-5-pruned-emaonly.safetensors
│   ├── realisticVisionV60B1_v51HyperVAE.safetensors
│   ├── cyberrealistic_v90.safetensors
│   ├── ponyDiffusionV6XL_v6StartWithThisOne.safetensors
│   ├── hentaiMixXLRoadTo_v50.safetensors
│   ├── svd_xt.safetensors
│   └── svd.safetensors
└── svd_xt_config/         # Componentes SVD
    ├── image_encoder/
    │   ├── config.json
    │   └── model.safetensors
    ├── unet/
    │   ├── config.json
    │   └── diffusion_pytorch_model.bin
    ├── vae/
    │   ├── config.json
    │   └── diffusion_pytorch_model.bin
    └── model_index.json
```

### 🔗 Enlaces de Descarga

#### 📸 Modelos Principales (Civitai.com)
1. **SD 1.5 Pruned**: https://civitai.com/models/2583/sd15-pruned
2. **Realistic Vision V6.0**: https://civitai.com/models/4201/realistic-vision-v60-b1
3. **CyberRealistic V9.0**: https://civitai.com/models/4429/cyberrealistic
4. **Pony Diffusion V6 XL**: https://civitai.com/models/257749/pony-diffusion-v6-xl
5. **HentaiMix XL**: https://civitai.com/models/119199/hentaimix-xl
6. **SVD**: https://civitai.com/models/108189/stable-video-diffusion
7. **SVD-XT**: https://civitai.com/models/101774/stable-video-diffusion-xt

#### 🤗 Componentes SVD (HuggingFace)
- **Image Encoder**: https://huggingface.co/stabilityai/stable-video-diffusion-img2vid-xt/resolve/main/image_encoder/model.safetensors
- **UNet**: https://huggingface.co/stabilityai/stable-video-diffusion-img2vid-xt/resolve/main/unet/diffusion_pytorch_model.bin
- **VAE**: https://huggingface.co/stabilityai/stable-video-diffusion-img2vid-xt/resolve/main/vae/diffusion_pytorch_model.bin
- **Configs**: Descargar los `config.json` de cada carpeta

### 💡 Consejos de Descarga
- Usa un gestor de descargas (como IDM o aria2) para archivos grandes
- Verifica que los archivos no estén corruptos después de descargar
- Los archivos `.safetensors` son más seguros que los `.ckpt`

---

## 🔍 Verificación de Setup

Antes de usar el sistema, verifica que todo esté configurado:

```bash
# Verificar setup completo
python verify_setup.py
```

Este script comprobará:
- ✅ Versión de Python y dependencias
- ✅ Estructura de directorios
- ✅ Modelos descargados
- ✅ Archivos de configuración
- ✅ Setup opcional de PHP/Symfony

## 🎯 Uso

### Iniciar el Servidor
```bash
cd api
python main.py
```

El servidor estará disponible en: **http://127.0.0.1:8000**

### Interfaz Web
1. Abre tu navegador en `http://127.0.0.1:8000`
2. Selecciona un **Preset** de la sección "Herramientas de Edición"
3. Sube una imagen (para modos img2img)
4. Ajusta parámetros opcionales
5. Haz clic en **"PROCESAR IMAGEN"**

### Modos Disponibles
- **TXT2IMG**: Generar imagen desde texto
- **IMG2IMG**: Editar imagen existente
- **TXT2VID**: Generar video desde texto
- **IMG2VID**: Animar imagen existente

---

## 🔧 Configuración

### Variables de Entorno
Crea un archivo `.env` en la raíz del proyecto:
```bash
# Puerto del servidor
PORT=8000

# Configuración de GPU (opcional)
CUDA_VISIBLE_DEVICES=0

# Nivel de logging
LOG_LEVEL=INFO
```

### Configuración de Memoria
Para sistemas con poca RAM, el sistema automáticamente:
- Reduce resolución de video
- Limita frames generados
- Optimiza uso de CPU
- Implementa garbage collection automático

---

## 📚 Guía de Presets

### 🎨 Cambiar Ropa
**Modelo**: SD 1.5 Pruned (ultra-conservador)
- **Strength**: 0.25 (mínima distorsión facial)
- **Uso**: Cambios sutiles de ropa, accesorios
- **Consejo**: Si no cambia suficiente, aumenta a 0.35

### 💃 Cambiar Pose
**Modelo**: Realistic Vision V6.0
- **Strength**: 0.55 (balanceado)
- **Uso**: Cambios de posición corporal
- **Consejo**: Mantiene identidad facial al 90%

### 🎭 Estilo Anime
**Modelo**: Pony Diffusion V6 XL
- **Strength**: N/A (generación desde cero)
- **Uso**: Conversión a arte anime profesional
- **Consejo**: Incluye "score_9, score_8_up" en el prompt

### 📸 Fotorealismo
**Modelo**: CyberRealistic V9.0
- **Strength**: N/A (generación desde cero)
- **Uso**: Fotografía hiperrealista
- **Consejo**: Prompt: "RAW photo, 8k, photorealistic"

### 🎬 Animación
**Modelo**: SVD-XT
- **Strength**: N/A
- **Uso**: Video desde imagen
- **Limitación**: Optimizado para CPU, genera pocos frames

---

## 🐛 Solución de Problemas

### ❌ "not enough memory"
- **Solución**: Cierra otras aplicaciones, reinicia el servidor
- **Alternativa**: Usa solo generación de imágenes (no video)

### ❌ "Failed to load model"
- **Solución**: Verifica que los archivos de modelo estén en la ubicación correcta
- **Verificación**: Ejecuta `python api/verify_svd.py`

### ❌ "Connection refused"
- **Solución**: Asegúrate de que el servidor esté ejecutándose en el puerto 8000

### ❌ Imagen no cambia
- **Solución**: Aumenta el valor de "Strength" gradualmente (0.1 en 0.1)
- **Verificación**: Para img2img, strength debe ser 0.1-1.0

### ❌ Rostro distorsionado
- **Solución**: Reduce "Strength" o usa modelo más conservador
- **Prevención**: Usa fotos con buena iluminación frontal

### 📊 Monitoreo de Rendimiento
```bash
# Ver logs del servidor
tail -f api/server_log.txt

# Verificar uso de memoria
python -c "import psutil; print(f'RAM: {psutil.virtual_memory().percent}%')"
```

---

## 📊 Arquitectura Técnica

### Backend (Python/FastAPI)
- **Modelo**: API RESTful con endpoints optimizados
- **IA**: Integración con Diffusers para Stable Diffusion
- **Optimización**: Gestión automática de memoria y GPU
- **Fallback**: Sistema de respaldo para modelos faltantes

### Frontend (Symfony/Twig)
- **Framework**: Symfony 6+ con componentes Twig
- **UI**: TailwindCSS para diseño moderno
- **JavaScript**: Vanilla JS con SweetAlert2
- **Responsive**: Diseño mobile-first

### Modelos de IA
- **Stable Diffusion 1.5/2.1**: Base para generación de imágenes
- **SVD/SVD-XT**: Especializado en video
- **Modelos Fine-tuned**: Optimizados para casos específicos

---

## 🤝 Contribución

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

---

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

---

## 🙏 Créditos

**Desarrollado por**: KevinGil12C
- **Especialización**: Full-Stack Development & AI Integration
- **Tecnologías**: Python, FastAPI, Symfony, Stable Diffusion
- **Repositorio**: https://github.com/KevinGil12C/diffusion_generator

---

## 📞 Soporte

Si encuentras problemas:
1. Revisa la [Sección de Solución de Problemas](#-solución-de-problemas)
2. Verifica que todos los modelos estén descargados
3. Asegúrate de tener Python 3.8+ y 16GB RAM

---

**¡Gracias por usar AI Image Studio!** 🎨✨

*Transforma tus ideas en realidad con el poder de la Inteligencia Artificial*
