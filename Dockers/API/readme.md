### API

El componente API es el punto de entrada principal del sistema. Este servicio expone un endpoint `/process-image` que gestiona el flujo completo de procesamiento de imágenes.

#### Flujo de trabajo:

1. **Recepción de la imagen:** El cliente envía una imagen al endpoint `/process-image`.
2. **Envío al Engine:** La imagen se envía al contenedor `Engine` que gestiona la comunicación interna entre los demás contenedores (`Bounding`, `ClasificacionEdad`, `Pixelado`).
3. **Respuesta final:** `Engine` envía la imagen procesada a la API, que la devuelve al cliente.

#### Requisitos:

* Python 3.10+
* Flask
* Requests

Para iniciar el contenedor:

```bash
docker-compose up --build api
```
