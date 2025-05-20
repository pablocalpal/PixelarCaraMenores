from flask import Flask, request, jsonify, Response
import requests
from io import BytesIO
import cv2
import numpy as np
import json


app = Flask(__name__)


# URLs de los otros contenedores Docker
URL_BOUNDING = "http://bounding:5001/detectar_caras"
URL_CLASIFICACION = "http://clasificacion:5002/menores"
URL_PIXELADO = "http://pixelado:5000/pixelar"


@app.route("/", methods=["GET"])
def inicio():
    return jsonify({"message": "API Engine operativa"}), 200


@app.route("/procesar", methods=["POST"])
def procesar():
    if 'imagen' not in request.files:
        return jsonify({"error": "No se ha enviado ninguna imagen"}), 400

    imagen = request.files['imagen']
    imagen_bytes = imagen.read()  # Leer toda la imagen una sola vez
    imagen_np = cv2.imdecode(np.frombuffer(imagen_bytes, np.uint8), cv2.IMREAD_COLOR)

    if imagen_np is None:
        return jsonify({"error": "No se pudo procesar la imagen"}), 400

    try:
        # Paso 1: Bounding box
        res_bounding = requests.post(
            URL_BOUNDING,
            files={'imagen': (imagen.filename, BytesIO(imagen_bytes), imagen.mimetype)}
        )
        if res_bounding.status_code != 200:
            return jsonify({"error": "Error en bounding box", "detalle": res_bounding.text}), 500

        bounding_json = res_bounding.json()
        detecciones = bounding_json.get("detecciones", [])

        # Paso 2: Recortar cada bounding box y convertir a imagen
        imagenes_caras = []
        for i, face in enumerate(detecciones):
            x1, y1, x2, y2 = face["bbox"]
            cropped = imagen_np[y1:y2, x1:x2]
            _, buffer = cv2.imencode('.jpg', cropped)
            face_bytes = BytesIO(buffer.tobytes())
            face_bytes.name = f"cara_{i}.jpg"
            imagenes_caras.append(('imagenes', (face_bytes.name, face_bytes, 'image/jpeg')))

        # Paso 2: Clasificación
        res_clasificacion = requests.post(
            URL_CLASIFICACION,
            files=imagenes_caras
        )
        
        if res_clasificacion.status_code != 200:
            return jsonify({"error": "Error en clasificación", "detalle": res_clasificacion.text}), 500

        menores = res_clasificacion.json()  # lista de 0 y 1

        # Filtrar bboxes para los que son menores
        menores_bboxes = []
        for d, es_menor in zip(detecciones, menores):
            if es_menor == 1:
                x1, y1, x2, y2 = d["bbox"]
                x = x1
                y = y1
                w = x2 - x1
                h = y2 - y1
                menores_bboxes.append([x, y, w, h])

        # Paso 3: Pixelado
        res_pixelado = requests.post(
            URL_PIXELADO,
            files={'imagen': (imagen.filename, BytesIO(imagen_bytes), imagen.mimetype)},
            data={'rectangulos': json.dumps(menores_bboxes)}
        )
        if res_pixelado.status_code != 200:
            return jsonify({"error": "Error en pixelado", "detalle": res_pixelado.text}), 500

        return Response(res_pixelado.content, content_type='image/jpeg')

    except Exception as e:
        return jsonify({"error": "Error inesperado", "detalle": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5003)
