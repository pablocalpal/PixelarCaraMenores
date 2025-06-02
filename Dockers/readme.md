# Docker Compose - Sistema Completo de Protección de Menores

Este directorio contiene la configuración de Docker Compose para desplegar todo el sistema de detección y protección de menores en imágenes como un conjunto de microservicios.

## 🏗️ Arquitectura del Sistema

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│       Web       │    │   API Gateway   │    │     Engine      │
│  (index.html)   │◄──►│  (Puerto 8000)  │◄──►│  (Puerto 5003)  │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                                       │
                              ┌────────────────────────┼────────────────────────┐
                              │                        │                        │
                              ▼                        ▼                        ▼
                    ┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
                    │    Bounding     │    │ClasificacionEdad│    │    Pixelado     │
                    │  (Puerto 5001)  │    │ (Puerto 5002)   │    │  (Puerto 5004)  │
                    └─────────────────┘    └─────────────────┘    └─────────────────┘
```

## 🐳 Servicios Incluidos

### 🌐 **web** - Interfaz Web
- **Descripción**: Frontend HTML/CSS/JavaScript para cargar imágenes
- **Acceso**: `/web/index.html`

### 🚪 **api** - API Gateway  
- **Puerto**: 8000
- **Descripción**: Punto de entrada público del sistema
- **Endpoint principal**: `POST /pixelar_menores`
- **Acceso**: http://localhost:8000

### 🤖 **engine** - Motor de Procesamiento
- **Puerto**: 5003
- **Descripción**: Orquesta el flujo completo de procesamiento
- **Endpoint**: `POST /procesar`
- **Acceso interno**: http://localhost:5003

### 📦 **bounding** - Detección de Rostros
- **Puerto**: 5001
- **Descripción**: Detecta rostros y genera bounding boxes
- **Acceso interno**: http://localhost:5001

### 🧠 **clasificacion** - Clasificación de Edad
- **Puerto**: 5002
- **Descripción**: Determina si una persona es menor de edad
- **Acceso interno**: http://localhost:5002

### 🔒 **pixelado** - Aplicación de Pixelado
- **Puerto**: 5004
- **Descripción**: Aplica efectos de pixelado a rostros de menores
- **Acceso interno**: http://localhost:5004

## 🚀 Despliegue Rápido


### Verificación del Despliegue

```bash
# Estado de todos los servicios
docker-compose ps

# Logs de todos los servicios
docker-compose logs

# Logs de un servicio específico
docker-compose logs api
docker-compose logs engine

# Seguir logs en tiempo real
docker-compose logs -f
```
