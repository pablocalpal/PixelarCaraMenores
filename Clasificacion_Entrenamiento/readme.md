### Clasificacion\_Entrenamiento

Este componente es responsable del desarrollo del modelo de clasificación de edad, cuyo objetivo es identificar si una persona en una imagen es menor de edad o adulta. El entrenamiento se lleva a cabo mediante un notebook (`entrenamiento.ipynb`) que utiliza TensorFlow y OpenCV.

#### Estructura del notebook:

1. **Carga de datos:** Se importan los datasets de imágenes etiquetadas con edades.
2. **Preprocesamiento de imágenes:** Las imágenes se convierten a escala de grises, se redimensionan y se normalizan.
3. **Creación del modelo:** Se implementa una arquitectura simple de CNN para clasificación de edades.
4. **Entrenamiento y validación:** Se entrena el modelo utilizando un conjunto de entrenamiento y se valida con un conjunto de validación.
5. **Guardado del modelo:** El modelo entrenado se guarda en formato `.h5` para su posterior uso en el componente `ClasificacionEdad`.

#### Requisitos:

* Python 3.10+
* TensorFlow
* OpenCV

Comando para ejecutar el notebook:

```bash
jupyter notebook entrenamiento.ipynb
```