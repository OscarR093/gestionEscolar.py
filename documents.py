import json
import random
import os

def generar_id_unico(array):
    # Longitud del arreglo
    longitud_array = len(array)
    
    # Generar un ID único: Prefijo de 3 dígitos seguido de longitud aleatoria
    prefijo = random.randint(1000, 9999)  # Genera un prefijo único de 4 dígitos
    id_numerico = longitud_array+prefijo
    
    # Retorna el ID único
    return id_numerico

def cargar_datos(nombre_archivo):
    if os.path.exists(nombre_archivo):
        with open(nombre_archivo, "r") as f:
            return json.load(f)
    return []

def guardar_datos(nombre_archivo, datos):
    with open(nombre_archivo, "w") as f:
        json.dump(datos, f, indent=4)