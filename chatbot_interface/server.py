from flask import Flask, request, jsonify, render_template
from cloud_agent import Agent 

app = Flask(__name__)

# Inicializamos el agente fuera de las rutas para que persista la sesión
# Usamos qwen2.5:7b como en tu main.py
ia_agent = Agent(model="qwen2.5:7b") 

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data.get('message', '').strip()
    
    if not user_message:
        return jsonify({'response': "No enviaste ningún mensaje."})

    # 1. Agregamos el mensaje del usuario al historial del agente
    ia_agent.messages.append({"role": "user", "content": user_message})

    # 2. Ejecutamos el loop agéntico 
    while True:
        response = ia_agent.client.chat(
            model=ia_agent.model,
            messages=ia_agent.messages,
            tools=ia_agent.tools
        )

        # process_response maneja las herramientas y guarda los mensajes
        called_tool = ia_agent.process_response(response)

        if not called_tool:
            # Si no hay más herramientas, la respuesta final está en el último mensaje
            final_reply = ia_agent.messages[-1]['content']
            break
    
    return jsonify({'response': final_reply})

if __name__ == '__main__':
    app.run(debug=True)