from flask import Flask, jsonify, request
import numpy as np
import cv2
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

@app.route("/pixelar", methods=["POST"])
def detectar_caras():
    """
    Endpoint para pixelar porciones de imagen, estas porciones se enviarán a la API como un array de arrays con la información de cada rectangulo a pixelar.
    
    :return: Respuesta de la imagen procesada
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

        # Leer la imagen en formato numpy array
        file_bytes = np.frombuffer(file.read(), np.uint8)
        image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)

        if image is None:
            return jsonify({"error": "No se pudo leer la imagen"}), 400

        if "rectangulos" not in request.form:
            return jsonify({"error": "Debe proporcionar los rectángulos en el campo 'rectangulos'"}), 400

        try:
            data = json.loads(request.form["rectangulos"])
        except json.JSONDecodeError:
            return jsonify({"error": "Formato JSON no válido en 'rectangulos'"}), 400

        # Verifica si es una lista
        if not isinstance(data, list):
            return jsonify({"error": "El cuerpo debe contener un array en la clave 'rectangulos'"}), 400
        
        # Verifica que cada elemento del array sea una lista de números
        for sub_array in data:
            if not isinstance(sub_array, list) or not all(isinstance(i, (int, float)) for i in sub_array):
                return jsonify({"error": "Cada elemento del array debe ser una lista de números"}), 400
        

        # Número de bloques para pixelar
        blocks = 6

        # Dimensiones de la imagen
        h, w = image.shape[:2]
        x_steps = w // blocks
        y_steps = h // blocks

        # Aplicar pixelado en las regiones específicas
        for (x, y, w, h) in data:
            roi = image[y:y + h, x:x + w]
            # Tamaño del bloque basado en el tamaño del ROI
            x_steps = max(w // blocks, 1)
            y_steps = max(h // blocks, 1)

            for y_roi in range(0, h, y_steps):
                for x_roi in range(0, w, x_steps):
                    # Asegurar que los límites no se excedan
                    end_x = min(x_roi + x_steps, w)
                    end_y = min(y_roi + y_steps, h)

                    sub_roi = roi[y_roi:end_y, x_roi:end_x]
                    color = sub_roi.mean(axis=(0, 1)).astype(int)
                    roi[y_roi:end_y, x_roi:end_x] = color

        # Convertir la imagen procesada a formato JPEG
        _, buffer = cv2.imencode('.jpg', image)
        return buffer.tobytes(), 200, {'Content-Type': 'image/jpeg'}

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
    app.run(host="0.0.0.0", port=5000, debug=False)
    
    
    
    
    
    
    
    
    
    
    



