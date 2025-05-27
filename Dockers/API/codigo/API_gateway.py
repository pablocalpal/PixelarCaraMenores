from flask import Flask, request, jsonify
import requests
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Habilita CORS para todos los dominios

ENGINE_URL = "http://engine:5003/procesar"
ALLOWED_IMAGE_TYPES = {
    "image/jpeg", "image/png", "image/jpg",
    "image/bmp", "image/gif", "image/webp"
}

@app.route("/pixelar_menores", methods=["POST"])
def upload_image():
    if 'file' not in request.files:
        return jsonify({"error": "No se ha enviado ninguna imagen"}), 400

    file = request.files['file']
    if file.content_type not in ALLOWED_IMAGE_TYPES:
        return jsonify({
            "error": f"Tipo de archivo no permitido: {file.content_type}. "
                     "Use PNG, JPG, JPEG, BMP, GIF o WEBP."
        }), 400

    # Verificar si está activado el modo debug
    debug_mode = request.form.get('debug', 'false').lower() == 'true'

    try:
        if debug_mode:
            res = requests.post(
                ENGINE_URL,
                files={"imagen": (file.filename, file.read(), file.content_type)},
                data={"debug": "true"},
                timeout=30
            )
        else:
            res = requests.post(
                ENGINE_URL,
                files={"imagen": (file.filename, file.read(), file.content_type)},
                timeout=30
            )
        res.raise_for_status()
        return res.content, res.status_code, {'Content-Type': res.headers.get('Content-Type', 'application/json')}
    except Exception as e:
        return jsonify({"error": "Error al contactar con el motor", "detalle": str(e)}), 500

@app.route("/", methods=["GET"])
def health():
    return jsonify({"status": "Public API operativa"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
