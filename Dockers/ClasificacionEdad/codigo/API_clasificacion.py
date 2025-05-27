from flask import Flask, jsonify, request
import numpy as np
import cv2
from keras.models import load_model
import json

# Create the Flask application
app = Flask(__name__)

# Allowed image file extensions
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    """
    Comprueba que el archivo subido sea compatible para la detección de caras (que sea imagen).
    
    :param filename: Nombre del archivo subido
    :return: Booleano, True si el archivo es permitido, False en caso contrario
    """
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def validate_image(file):
    """
    Valida la imagen antes de la detección de caras.
    
    :param file: Archivo de imagen a validar
    :raises ValueError: Si la imagen no es válida
    """
    # Verificar tamaño máximo (por ejemplo, 10MB)
    file.seek(0, 2)  # Mover al final del archivo
    file_size = file.tell()
    file.seek(0)  # Reiniciar puntero de archivo
    
    if file_size > 10 * 1024 * 1024:  # 10MB
        raise ValueError("El tamaño del archivo excede el límite de 10MB")
    
    # Intentar abrir la imagen para validarla
    try:
        # Use OpenCV to read and validate the image
        img_bytes = file.read()
        file.seek(0)  # Reset file pointer
        img_np = cv2.imdecode(np.frombuffer(img_bytes, np.uint8), cv2.IMREAD_COLOR)
        
        if img_np is None or img_np.size == 0:
            raise ValueError("No se puede leer la imagen")
        
    except Exception as e:
        raise ValueError(f"Archivo de imagen no válido: {str(e)}")

@app.route("/menores", methods=["POST"])
def detectar_menores():
    """
    Endpoint para clasificar imágenes de caras de personas. Utiliza un modelo entrenado para predecir si una persona es menor de 18 años.
    :return: Array de booleanos (convertidos a 0/1 para facilitar interpretación) o información detallada si debug=true
    """
    try:
        # Verificar si se han enviado archivos
        if 'imagenes' not in request.files:
            return jsonify({"error": "No se han proporcionado imágenes."}), 400

        # Verificar si está activado el modo debug
        debug_mode = request.form.get('debug', 'false').lower() == 'true'

        # Cargar el modelo
        try:
            model = load_model("./modelo.keras")
        except Exception as e:
            return jsonify({"error": "Error al cargar el modelo.", "detalle": str(e)}), 500

        # Leer las imágenes
        archivos = request.files.getlist("imagenes")
        resultados = []
        resultados_detalle = []

        for i, archivo in enumerate(archivos):
            if archivo.filename == '':
                resultado_simple = 0
                resultado_detallado = {
                    "imagen_id": i,
                    "probabilidad": 0.0,
                    "es_menor": False,
                    "error": "Archivo vacío"
                }
                resultados.append(resultado_simple)
                resultados_detalle.append(resultado_detallado)
                continue

            if not allowed_file(archivo.filename):
                resultado_simple = 0
                resultado_detallado = {
                    "imagen_id": i,
                    "probabilidad": 0.0,
                    "es_menor": False,
                    "error": "Tipo de archivo no permitido"
                }
                resultados.append(resultado_simple)
                resultados_detalle.append(resultado_detallado)
                continue

            try:
                validate_image(archivo)

                file_bytes = np.frombuffer(archivo.read(), np.uint8)
                image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

                if image is None:
                    resultado_simple = 0
                    resultado_detallado = {
                        "imagen_id": i,
                        "probabilidad": 0.0,
                        "es_menor": False,
                        "error": "No se pudo decodificar la imagen"
                    }
                    resultados.append(resultado_simple)
                    resultados_detalle.append(resultado_detallado)
                    continue

                resized = cv2.resize(image, (64, 64))
                normalized = resized / 255.0
                input_data = np.expand_dims(normalized, axis=0)

                # Predicción binaria directamente del modelo
                prediccion = model.predict(input_data)
                probabilidad_raw = float(prediccion[0][0])
                
                # Umbral de 0.6 para clasificar como menor
                es_menor = probabilidad_raw < 0.6
                resultado_simple = int(es_menor)
                
                resultado_detallado = {
                    "imagen_id": i,
                    "probabilidad": probabilidad_raw,
                    "es_menor": es_menor,
                    "confianza": abs(probabilidad_raw - 0.6),  # Qué tan lejos está del umbral
                    "umbral_usado": 0.6
                }
                
                resultados.append(resultado_simple)
                resultados_detalle.append(resultado_detallado)

            except Exception as e:
                resultado_simple = 0
                resultado_detallado = {
                    "imagen_id": i,
                    "probabilidad": 0.0,
                    "es_menor": False,
                    "error": f"Error al procesar imagen: {str(e)}"
                }
                resultados.append(resultado_simple)
                resultados_detalle.append(resultado_detallado)

        # Retornar respuesta según el modo
        if debug_mode:
            return jsonify({
                "resultados": resultados,
                "detalle": resultados_detalle,
                "debug": True,
                "total_imagenes": len(archivos),
                "menores_detectados": sum(resultados)
            }), 200
        else:
            return jsonify(resultados), 200

    except Exception as e:
        return jsonify({
            "error": "Error interno del servidor.",
            "detalle": str(e)
        }), 500


@app.route("/", methods=["GET"])
def inicio():
    """
    Endpoint de verificación.
    
    :return: Respuesta JSON indicando que la API está operativa
    """
    return jsonify({
        "message": "API de Detección Facial operativa",
    }), 200



# Configuración de la aplicación Flask
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB tamaño máximo de carga

if __name__ == "__main__":
    # Ejecutar la aplicación
    app.run(host="0.0.0.0", port=5002, debug=False)