from flask import Flask, jsonify, request
import numpy as np
import cv2
from retinaface import RetinaFace
from io import BytesIO
from PIL import Image
import werkzeug

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

@app.route("/detectar_caras", methods=["POST"])
def detectar_caras():
    """
    Endpoint para el bounding de caras.
    
    :return: Respuesta JSON con un array de coordenadas de las caras detectadas
    """
    try:
        # Verificar si se ha enviado un archivo
        if 'imagen' not in request.files:
            return jsonify({"error": "No se ha proporcionado ninguna imagen."}), 400

        file = request.files['imagen']
        
        # Verificar si el archivo tiene nombre
        if file.filename == '':
            return jsonify({"error": "El archivo no tiene nombre."}), 400
        
        # Validar extensión del archivo
        if not allowed_file(file.filename):
            return jsonify({
                "error": "Tipo de archivo no permitido. Use PNG, JPG, JPEG, GIF, BMP o WEBP."
            }), 400

        try:
            # Validar imagen
            validate_image(file)
            
            # Leer imagen con OpenCV
            img_bytes = file.read()
            file.seek(0)  # Resetear puntero de archivo
            
            # Decodificar imagen con OpenCV
            img_np = cv2.imdecode(np.frombuffer(img_bytes, np.uint8), cv2.IMREAD_COLOR)
            
            # Convertir de BGR a RGB (RetinaFace prefiere RGB)
            img_rgb = cv2.cvtColor(img_np, cv2.COLOR_BGR2RGB)
            
            # Detectar caras
            resp = RetinaFace.detect_faces(img_rgb)
            
        except ValueError as ve:
            return jsonify({"error": str(ve)}), 400
        except Exception as e:
            # Errores inesperados durante el procesamiento de imagen
            return jsonify({
                "error": "Error interno al procesar la imagen.", 
                "detalle": str(e)
            }), 500

        try:
            # Procesar caras detectadas
            facial_areas = []
            for key, item in resp.items():
                if item.get("facial_area"):
                    # Convertir valores a enteros
                    facial_area = [int(i) for i in item["facial_area"]]
                    facial_areas.append({
                        "bbox": facial_area,
                        "confidence": float(item.get("score", 0)),
                        "id": key  # Añadir identificador único de cara
                    })

            # Devolver resultados de detección
            return jsonify({
                "detecciones": facial_areas,
                "total_caras": len(facial_areas)
            }), 200

        except Exception as e:
            return jsonify({
                "error": "Error al procesar los resultados de detección.",
                "detalle": str(e)
            }), 500

    except werkzeug.exceptions.RequestEntityTooLarge:
        return jsonify({"error": "El archivo es demasiado grande."}), 413

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
    app.run(host="0.0.0.0", port=5001, debug=False)