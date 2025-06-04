# Clasificación de menores

Docker que expone un endpoint para clasificar imágenes y predecir si contienen rostros de personas menores de 18 años, utilizando un modelo previamente entrenado en Tensorflow.

## Requisitos

* Python 3.7+
* Flask
* numpy
* opencv-python
* keras (y tensorflow como backend)

La API queda disponible en `http://localhost:5002`

## Endpoints

### GET `/`

Verifica que el servicio está operativo.

**Respuesta:**

```json
{
  "message": "API de Detección Facial operativa"
}
```

---

### POST `/menores`

Clasifica una o varias imágenes enviadas mediante `multipart/form-data`.

**Parámetros:**

* `imagenes`: una o varias imágenes (cada cara detectada recortada de la imagen original) `.jpg`, `.jpeg` o `.png`
* `debug`: opcional, si es `"true"` se devuelve salida detallada por imagen

**Respuesta simple (sin debug):**

```json
[1, 0, 1]
```

**Respuesta con debug=true:**

```json
{
  "resultados": [1, 0],
  "detalle": [
    {
      "imagen_id": 0,
      "probabilidad": 0.42,
      "es_menor": true,
      "confianza": 0.18,
      "umbral_usado": 0.6
    },
    {
      "imagen_id": 1,
      "probabilidad": 0.81,
      "es_menor": false,
      "confianza": 0.21,
      "umbral_usado": 0.6
    }
  ],
  "debug": true,
  "total_imagenes": 2,
  "menores_detectados": 1
}
```

---

## Detalles técnicos

* Imágenes redimensionadas a `64x64`, normalizadas en rango `[0, 1]`
* El modelo devuelve una probabilidad entre 0 y 1
* Umbral de clasificación:

  * `< 0.6` → menor (1)
  * `>= 0.6` → no menor (0)
  
  Elijo este umbral para que haya menos falsos negativos, aún sacrificando falsos positivos.
  Preferimos que haya algún adulto pixelado que niños sin pixelar. 

---

## Validaciones

* Solo se aceptan `.jpg`, `.jpeg`, `.png`
* Tamaño máximo por archivo: 10MB
* Payload total máximo: 16MB
* Se ignoran archivos vacíos o inválidos

---

¿Quieres que prepare un `Dockerfile` también?
