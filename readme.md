# Proyecto de Identificación y Protección de Menores en Imágenes

Este repositorio contiene un sistema completo para la identificación de caras en imágenes, la clasificación de edades y la protección de menores mediante pixelado. El proyecto está compuesto por varios contenedores Docker interconectados que implementan diferentes etapas del proceso:

1. **Clasificacion\_Entrenamiento:** Entrena un modelo de clasificación de edades que distingue entre menores y adultos utilizando imágenes faciales.
2. **Bounding:** Detecta caras en una imagen utilizando un modelo preexistente descargado de internet.
3. **ClasificacionEdad:** Clasifica cada cara detectada como `menor` o `adulto` usando el modelo entrenado.
4. **Pixelado:** Aplica un filtro de pixelado a las caras etiquetadas como `menor`.
5. **Engine:** Coordina el flujo interno entre los contenedores anteriores y estructura las respuestas para la API.
6. **API:** Expone un endpoint público `/process-image` que inicia el flujo de procesamiento, gestiona las peticiones y devuelve la imagen final procesada.

## Arquitectura del sistema

* **Docker:** Cada componente está dockerizado por separado, permitiendo una fácil escalabilidad y despliegue.
* **Red interna de Docker:** Los contenedores se comunican entre sí a través de una red privada, asegurando que los componentes internos no sean accesibles desde fuera del sistema.
* **Flujo de procesamiento:** La API envía la imagen al `Engine`, que coordina la detección de caras (`Bounding`), la clasificación de edad (`ClasificacionEdad`) y el pixelado (`Pixelado`), y retorna la imagen final procesada.

## Requisitos del sistema

* Docker y Docker Compose
* Python 3.10+
* TensorFlow
* OpenCV
* Flask
* Requests

## Instrucciones de despliegue

1. Clonar el repositorio:

   ```bash
   git clone <URL del repositorio>
   cd <directorio del repositorio>
   ```
2. Construir los contenedores:

   ```bash
   docker-compose up --build
   ```
3. Acceder a la API:

   * Endpoint principal: `http://localhost:5000/process-image`

## Flujo de trabajo

* **Entrada:** Imagen enviada a la API en formato base64.
* **Procesamiento:**

  1. Detección de caras (`Bounding`).
  2. Clasificación de edad (`ClasificacionEdad`).
  3. Pixelado de caras de menores (`Pixelado`).
* **Salida:** Imagen con las caras de menores pixeladas.

## Desarrollo y pruebas

* Cada componente tiene su propio archivo `readme.md` que detalla el propósito, los endpoints y las instrucciones específicas de ejecución.
* Los modelos de clasificación se entrenan en el notebook `entrenamiento.ipynb` dentro del componente `Clasificacion_Entrenamiento`