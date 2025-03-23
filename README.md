
# Proyecto MLOPS_Taller4

## 1. **Uso del Proyecto**

Este proyecto es una implementación de un sistema MLOps utilizando **MLflow** para el seguimiento de experimentos, **MinIO** como almacenamiento de artefactos compatible con S3, y **PostgreSQL** como base de datos backend para **MLflow**.

### 1.1 **Requisitos previos**

Asegúrate de tener los siguientes requisitos previos instalados:

- **Docker** y **Docker Compose** (si decides usar Docker para otros servicios).
- **Python 3.x**.
- **Git** (para clonar el repositorio).
- **systemd** (para levantar el servicio `ml_flow_serv.service` de **MLflow**).

### 1.2 **Iniciar los Servicios con Docker Compose**

Para iniciar todos los servicios necesarios (MinIO, PostgreSQL y otros), simplemente ejecuta el siguiente comando desde la raíz del repositorio:

```bash
docker-compose up --build
```

Este comando construirá las imágenes de Docker y levantará los servicios definidos en el archivo `docker-compose.yml`, incluyendo:

- **MinIO** (como almacenamiento de artefactos S3).
- **PostgreSQL** (como base de datos para MLflow).
- Otros servicios como el servicio de **train_models**.

### 1.3 **Acceder a los Servicios**

Una vez que los servicios estén levantados, puedes acceder a los siguientes servicios:

- **MinIO**: Navega a `http://127.0.0.1:9001` para acceder a la consola web de **MinIO** (usando las credenciales `admin` / `password`).
- **MLflow**: Navega a `http://127.0.0.1:5000` para acceder a la interfaz de usuario de **MLflow** y ver los experimentos y modelos registrados.

### 1.4 **Usar el Jupyter Notebook**

Los modelos se entrenan utilizando los **Jupyter Notebooks** ubicados en el directorio `train_models`. Para acceder a los notebooks, navega a:

```bash
http://127.0.0.1:8888
```

Desde ahí podrás entrenar los modelos y registrar los resultados en **MLflow**.

---

## 2. **Estructura del Proyecto**

A continuación se describe la estructura del repositorio:

```
MLOPS_Taller4/
│
├── app/                      # Código de la aplicación FastAPI
├── train_models/             # Directorio para el código de entrenamiento de modelos
│   ├── datos/                # Datos de entrada
│   ├── mlruns/               # Directorio local donde se guardan los experimentos
│   └── train_models.py       # Código principal para entrenamiento de modelos
│
├── docker-compose.yml        # Configuración de Docker Compose
├── ml_flow_serv.service      # Archivo de configuración para el servicio de MLflow
├── requirements.txt          # Dependencias de Python
└── README.md                 # Documentación del repositorio
```

### 2.1 **Explicación de los Servicios**

1. **MinIO**:
   - **MinIO** actúa como un almacenamiento S3 local para los artefactos de **MLflow**. Los modelos y otros artefactos (como archivos de datos) se almacenan en el bucket `mlflows3/artifacts`.
   
2. **PostgreSQL**:
   - **PostgreSQL** se usa como el almacenamiento backend de **MLflow**. La base de datos `mlflow` es donde se guardan los metadatos de los experimentos (parámetros, métricas, etc.).

3. **MLflow**:
   - **MLflow** se utiliza para realizar el seguimiento de los experimentos, registrar los modelos y almacenarlos en **MinIO**.
   - **MLflow** se levanta mediante el archivo `ml_flow_serv.service`, que es un servicio de **systemd** que inicia **MLflow** en el sistema.

4. **train_models**:
   - Contiene el código para entrenar los modelos utilizando **scikit-learn** y otros frameworks.
   - Los experimentos y los artefactos se registran en **MLflow** y se almacenan en **MinIO**.

---

## 3. **Levantamiento de MLflow desde el servicio `.service`**

En lugar de usar **Docker** para levantar el servicio de **MLflow**, hemos optado por levantarlo utilizando un archivo de servicio **systemd** llamado `ml_flow_serv.service`. Aquí te explicamos cómo levantar **MLflow** a partir de este archivo.

### 3.1 **Configurar el archivo de servicio `ml_flow_serv.service`**

El archivo `ml_flow_serv.service` se encuentra en la raíz del proyecto. Este archivo define cómo debe iniciarse **MLflow** como un servicio de sistema. Aquí está el archivo corregido:

```ini
[Unit]
Description=MLflow tracking server
After=network.target

[Service]
User=estudiante
Restart=on-failure
RestartSec=3
WorkingDirectory=/home/estudiante/MLOPS_Taller4/

# Configuración de MinIO como almacenamiento de artefactos S3
Environment=MLFLOW_S3_ENDPOINT_URL=http://10.43.101.179:9000
Environment=AWS_ACCESS_KEY_ID=admin
Environment=AWS_SECRET_ACCESS_KEY=password

# Apuntar a la carpeta local donde se almacenan los experimentos
Environment=MLFLOW_TRACKING_URI=file:///home/estudiante/MLOPS_Taller4/train_models/mlruns

# Iniciar el servidor MLflow
ExecStart=/usr/bin/python3 -m mlflow server   --backend-store-uri "postgresql://mlflow:mlflowpassword@172.18.0.4:5432/mlflow"   --default-artifact-root s3://mlflows3/artifacts   --host 0.0.0.0   --serve-artifacts

ExecStopPost=/bin/echo "MLflow process stopped" >> /home/estudiante/mlflow.log

[Install]
WantedBy=multi-user.target
```

### 3.2 **Iniciar el servicio de MLflow con `systemd`**

1. **Recargar el archivo de servicio** para que **systemd** reconozca cualquier cambio realizado:

   ```bash
   sudo systemctl daemon-reload
   ```

2. **Iniciar el servicio de MLflow**:

   ```bash
   sudo systemctl start ml_flow_serv.service
   ```

3. **Verificar el estado del servicio**:

   Para verificar que **MLflow** se está ejecutando correctamente, puedes comprobar su estado con:

   ```bash
   sudo systemctl status ml_flow_serv.service
   ```

4. **Ver los logs de **MLflow**:

   Si necesitas verificar los logs de **MLflow** para asegurarte de que todo está funcionando bien, puedes hacerlo con:

   ```bash
   sudo journalctl -u ml_flow_serv.service -f
   ```

### 3.3 **Detener el servicio de MLflow**

Si necesitas detener el servicio de **MLflow**, puedes hacerlo con:

```bash
sudo systemctl stop ml_flow_serv.service
```

---

## 4. **Problema Actual**

Los servicios funcionan correctamente pero no logracmos realizar la inferencia del modelo desde el API, los experimentos se ejeuctan correctamente en **MLflow** y se con **MinIO** se almacenan los artefactos correctamente como se muestran en la siguientes iamgenes:

Imagenes/MinIO.png

Imagenes/mlflow.png

### Conclusión

Este repositorio implementa una arquitectura básica para **MLOps** utilizando **MLflow**, **MinIO** y **PostgreSQL**. Actualmente, estamos abordando problemas relacionados con la ubicación de los experimentos y el almacenamiento de artefactos en **MinIO**. Con los cambios en el archivo de servicio y en las configuraciones, este sistema debería funcionar correctamente, permitiendo un flujo de trabajo eficiente para el seguimiento de experimentos, el almacenamiento de modelos y la gestión de artefactos.
