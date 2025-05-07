### Engine

El componente `Engine` actúa como el coordinador interno del sistema. Se encarga de gestionar el flujo de comunicación entre los componentes `Bounding`, `ClasificacionEdad` y `Pixelado`, y de proporcionar respuestas estructuradas a la API.

#### Funcionalidad:

* **Coordinación de procesos:** Recibe las imágenes desde la API y orquesta la comunicación con los contenedores internos.
* **Manejo de excepciones:** Implementa control de errores para los casos en los que un servicio no responde o falla.
* **Formato de respuestas:** Recibe las respuestas de los componentes y las organiza en un formato estándar para su envío a la API.

#### Flujo de trabajo:

1. **Recepción de la imagen:** La API envía la imagen al `Engine` para su procesamiento.
2. **Detección de caras:** `Engine` envía la imagen a `Bounding` y recibe las coordenadas de las caras detectadas.
3. **Clasificación de edad:** `Engine` envía cada cara detectada a `ClasificacionEdad` y recibe la etiqueta (`menor` o `adulto`).
4. **Pixelado:** `Engine` envía las caras etiquetadas como `menor` a `Pixelado` y recibe las caras pixeladas.
5. **Respuesta final:** `Engine` compone la imagen final con las caras pixeladas y envía la respuesta a la API.

#### Requisitos:

* Python 3.10+
* Requests
* Flask (o cualquier otro framework HTTP para coordinar servicios internos)

Para iniciar el contenedor:

```bash
docker-compose up --build engine
```
