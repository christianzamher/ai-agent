# agent.py
import os
import json
from ollama import Client

class Agent:
    def __init__(self, model="phi3:3.8b", host="http://localhost:11434"):
        self.client = Client(host=host)
        self.model = model
        self.messages = [
    {"role": "system", "content": """Eres un asistente útil que habla español y eres muy conciso con tus respuestas.
IMPORTANTE: Solo usa herramientas cuando el usuario lo pida explícitamente.
Nunca uses edit_file, read_file o list_files_in_dir en respuesta a saludos, agradecimientos o conversación general."""}
]
        self.setup_tools()

    def setup_tools(self):
        self.tools = [
            {
                "type": "function",
                "function": {
                    "name": "list_files_in_dir",
                    "description": "Lista los archivos que existen en un directorio dado (por defecto es el directorio actual)",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "directory": {
                                "type": "string",
                                "description": "Directorio para listar (opcional). Por defecto es el directorio actual"
                            }
                        },
                        "required": []
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "read_file",
                    "description": "Lee el contenido de un archivo en una ruta especificada",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "path": {
                                "type": "string",
                                "description": "La ruta del archivo a leer"
                            }
                        },
                        "required": ["path"]
                    }
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "edit_file",
                    "description": "Edita el contenido de un archivo reemplazando prev_text por new_text. Crea el archivo si no existe.",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "path": {
                                "type": "string",
                                "description": "La ruta del archivo a editar"
                            },
                            "prev_text": {
                                "type": "string",
                                "description": "El texto que se va a buscar para reemplazar (puede ser vacío para archivos nuevos)"
                            },
                            "new_text": {
                                "type": "string",
                                "description": "El texto que reemplazará a prev_text (o el texto para un archivo nuevo)"
                            }
                        },
                        "required": ["path", "new_text"]
                    }
                }
            }
        ]

    def list_files_in_dir(self, directory="."):
        print("  ⚙️ Herramienta llamada: list_files_in_dir")
        try:
            files = os.listdir(directory)
            return {"files": files}
        except Exception as e:
            return {"error": str(e)}

    def read_file(self, path):
        print("  ⚙️ Herramienta llamada: read_file")
        try:
            with open(path, encoding="utf-8") as f:
                return f.read()
        except Exception as e:
            err = f"Error al leer el archivo {path}"
            print(err)
            return err

    def edit_file(self, path, new_text, prev_text=""):
        print("  ⚙️ Herramienta llamada: edit_file")
        try:
            existed = os.path.exists(path)
            if existed and prev_text:
                content = self.read_file(path)
                if prev_text not in content:
                    return f"Texto '{prev_text}' no encontrado en el archivo"
                content = content.replace(prev_text, new_text)
            else:
                dir_name = os.path.dirname(path)
                if dir_name:
                    os.makedirs(dir_name, exist_ok=True)
                content = new_text

            with open(path, "w", encoding="utf-8") as f:
                f.write(content)

            action = "editado" if existed and prev_text else "creado"
            return f"Archivo {path} {action} exitosamente"
        except Exception as e:
            err = f"Error al crear o editar el archivo {path}"
            print(err)
            return err

    def process_response(self, response):
        """
        Procesa la respuesta de Ollama.
        Retorna True si se llamó una herramienta, False si es respuesta final.
        """
        message = response.message

        # Guardar el mensaje del asistente en el historial
        self.messages.append({"role": "assistant", "content": message.content, "tool_calls": message.tool_calls})

        if message.tool_calls:
            for tool_call in message.tool_calls:
                fn_name = tool_call.function.name
                args = tool_call.function.arguments

                print(f"  - El modelo considera llamar a la herramienta: {fn_name}")
                print(f"  - Argumentos: {args}")

                if fn_name == "list_files_in_dir":
                    result = self.list_files_in_dir(**args)
                elif fn_name == "read_file":
                    result = self.read_file(**args)
                elif fn_name == "edit_file":
                    path = args.get("path", "")
                    new_text = args.get("new_text", "").strip()

                    if not new_text:
                        print("  ⚠️ edit_file bloqueado: new_text vacío")
                        result = "Operación cancelada"
                    elif os.path.exists(path) and not any(c in new_text for c in ["<", "{", "def ", "import ", "\n"]):
                        print("  ⚠️ edit_file bloqueado: new_text parece texto conversacional, no código")
                        result = "Operación cancelada: el contenido no parece código"
                    else:
                        result = self.edit_file(**args)
                else:
                    result = f"Herramienta '{fn_name}' no encontrada"

                # Agregar resultado de la herramienta al historial
                self.messages.append({
                    "role": "tool",
                    "content": json.dumps(result, ensure_ascii=False)
                })

            return True  # Se llamó al menos una herramienta

        # Respuesta final de texto
        reply = message.content or ""
        print(f"Asistente: {reply}")
        return False