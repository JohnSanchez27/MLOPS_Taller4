import os
import mlflow
import mlflow.sklearn
import json

def cargar_modelos():
    print("Ingresando a la carga de modelos desde MLflow...")

    try:
        # Configuración del URI de seguimiento de MLflow
        mlflow.set_tracking_uri("http://10.43.101.179:5000")  # Asegúrate de que esta URL apunte a tu servidor MLflow
        
        # Cargar el modelo desde MLflow (usando su nombre y la etiqueta de 'producción')
        model_uri = "models:/production_model/Production"  # Reemplaza 'production_model' con el nombre de tu modelo
        print(f"Intentando cargar el modelo de MLflow: {model_uri}")

        # Cargar el modelo registrado
        modelo1 = mlflow.pyfunc.load_model(model_uri)

        # Hacer inferencia
        print("Modelo cargado exitosamente desde MLflow.")
        
        return modelo1
    except Exception as e:
        print(f"Error al cargar el modelo desde MLflow: {e}")
        return None

