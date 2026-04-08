import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
 # Mantenemos el nombre de la clase para que server.py no se entere del cambio
class GeminiAgent:
    def __init__(self):
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError("No se encontró GROQ_API_KEY en el archivo .env")
        
        self.client = Groq(api_key=api_key)
        # Este es uno de los modelos más potentes y gratuitos de Groq
        self.model_name = "llama-3.3-70b-versatile"

    def get_response(self, user_input):
        try:
            completion = self.client.chat.completions.create(
                model=self.model_name,
                messages=[
                    {"role": "system", "content": "Eres un asistente técnico experto y conciso. Hablas español argentino si el usuario te habla así."},
                    {"role": "user", "content": user_input}
                ],
                temperature=0.7,
            )
            return completion.choices[0].message.content
        except Exception as e:
            print(f"Error en Groq: {e}")
            return "Che, Groq también se puso la gorra. Probá en un ratito."