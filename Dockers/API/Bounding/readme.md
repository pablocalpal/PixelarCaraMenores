### Bounding

Este componente se encarga de la detección de caras en imágenes. Utiliza un modelo preentrenado disponible públicamente, basado en OpenCV.

#### Flujo del componente:

1. **Recepción de la imagen:** Se recibe una imagen en formato `[]Bytes`.
2. **Detección de caras:** Se utiliza el modelo para detectar las coordenadas de cada cara en la imagen.
3. **Respuesta:** Se envían las coordenadas de las caras detectadas al componente `API` para su posterior procesamiento.

#### Requisitos:

* Python 3.10+
* OpenCV

Endpoint expuesto:

* `/detect-faces` (POST): Recibe una imagen y devuelve las coordenadas de las caras detectadas.
