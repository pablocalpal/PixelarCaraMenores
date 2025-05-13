### Pixelado

Este componente se encarga de pixelar las caras etiquetadas como `menor`, preservando así la identidad del menor antes de retornar la imagen procesada.

#### Flujo del componente:

1. **Recepción de la cara:** Se recibe una imagen de una cara etiquetada como `menor`.
2. **Pixelado:** Se aplica un filtro de pixelado a la región de la cara.
3. **Respuesta:** Se devuelve la imagen modificada al componente `API` para su composición final.

#### Requisitos:

* Python 3.10+
* OpenCV

Endpoint expuesto:

* `/pixelate-face` (POST): Recibe una cara y devuelve la cara pixelada.