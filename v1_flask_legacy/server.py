import os
from flask import Flask, request, jsonify, render_template
from grok_agent import GeminiAgent

app = Flask(__name__)

# Inicializamos el agente
# Aunque el archivo se llame grok_agent.py, la clase adentro se llama GeminiAgent
ia_agent = GeminiAgent()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data.get('message')

    if not user_message:
        return jsonify({"response": "No enviaste ningún mensaje."}), 400

    # Llamamos al método que creamos en tu grok_agent.py
    response_text = ia_agent.get_response(user_message)

    return jsonify({"response": response_text})

if __name__ == '__main__':
    # Configuración para que funcione tanto local como en la nube
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)