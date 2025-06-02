### ClasificacionEdad

Este componente implementa la clasificación de edades utilizando el modelo entrenado en `Clasificacion_Entrenamiento`. Determina si una cara pertenece a un menor o un adulto.

#### Flujo del componente:

1. **Recepción de la cara:** Se recibe una imagen de una cara previamente detectada.
2. **Clasificación:** Se carga el modelo entrenado y se predice si la persona es menor o adulta.
3. **Respuesta:** Se devuelve la etiqueta correspondiente (`menor` o `adulto`).

#### Requisitos:

* Python 3.10+
* TensorFlow
* OpenCV

Endpoint expuesto:

* `/classify-age` (POST): Recibe una cara y devuelve la etiqueta (`menor` o `adulto`).
