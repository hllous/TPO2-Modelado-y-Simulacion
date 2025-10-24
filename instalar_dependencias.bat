@echo off
echo ============================================
echo   Instalador de Dependencias
echo   Sistemas Dinamicos 2D
echo ============================================
echo.
echo Instalando dependencias necesarias...
echo.

pip install -r requirements.txt

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ============================================
    echo   Instalacion completada exitosamente!
    echo ============================================
    echo.
    echo Ahora puede ejecutar el programa usando:
    echo     ejecutar_gui.bat
    echo.
    echo O directamente:
    echo     python sistemas_dinamicos_gui.py
    echo.
) else (
    echo.
    echo ERROR: Hubo un problema durante la instalacion.
    echo Verifique que pip este instalado correctamente.
    echo.
)

pause
