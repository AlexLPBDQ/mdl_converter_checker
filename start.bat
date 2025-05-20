@echo off
title Conversion de modèles .MDL vers Source Engine
cd /d "%~dp0"

echo [🔁] Lancement du script Python...
py mdl_converter.py

pause