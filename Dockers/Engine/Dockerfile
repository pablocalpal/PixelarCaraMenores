# Use an older Python base image compatible with TensorFlow 2.5.0
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install dependencies - with specific sequence to manage compatibility
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir \
    Flask \
    numpy \
    Pillow \
    werkzeug \
    opencv-python-headless && \
    pip install --no-cache-dir tensorflow==2.5.0 && \
    pip install --no-cache-dir retinaface==1.1.1

# Copy API code
COPY ./codigo/engine_api.py /app/engine_api.py

# Set Flask environment variables
ENV FLASK_APP=engine_api.py
ENV FLASK_RUN_HOST=0.0.0.0

# Expose Flask port
EXPOSE 5003

# Command to run the app
CMD ["flask", "run", "--port=5003"]