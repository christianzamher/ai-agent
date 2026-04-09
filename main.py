from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from grok_agent import GeminiAgent
import uvicorn
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Mandria Bot API")

# 🛠️ Configuramos los archivos estáticos y templates
app.mount("/static", StaticFiles(directory="static"), name="static")

# 🕷️ Configuramos CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
templates = Jinja2Templates(directory="templates")

agente = GeminiAgent()

@app.get("/")
async def home(request: Request):
    # Esto le dice a FastAPI que renderice el HTML que vamos a crear
    return templates.TemplateResponse(request=request, name="index.html")


historiales = {} 

@app.get("/preguntar")
async def preguntar(query: str):
    session_id = "usuario_unico"
    
    if session_id not in historiales:
        historiales[session_id] = []

    # 🧠 SUPERPODER: El Contexto Silencioso
    # En lugar de sumarlo todo al query, armamos un bloque de contexto
    contexto = "\n".join(historiales[session_id])
    
    # Le mandamos al agente la pregunta LIMPIA (query) 
    # pero le pasamos el contexto aparte si tu GeminiAgent lo permite,
    # o armamos un System Prompt mejorado.
    
    instruccion_con_memoria = f"""
    Contexto de la charla previa:
    {contexto}
    
    Pregunta actual del usuario: {query}
    """

    # Aquí está el truco: le pedimos la respuesta pasándole la instrucción.
    # Pero para que NO use Tavily con todo ese texto, 
    # Gemini debe decidir qué parte es la pregunta real.
    respuesta = agente.get_response(instruccion_con_memoria) 

    # Guardamos solo lo importante en el historial para no inflarlo
    historiales[session_id].append(f"U: {query}")
    historiales[session_id].append(f"M: {respuesta[:100]}...") # Guardamos un resumen
    historiales[session_id] = historiales[session_id][-6:] # Bajamos a 6 para no saturar

    return {"respuesta": respuesta}

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)