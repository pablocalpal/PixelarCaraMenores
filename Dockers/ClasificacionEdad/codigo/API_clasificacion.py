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
    Endpoint para clasificar imágenes de caras de personas. Utiliza un modelo entrenado para predecir la edad y devuelve un array de booleanos según si la edad predicha es menor de 18 años.
    :return: Array de booleanos
    """
    try:
        # Verificar si se han enviado archivos
        if 'imagenes' not in request.files:
            return jsonify({"error": "No se han proporcionado imágenes."}), 400

        # Cargar el modelo
        try:
            model = load_model("./modelo.keras")
        except Exception as e:
            return jsonify({"error": "Error al cargar el modelo.", "detalle": str(e)}), 500

        # Leer las imágenes
        archivos = request.files.getlist("imagenes")
        resultados = []

        for archivo in archivos:
            # Verificar si el archivo tiene nombre
            if archivo.filename == '':
                resultados.append(False)
                continue

            # Validar extensión del archivo
            if not allowed_file(archivo.filename):
                resultados.append(False)
                continue

            try:
                # Leer la imagen en formato numpy array
                file_bytes = np.frombuffer(archivo.read(), np.uint8)
                image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

                if image is None:
                    resultados.append(False)
                    continue

                # Redimensionar y normalizar correctamente
                resized = cv2.resize(image, (64, 64))  # Cambiar a 64x64 para coincidir con el modelo
                normalized = resized / 255.0  # Normalización única

                # Agregar dimensión de lote (batch) sin aplanar
                input_data = np.expand_dims(normalized, axis=0)  # Forma resultante: (1, 64, 64, 3)

                # Realizar predicción
                prediccion = model.predict(input_data)
                
                
                
                edad_predicha = prediccion[0][0]

                # Añadir resultado al array
                resultados.append(edad_predicha < 18)

            except Exception as e:
                        return jsonify({
                        "error": "Error al procesar imagen.",
                        "detalle": str(e)
                    }), 500

        return jsonify([int(r) for r in resultados]), 200 # Convertir booleanos a enteros (0 o 1) para que jsonify los acepte

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