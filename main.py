import os
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

# Importamos tu lógica de IA
from grok_agent import GeminiAgent

app = FastAPI(title="Mandria Bot API")

# 🛠️ CONFIGURACIÓN DE RUTAS ABSOLUTAS (Para evitar el Not Found en Render)
base_path = os.path.dirname(os.path.abspath(__file__))
static_path = os.path.join(base_path, "static")
templates_path = os.path.join(base_path, "templates")

# Montamos los archivos estáticos (CSS, imágenes)
app.mount("/static", StaticFiles(directory=static_path), name="static")

# Configuramos el motor de templates
templates = Jinja2Templates(directory=templates_path)

# 🕷️ CONFIGURACIÓN DE CORS (Esencial para audio y fetch)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inicializamos al bardo del agente
agente = GeminiAgent()

# Diccionario para la memoria de la charla
historiales = {}

# --- RUTAS ---

@app.get("/")
async def home(request: Request):
    """Ruta principal que sirve la interfaz web"""
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/health")
async def health():
    """Ruta para que Render sepa que el bot está vivo"""
    return {"status": "El Mandria está en el bar y tiene ginebra", "port": os.environ.get("PORT")}

@app.get("/preguntar")
async def preguntar(query: str):
    """Ruta de procesamiento de mensajes con historial"""
    session_id = "usuario_unico" # Podrías cambiarlo por una IP o ID de sesión más adelante
    
    if session_id not in historiales:
        historiales[session_id] = []

    # Construimos el contexto con los últimos mensajes
    contexto = "\n".join(historiales[session_id])
    
    instruccion_con_memoria = f"""
    Contexto de la charla previa:
    {contexto}
    
    Pregunta actual del usuario: {query}
    """

    # Obtenemos la respuesta de tu GeminiAgent
    respuesta = agente.get_response(instruccion_con_memoria) 

    # Actualizamos historial (mantenemos solo lo último para no saturar)
    historiales[session_id].append(f"U: {query}")
    historiales[session_id].append(f"M: {respuesta[:150]}...") 
    historiales[session_id] = historiales[session_id][-6:] 

    return {"respuesta": respuesta}

if __name__ == "__main__":
    # Configuración dinámica de puerto para despliegue
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)