# 🎻 Mandria Bot - Agente Tanguero con IA

Un asistente inteligente desarrollado para la comunidad del **ETI (Encuentro Tanguero del Interior)**, combinando la potencia de **FastAPI** con una interfaz enfocada en la accesibilidad y el folklore rioplatense.

## 🚀 Características Principales
* **Interfaz Inspirada en ETI**: Diseño visual basado en la estética de ETI Ushuaia.
* **Accesibilidad Inteligente**: 
    * Soporte de **Speech-to-Text** (micrófono) para usuarios con dificultades motrices o músicos con las manos ocupadas.
    * Respuesta automática por **Voz (Text-to-Speech)** con acento argentino (`es-AR`) cuando se usa el micrófono.
* **Lógica de QA**: Implementación de manejo de errores ("Se me cortó una cuerda") y limpieza de buffers de audio.

## 🛠️ Tech Stack
* **Backend**: FastAPI (Python 3.10+).
* **IA**: Integración con modelos de lenguaje para respuestas con personalidad tanguera.
* **Frontend**: HTML5, CSS3 (Custom Properties) y Vanilla JavaScript (Web Speech API).

## 📦 Instalación
1. Clonar el repo.
2. Crear un entorno virtual: `python -m venv venv`.
3. Instalar dependencias: `pip install -r requirements.txt`.
4. Configurar tu `.env` con las API Keys necesarias.