@echo off
cd /d "%~dp0"
echo ===================================================
echo      Diffusion Generator - Backend Launcher
echo ===================================================
echo.

echo [1/3] Limpiando procesos antiguos...
:: Matar procesos en puerto 8000
for /f "tokens=5" %%a in ('netstat -aon ^| findstr :8000') do (
    echo Matando proceso en puerto 8000 PID: %%a...
    taskkill /F /PID %%a 2>nul
)

:: Matar otros procesos de python que esten corriendo main.py (opcional pero recomendado)
taskkill /F /IM python.exe 2>nul

echo.
echo [2/3] Iniciando entorno virtual...
if exist "venv\Scripts\activate.bat" (
    call venv\Scripts\activate.bat
) else (
    echo ERROR: No se encontro el entorno virtual en venv\Scripts\activate.bat
    pause
    exit /b
)

echo.
echo [2.5/3] Verificando dependencias criticas...
pip install diffusers safetensors omegaconf transformers accelerate --quiet


echo.
echo [3/3] Ejecutando servidor FastAPI...
echo El servidor estara disponible en http://127.0.0.1:8000
echo.
python main.py

echo.
echo El servidor se ha detenido.
pause
