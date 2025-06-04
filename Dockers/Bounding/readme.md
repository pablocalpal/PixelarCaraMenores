### Bounding

El modulo `Bounding` se encarga de detectar caras en la imagen que se le pase utilizando el modelo **RetinaFace**. Este servicio actúa como primer paso dentro del flujo del sistema, identificando las coordenadas de las caras presentes en una imagen para su posterior procesamiento.

#### Funcionalidad:

* **Recepción de imágenes:** Acepta imágenes en formatos comunes como PNG, JPG o JPEG mediante un endpoint HTTP.
* **Validación de archivos:** Verifica el tipo, tamaño (máx. 10MB) y validez del archivo recibido antes de procesarlo.
* **Detección facial:** Utiliza RetinaFace para detectar las caras presentes en la imagen y extraer sus coordenadas (`facial_area`) y niveles de confianza (`score`).
* **Respuesta estructurada:** Devuelve un array de detecciones con la posición de cada cara y un identificador único.

#### Flujo de trabajo:

1. **Petición desde Engine:** El componente `Engine` envía una imagen al endpoint `/detectar_caras`.
2. **Validación de la imagen:** Se verifica la extensión, tamaño y contenido de la imagen recibida.
3. **Preprocesamiento:** La imagen se convierte al formato RGB, compatible con RetinaFace.
4. **Inferencia:** RetinaFace detecta las caras presentes en la imagen.
5. **Procesamiento de resultados:** Se extraen las coordenadas de cada cara junto con su nivel de confianza.
6. **Respuesta:** Se devuelve una estructura JSON con la información de las caras detectadas.

#### Estructura de respuesta:

```json
{
  "detecciones": [
    {
      "bbox": [x1, y1, x2, y2],
      "confidence": 0.9987,
      "id": "face_1"
    },
    ...
  ],
  "total_caras": 2
}
```

#### Endpoints:

* `GET /`: Verificación de estado (devuelve mensaje de salud).
* `POST /detectar_caras`: Recibe la imagen y responde con las coordenadas de los rostros detectados.

#### Requisitos:

* Python 3.10+
* Flask
* OpenCV (`cv2`)
* Numpy
* Pillow
* RetinaFace
* Werkzeug

#### Consideraciones:

* Solo se permiten imágenes de hasta **10MB**.
* La detección se realiza en memoria y la respuesta incluye información relevante para componentes posteriores.
