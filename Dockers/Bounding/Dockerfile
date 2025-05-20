# Use an older Python base image compatible with TensorFlow 2.5.0
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Instala dependencias del sistema
RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Install dependencies - with specific sequence to manage compatibility
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir \
    Flask \
    numpy \
    Pillow \
    werkzeug \
    opencv-python-headless && \
    pip install --no-cache-dir tensorflow==2.5.0 && \
    pip install retina-face==0.0.17

# Copy API code
COPY ./codigo/API_bounding.py /app/API_bounding.py

# Set Flask environment variables
ENV FLASK_APP=API_bounding.py
ENV FLASK_RUN_HOST=0.0.0.0

# Expose Flask port
EXPOSE 5001

# Command to run the app
CMD ["flask", "run", "--port=5001"]