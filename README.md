# Taller 4: Procesamiento de Datos y Entrenamiento de Modelos con MLFlow y MinIO

## Descripción
Este taller aborda el procesamiento de datos, la gestión de modelos de machine learning y la orquestación de tareas mediante Apache MLflow y MinIO. Se implementa una arquitectura basada en contenedores para facilitar la reproducibilidad y escalabilidad del flujo de trabajo.

El objetivo principal es automatizar la carga, procesamiento y almacenamiento de datos para entrenar modelos de machine learning y gestionar su despliegue en un entorno controlado.

## Estructura del Proyecto

El proyecto está organizado en los siguientes directorios, cada uno con un propósito específico:

- **app/:** Contiene los scripts principales para la gestión de modelos y la ejecución de tareas dentro de la aplicación.

- **dags/:** Almacena los DAGs (Directed Acyclic Graphs) utilizados por Apache Airflow para la orquestación de tareas.

- **datos/:** Incluye los datasets necesarios para el procesamiento y entrenamiento de modelos.

- **logs/:** Directorio para almacenar los registros de ejecución generados por los procesos.

- **minio_data/:** Espacio de almacenamiento para los datos gestionados mediante MinIO.

- **train_models/:** Contiene los scripts y configuraciones necesarios para entrenar los modelos de machine learning.

Archivos de configuración: Incluye docker-compose.yml, Dockerfile y archivos de requerimientos que definen el entorno del proyecto.

```
Taller_4/
│-- app/
│   │-- cargar_modelos.py
│   │-- Dockerfile.app
│   │-- main.py
│   │-- requirements.txt
│
│-- dags/
│   │-- carga_datos.py
│   │-- elimina_datos.py
│   │-- train.py
│
│-- datos/
│   │-- penguins_lter.csv
│
│-- logs/
│
│-- minio_data/
│
│-- train_models/
│   │-- Dockerfile.app
│   │-- requirements.txt
│   │-- train.ipynb
│
│-- docker-compose.yml
│-- Dockerfile
│-- README.md
│-- requirements.txt
```

## Requisitos
Antes de ejecutar el taller, asegúrate de tener instalados los siguientes requisitos:

- Docker y Docker Compose
- Python 3.8+
- Apache Airflow
- Mlflow
- MinIO (para almacenamiento de datos)

## Configuración y Ejecución

### 1. Clonar el repositorio
```sh
git clone https://github.com/JohnSanchez27/MLOPS_Taller4
cd MLOps_Taller4
```

### 2. Construir y levantar los contenedores
Ejecuta el siguiente comando para construir y levantar los servicios definidos en `docker-compose.yml`:
```sh
docker-compose up --build -d
```
Esto iniciará los contenedores de Airflow, MinIO y los servicios relacionados.

### 3. Acceder a Apache Airflow
Abre un navegador y accede a la interfaz web de Airflow en:
```
http:
```
Las credenciales predeterminadas son:
- Usuario: `airflow`
- Contraseña: `airflow`