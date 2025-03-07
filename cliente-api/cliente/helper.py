import requests
import environ
import os
from pathlib import Path

# Cargar variables del .env
BASE_DIR = Path(__file__).resolve().parent.parent
env = environ.Env()
environ.Env.read_env(os.path.join(BASE_DIR, ".env"), True)

# Función para obtener usuarios en formato de selección para formularios
def obtener_usuarios_select():
    headers = {'Authorization': 'Bearer ' + env("TOKEN_ADMIN")}
    response = requests.get("http://127.0.0.1:8000/api/v1/usuarios", headers=headers)

    if response.status_code == 200:
        usuarios = response.json()
        lista_usuarios = [(usuario["id"], usuario["username"]) for usuario in usuarios]
        return lista_usuarios
    else:
        return []
    

def obtener_apps_select():
    headers = {'Authorization': 'Bearer ' + env("TOKEN_ADMIN")}
    response = requests.get("http://127.0.0.1:8000/api/v1/apps", headers=headers)

    if response.status_code == 200:
        apps = response.json()
        return [(app["id"], app["nombre"]) for app in apps]
    return []


def obtener_comentario(comentario_id):
    headers = {'Authorization': 'Bearer ' + env("TOKEN_ADMIN")}
    response = requests.get(f"http://127.0.0.1:8000/api/v1/comentarios/{comentario_id}", headers=headers)

    print("Código de respuesta:", response.status_code)  # Verificar el código de estado
    print("Texto de respuesta:", response.text)  # Verificar si devuelve HTML u otra cosa

    if response.status_code == 200:
        try:
            return response.json()  # Intentamos parsear solo si la respuesta tiene contenido
        except requests.exceptions.JSONDecodeError:
            print("La API devolvió una respuesta vacía o inválida.")
            return None
    return None

def obtener_token_session(usuario,password):
        token_url = "http://127.0.0.1:8000/api/v1/token/" 
        data = {
            'grant_type': 'password',
            'username': usuario,
            'password': password,
            'client_id': 'mi_aplicacion',
            'client_secret': 'mi_clave_secreta',
        }

        response = requests.post(token_url, data=data)
        respuesta = response.json()
        if response.status_code == 200:
            return respuesta.get('access_token')
        else:
            raise Exception(respuesta.get("error_description"))

