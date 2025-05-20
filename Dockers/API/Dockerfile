FROM python:3.9-slim

WORKDIR /app

RUN pip install --no-cache-dir Flask requests

COPY ./codigo/API_gateway.py /app/API_gateway.py

# Set Flask environment variables
ENV FLASK_APP=API_gateway.py
ENV FLASK_RUN_HOST=0.0.0.0

EXPOSE 8000

# Command to run the app
CMD ["flask", "run", "--port=8000"]