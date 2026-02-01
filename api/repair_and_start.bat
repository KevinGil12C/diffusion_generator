@echo off
cd /d "%~dp0"
echo ===================================================
echo   REPARACION DEL SISTEMA - DIFFUSION GENERATOR
echo ===================================================
echo.

echo [1/4] Deteniendo todos los procesos de Python...
taskkill /F /IM python.exe 2>nul
taskkill /F /IM uvicorn.exe 2>nul
echo.

echo [2/4] Activando entorno virtual...
if exist "venv\Scripts\activate.bat" (
    call venv\Scripts\activate.bat
) else (
    echo ERROR: No se encontro venv.
    pause
    exit /b
)

echo.
echo [3/4] Reinstalando librerias criticas (Esto puede tardar unos minutos)...
echo Por favor espera y no cierres la ventana...
pip install --upgrade diffusers transformers accelerate omegaconf safetensors peft

echo.
echo [4/4] Iniciando el servidor...
python main.py
pause
