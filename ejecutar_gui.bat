@echo off
echo ============================================
echo   Sistemas Dinamicos 2D - Interfaz Grafica
echo ============================================
echo.
echo Iniciando aplicacion...
echo.

python sistemas_dinamicos_gui.py

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo ERROR: No se pudo ejecutar el programa.
    echo Verifique que Python este instalado y las dependencias esten disponibles.
    echo.
    echo Para instalar dependencias, ejecute:
    echo     pip install -r requirements.txt
    echo.
    pause
)
