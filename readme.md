# Sistema de Protección de Menores en Imágenes

Este proyecto implementa un sistema completo para la detección automática de menores en fotografías y su posterior pixelado para proteger su privacidad. El sistema está compuesto por múltiples microservicios que trabajan en conjunto utilizando Docker.

## 🎯 Objetivo

Desarrollar una solución automatizada que:
- Detecte rostros en imágenes
- Clasifique la edad de las personas (menor/mayor de edad)
- Pixele automáticamente los rostros de menores
- Proporcione una interfaz web para el usuario final

![image](https://github.com/user-attachments/assets/338eb255-cf7e-4632-8b07-4c0e214622fa)

## 🏗️ Arquitectura del Sistema

El proyecto está organizado en los siguientes servicios:

### 🔧 API Gateway (`API/`)
Punto de entrada principal del sistema que coordina las peticiones entre los diferentes servicios.

### 🤖 Engine (`Engine/`)
Motor principal de procesamiento que orquesta el flujo de trabajo entre los servicios de detección, clasificación y pixelado.

### 📦 Bounding (`Bounding/`)
Servicio encargado de la detección de rostros en las imágenes y la generación de coordenadas de delimitación.

### 🧠 Clasificación por Edad (`ClasificacionEdad/`)
Servicio de machine learning que determina si una persona es menor o mayor de edad basándose en características faciales.

### 🔒 Pixelado (`Pixelado/`)
Servicio que aplica efectos de pixelado a las regiones especificadas para proteger la identidad de los menores.

### 🌐 Web Interface (`web/`)
Interfaz web desarrollada en HTML/CSS/JavaScript que permite a los usuarios cargar imágenes y visualizar los resultados.

## 🚀 Tecnologías Utilizadas

- **Docker & Docker Compose**: Containerización y orquestación de servicios
- **Python**: Lenguaje principal para los servicios de backend
- **OpenCV**: Procesamiento de imágenes
- **TensorFlow**: Machine learning para clasificación de edad
- **Flask**: APIs REST
- **HTML/CSS/JavaScript**: Frontend web
- **Jupyter Notebooks**: Entrenamiento y experimentación de modelos

## 🔧 Instalación y Configuración

1. **Clonar el repositorio**
   ```bash
   git clone https://github.com/pablocalpal/PixelarCaraMenores
   cd clasificacion-entrenamiento
   ```

2. **Construir los contenedores**
   ```bash
   docker-compose build
   ```

3. **Iniciar los servicios**
   ```bash
   docker-compose up -d
   ```

4. **Verificar que todos los servicios estén funcionando**
   ```bash
   docker-compose ps
   ```

## 📖 Uso del Sistema

1. **Acceder a la interfaz web** en el archivo `./web/index.html`
2. **Cargar una imagen** utilizando el formulario de upload
3. **Procesar la imagen** - el sistema automáticamente:
   - Detectará los rostros
   - Clasificará la edad de cada persona
   - Pixelará los rostros de menores detectados
4. **Descargar el resultado** con las protecciones aplicadas

## 🔄 Flujo de Procesamiento

```
Imagen Original → Detección de Rostros → Clasificación de Edad → Pixelado Selectivo → Imagen Procesada
```

## 📁 Estructura de Directorios

```
clasificacion-entrenamiento/
├── API/                    # Gateway y coordinador principal
├── Bounding/              # Detección de rostros
├── ClasificacionEdad/     # Clasificación de edad
├── Engine/                # Motor de procesamiento
├── Pixelado/             # Aplicación de efectos de privacidad
├── web/                  # Interfaz de usuario
└── docker-compose.yml    # Configuración de servicios
```

## 🛠️ Desarrollo y Contribución

### Configuración de Desarrollo

1. Cada servicio puede desarrollarse independientemente
2. Utilizar los Dockerfiles individuales para testing
3. El notebook de jupyter de entrenamiento del modelo de clasificación es público para experimentar con el / hacer transferencia de conocimiento.

## 🔒 Consideraciones de Privacidad

Este sistema está diseñado para **proteger la privacidad de menores**. Todas las imágenes procesadas:
- Se mantienen en memoria durante el procesamiento
- No se almacenan permanentemente en el servidor
- Se procesan de forma local sin envío a servicios externos
