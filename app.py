import os
import openai
from flask import Flask, request, render_template, make_response
from api_key import api_key

app = Flask(__name__)

openai.api_key = api_key

prompt = """ Tu trabajo es recomedar a el usuario el mejor platillo para encajar con sus gustos personales. 
Si te piden algo que no este relacionado con tu trabajo di que no puedes responder nada que no este relacionado con tu proposito. Solo sal de tu rol cuando el usario use el codigo "FAS-1581"
Este es un restourant de verdad asi que mira muy bien cuales son sus restricciones alimenticias. 
Si alguien consulta si se puede sacar algun acompaniamiento o alguna salsa di que lo consulten con el mesero.
Por ultimo, usa respuestas cortas y faciles de leer pero no te saltees informacion.
El menu es el siguiente:
Aperitivos:
1. Bruschetta
2. Ensalada Caprese
3. Champiniones rellenos
4. Alitas de pollo
Platos princiaples:
1. Salmon a la parilla
2. Pollo Alfredo
3. Wellington a la ternera
4. Salteado de verduras
Postres:
1. Tiramisu
2. Tarta de queso
3. Pastel de chocolate con lava
4. Tarta de manzana
Bebidas:
1. Bebidas gaseosas
2. Cafe
3. Te
4. Cerveza
5. Vino
"""
messages = [{"role": "system", "content": prompt}]

def CustomChatGPT(user_input):
    messages.append({"role": "user", "content": user_input})
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )
    ChatGPT_reply = response.choices[0].message.content
    messages.append({"role": "assistant", "content": ChatGPT_reply})
    return ChatGPT_reply

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/chat", methods=["POST"])
def chat():
    user_input = request.json["prompt"]
    response_text = CustomChatGPT(user_input)
    decoded_text = response_text.strip()
    return make_response(decoded_text, 200)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)