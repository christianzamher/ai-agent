@echo off
title Chatbot Multi-Agent Local
echo ==========================================
echo   PREPARANDO EL ENTORNO (GROQ + FLASK)
echo ==========================================

:: Instalamos groq y mantenemos flask y dotenv
.\env\Scripts\python.exe -m pip install flask groq python-dotenv

echo.
echo ==========================================
echo   LANZANDO SERVIDOR EN http://127.0.0.1:5000
echo ==========================================
echo.

.\env\Scripts\python.exe server.py
pause