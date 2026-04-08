# main.py
from dotenv import load_dotenv
from coder_agent import Agent

load_dotenv()

print("Iniciando agente de IA (Ollama)")

agent = Agent(model="qwen2.5:7b")  # cambia el modelo si querés

while True:
    user_input = input("Tú: ").strip()

    if not user_input:
        continue

    if user_input.lower() in ("salir", "exit", "bye", "sayonara"):
        print("Hasta luego!")
        break

    # Agregar mensaje del usuario al historial
    agent.messages.append({"role": "user", "content": user_input})

    # Loop agentico: seguir llamando mientras haya tool calls
    while True:
        response = agent.client.chat(
            model=agent.model,
            messages=agent.messages,
            tools=agent.tools
        )

        called_tool = agent.process_response(response)

        # Si no se llamó herramienta, tenemos la respuesta final
        if not called_tool:
            break