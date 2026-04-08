import os
import json
from groq import Groq
from tavily import TavilyClient
from dotenv import load_dotenv

load_dotenv()

class GeminiAgent:
    def __init__(self):
        # Cargamos las dos llaves
        self.groq_api_key = os.getenv("GROQ_API_KEY")
        self.tavily_api_key = os.getenv("TAVILY_API_KEY")
        
        if not self.groq_api_key or not self.tavily_api_key:
            raise ValueError("Faltan APIs en el .env (GROQ o TAVILY)")
        
        self.client = Groq(api_key=self.groq_api_key)
        self.tavily = TavilyClient(api_key=self.tavily_api_key)
        self.model_name = "llama-3.3-70b-versatile"

    def _web_search(self, query):
        """Función interna para buscar en internet"""
        try:
            # Buscamos y traemos un resumen del contenido
            search_result = self.tavily.search(query=query, search_depth="advanced", max_results=3)
            context = ""
            for res in search_result['results']:
                context += f"\nFuente: {res['url']}\nContenido: {res['content']}\n"
            return context
        except Exception as e:
            return f"Error buscando en la web: {e}"

    def get_response(self, user_input):
        try:
            # PASO 1: El bot recibe la consulta y decide si necesita internet
            # Le pasamos un system prompt que lo obligue a usar el contexto si se lo damos
            messages = [
                {
                    "role": "system", 
                    "content": "Eres un asistente experto. Si el usuario te pregunta algo de actualidad o que no sabes, utiliza la información de búsqueda que se te proporcionará. Hablas español argentino."
                }
            ]

            # PASO 2: Hacemos una búsqueda rápida con Tavily SIEMPRE o bajo lógica (aquí lo hacemos directo para asegurar éxito)
            print(f"Investigando en la web para: {user_input}...")
            contexto_web = self._web_search(user_input)

            # PASO 3: Armamos el prompt final con la info de internet
            prompt_final = f"""
            Basándote en esta información de internet:
            {contexto_web}
            
            Responde a la siguiente pregunta del usuario:
            {user_input}
            """
            
            messages.append({"role": "user", "content": prompt_final})

            completion = self.client.chat.completions.create(
                model=self.model_name,
                messages=messages,
                temperature=0.6,
            )
            return completion.choices[0].message.content
            
        except Exception as e:
            print(f"Error: {e}")
            return "Che, se me cruzaron los cables con la búsqueda. Reintentá."