import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

def load_and_clean_csv(file_path):
    """
    Función para cargar un archivo CSV, limpiar el nombre de las columnas y mostrar las primeras filas del DataFrame.
    
    Parámetros:
        file_path (str): La ruta del archivo CSV.

    Retorna:
        pd.DataFrame: El DataFrame cargado y limpio.
    """
    # Cargar el archivo CSV
    df = pd.read_csv(file_path)
    
    # Establecer opciones de visualización
    pd.set_option("display.max_columns", None)
    
    # Limpiar los nombres de las columnas (minúsculas, sin espacios)
    df.columns = df.columns.str.lower().str.strip().str.replace(" ", "_")
    
    # Mostrar las primeras filas
    return df