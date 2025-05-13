# Usa una imagen base de Python
FROM python:3.11.12-slim

# Establece el directorio de trabajo
WORKDIR /app

# Instala Flask, NumPy y OpenCV
RUN pip install --no-cache-dir Flask numpy opencv-python-headless

# Copia el código de la API
COPY ./codigo/API_pixelado.py /app/API_pixelado.py

# Define la variable de entorno para Flask
ENV FLASK_APP=API_pixelado.py
ENV FLASK_RUN_HOST=0.0.0.0

# Expone el puerto Flask
EXPOSE 5000

# Comando para ejecutar la app
CMD ["flask", "run"]
