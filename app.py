from flask import Flask, render_template, request, jsonify

from schemas import validar_pregunta
from services.tutor_service import responder_pregunta

app = Flask(__name__)


@app.route("/")
def inicio():
    return render_template("index.html")


@app.route("/preguntar", methods=["POST"])
def preguntar():
    pregunta, error = validar_pregunta(request.get_json(silent=True))
    if error:
        return jsonify({"error": error}), 400

    try:
        respuesta = responder_pregunta(pregunta)
    except Exception as e:
        print("Error al responder:", e)  # el detalle se ve en la terminal
        return jsonify({"error": "No pude generar la respuesta. Intenta de nuevo."}), 500

    return jsonify({"respuesta": respuesta})


if __name__ == "__main__":
    app.run(debug=True)