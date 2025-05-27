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


def dibujar_debug_image(imagen_np, detecciones, predicciones_detalle):
    """
    Dibuja bounding boxes con información de debug en la imagen
    """
    imagen_debug = imagen_np.copy()
    
    for i, (deteccion, prediccion) in enumerate(zip(detecciones, predicciones_detalle)):
        x1, y1, x2, y2 = deteccion["bbox"]
        probabilidad = prediccion["probabilidad"]
        es_menor = prediccion["es_menor"]
        
        # Color del bounding box: rojo si es menor, verde si no
        color = (0, 0, 255) if es_menor else (0, 255, 0)  # BGR format
        
        # Dibujar rectángulo
        cv2.rectangle(imagen_debug, (x1, y1), (x2, y2), color, 2)
        
        # Texto con información
        texto = f"P: {probabilidad:.3f}"
        etiqueta = "MENOR" if es_menor else "ADULTO"
        
        # Fondo para el texto
        (text_width, text_height), _ = cv2.getTextSize(texto, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)
        (label_width, label_height), _ = cv2.getTextSize(etiqueta, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 2)
        
        # Rectángulo de fondo para probabilidad
        cv2.rectangle(imagen_debug, (x1, y1 - text_height - 10), 
                     (x1 + text_width + 10, y1), color, -1)
        
        # Rectángulo de fondo para etiqueta
        cv2.rectangle(imagen_debug, (x1, y2), 
                     (x1 + label_width + 10, y2 + label_height + 10), color, -1)
        
        # Texto blanco
        cv2.putText(imagen_debug, texto, (x1 + 5, y1 - 5), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        cv2.putText(imagen_debug, etiqueta, (x1 + 5, y2 + label_height + 5), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
    
    return imagen_debug


@app.route("/procesar", methods=["POST"])
def procesar():
    if 'imagen' not in request.files:
        return jsonify({"error": "No se ha enviado ninguna imagen"}), 400

    imagen = request.files['imagen']
    imagen_bytes = imagen.read()  # Leer toda la imagen una sola vez
    imagen_np = cv2.imdecode(np.frombuffer(imagen_bytes, np.uint8), cv2.IMREAD_COLOR)

    if imagen_np is None:
        return jsonify({"error": "No se pudo procesar la imagen"}), 400

    # Verificar si está activado el modo debug
    debug_mode = request.form.get('debug', 'false').lower() == 'true'

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

        # Si no hay detecciones, devolver imagen original
        if not detecciones:
            if debug_mode:
                # Devolver imagen original con mensaje de "no faces detected"
                imagen_debug = imagen_np.copy()
                cv2.putText(imagen_debug, "No faces detected", (50, 50), 
                           cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                _, buffer = cv2.imencode('.jpg', imagen_debug)
                return Response(buffer.tobytes(), content_type='image/jpeg')
            else:
                return Response(imagen_bytes, content_type='image/jpeg')

        # Paso 2: Recortar cada bounding box y convertir a imagen
        imagenes_caras = []
        for i, face in enumerate(detecciones):
            x1, y1, x2, y2 = face["bbox"]
            cropped = imagen_np[y1:y2, x1:x2]
            _, buffer = cv2.imencode('.jpg', cropped)
            face_bytes = BytesIO(buffer.tobytes())
            face_bytes.name = f"cara_{i}.jpg"
            imagenes_caras.append(('imagenes', (face_bytes.name, face_bytes, 'image/jpeg')))

        # Paso 2: Clasificación (con información detallada si es debug)
        clasificacion_data = {'debug': 'true' if debug_mode else 'false'}
        
        res_clasificacion = requests.post(
            URL_CLASIFICACION,
            files=imagenes_caras,
            data=clasificacion_data
        )
        
        if res_clasificacion.status_code != 200:
            return jsonify({"error": "Error en clasificación", "detalle": res_clasificacion.text}), 500

        clasificacion_json = res_clasificacion.json()
        
        # Si es modo debug, devolver imagen con bounding boxes anotados
        if debug_mode:
            if isinstance(clasificacion_json, dict) and 'detalle' in clasificacion_json:
                predicciones_detalle = clasificacion_json['detalle']
                imagen_debug = dibujar_debug_image(imagen_np, detecciones, predicciones_detalle)
                _, buffer = cv2.imencode('.jpg', imagen_debug)
                return Response(buffer.tobytes(), content_type='image/jpeg')
            else:
                # Fallback si la API de clasificación no soporta modo debug
                menores = clasificacion_json if isinstance(clasificacion_json, list) else []
                predicciones_detalle = []
                for i, es_menor in enumerate(menores):
                    predicciones_detalle.append({
                        "probabilidad": 0.5,  # Valor por defecto
                        "es_menor": bool(es_menor)
                    })
                imagen_debug = dibujar_debug_image(imagen_np, detecciones, predicciones_detalle)
                _, buffer = cv2.imencode('.jpg', imagen_debug)
                return Response(buffer.tobytes(), content_type='image/jpeg')

        # Modo normal: proceder con pixelado
        menores = clasificacion_json if isinstance(clasificacion_json, list) else clasificacion_json.get('resultados', [])

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