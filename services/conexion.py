import requests
from dotenv import load_dotenv
import os

load_dotenv()
BASE_URL =os.getenv("BASE_URL")
API_KEY=os.getenv("API_KEY") # Reemplaza con la URL de tu API

# Función para manejar las solicitudes GET
def get_request(endpoint):
    try:
        response = requests.get(f"{BASE_URL}{endpoint}{API_KEY}")
        response.raise_for_status()  # Verifica que la solicitud fue exitosa
        return response.json()  # Devuelve la respuesta como un diccionario
    except requests.exceptions.RequestException as e:
        print(f"Error GET: {e}")
        return None

# Función para manejar las solicitudes POST
def post_request(endpoint, data):
    try:
        response = requests.post(f"{BASE_URL}{endpoint}{API_KEY}", json=data)
        response.raise_for_status()  # Verifica que la solicitud fue exitosa
        return response.json()  # Devuelve la respuesta como un diccionario
    except requests.exceptions.RequestException as e:
        print(f"Error POST: {e}")
        return None

# Función para manejar las solicitudes PUT
def put_request(endpoint, id, data):
    try:
        response = requests.put(f"{BASE_URL}{endpoint}/{id}{API_KEY}", json=data)
        response.raise_for_status()  # Verifica que la solicitud fue exitosa
        return response.json()  # Devuelve la respuesta como un diccionario
    except requests.exceptions.RequestException as e:
        print(f"Error PUT: {e}")
        return None

# Función para manejar las solicitudes DELETE
def delete_request(endpoint, id):
    try:
        response = requests.delete(f"{BASE_URL}{endpoint}/{id}{API_KEY}")
        response.raise_for_status()  # Verifica que la solicitud fue exitosa
        return response.status_code == 204  # Devuelve True si el código de estado es 204
    except requests.exceptions.RequestException as e:
        print(f"Error DELETE: {e}")
        return False

# Función para obtener un recurso por ID (GET/{id})
def get_by_id(endpoint, id):
    try:
        response = requests.get(f"{BASE_URL}{endpoint}/{id}{API_KEY}")
        response.raise_for_status()  # Verifica que la solicitud fue exitosa
        return response.json()  # Devuelve la respuesta como un diccionario
    except requests.exceptions.RequestException as e:
        print(f"Error GET by ID: {e}")
        return None

def search_by_field(endpoint, field, value):
    try:
        data={
            "field": field,
            "value": value
            }
        
        response = requests.post(f"{BASE_URL}{endpoint}/search{API_KEY}", json=data)
        response.raise_for_status()  # Verifica que la solicitud fue exitosa
        return response.json()  # Devuelve la respuesta como un diccionario
    except requests.exceptions.RequestException as e:
        #print(f"Error POST: {e}")
        return None