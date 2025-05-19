# Usa una imagen base de Python
FROM python:3.11.12-slim

# Establece el directorio de trabajo
WORKDIR /app

# Instala dependencias
RUN pip install --no-cache-dir Flask numpy opencv-python-headless keras h5py tensorflow

# Copia el código de la API
COPY ./codigo/API_clasificacion.py /app/API_clasificacion.py
COPY ./codigo/modelo.keras /app/modelo.keras

# Define la variable de entorno para Flask
ENV FLASK_APP=API_clasificacion.py
ENV FLASK_RUN_HOST=0.0.0.0

# Expone el puerto Flask
EXPOSE 5002

# Comando para ejecutar la app
CMD ["flask", "run", "--port=5002"]