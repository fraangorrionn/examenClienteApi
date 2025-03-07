import environ
import os
from pathlib import Path
import requests
from django.shortcuts import render, redirect
from django.conf import settings
from .forms import *
from .helper import *
from django.contrib import messages
import json


def crear_cabecera():
    return {
        'Authorization': 'Bearer ' + settings.TOKEN_ACCESO,  
        "Content-Type": "application/json"
    }


# Página de inicio
def index(request):
    return render(request, 'index.html')

def lista_usuarios(request):
    headers = crear_cabecera()
    print("Cabecera enviada en lista_usuarios:", headers)  # Verificar que realmente se envía el token
    response = requests.get("http://127.0.0.1:8000/api/v1/usuarios/", headers=headers)
    usuarios = response.json() if response.status_code == 200 else []
    return render(request, "usuarios/lista_usuarios.html", {"usuarios": usuarios})

def lista_apps(request):
    headers = crear_cabecera()
    print("Cabecera enviada en lista_apps:", headers)  
    response = requests.get("http://127.0.0.1:8000/api/v1/apps/", headers=headers)
    apps = response.json() if response.status_code == 200 else []
    return render(request, "apps/lista_apps.html", {"apps": apps})

def lista_comentarios(request):
    headers = crear_cabecera()
    print("Cabecera enviada en lista_comentarios:", headers)  
    response = requests.get("http://127.0.0.1:8000/api/v1/comentarios/", headers=headers)
    comentarios = response.json() if response.status_code == 200 else []
    return render(request, "comentarios/lista_comentarios.html", {"comentarios": comentarios})


# Vista para la búsqueda avanzada de usuarios
def buscar_usuarios(request):
    errores = None
    usuarios = []

    if len(request.GET) > 0:
        formulario = BusquedaAvanzadaUsuarioForm(request.GET)

        if formulario.is_valid():
            try:
                headers = crear_cabecera()
                response = requests.get(
                    "http://127.0.0.1:8000/api/v1/usuarios/buscar",
                    headers=headers,
                    params=formulario.cleaned_data
                )

                if response.status_code == 200:
                    usuarios = response.json()
                else:
                    response.raise_for_status()

            except requests.exceptions.HTTPError as http_err:
                errores = {"error": [f"Error en la petición: {http_err}"]}
            except Exception as err:
                errores = {"error": [f"Error inesperado: {err}"]}
        else:
            errores = formulario.errors

    else:
        formulario = BusquedaAvanzadaUsuarioForm(None)

    return render(request, "usuarios/buscar_usuarios.html", {"formulario": formulario, "usuarios": usuarios, "errores": errores})

def buscar_apps(request):
    errores = None  # Para capturar errores

    if len(request.GET) > 0:  # Si hay filtros en la búsqueda
        formulario = MobileAppBusquedaForm(request.GET)

        if formulario.is_valid():
            try:
                headers = crear_cabecera()

                # Hacer la petición GET a API-REST
                response = requests.get(
                    "http://127.0.0.1:8000/api/v1/apps/buscar",
                    headers=headers,
                    params=formulario.cleaned_data
                )

                if response.status_code == 200:
                    apps = response.json()
                    return render(request, 'apps/buscar_app.html', {
                        "form": formulario, "apps": apps, "errores": errores
                    })
                else:
                    response.raise_for_status()

            except requests.exceptions.HTTPError as http_err:
                print(f'Error HTTP: {http_err}')
                errores = {"error": [f"Error en la petición: {http_err}"]}
                return render(request, 'apps/buscar_app.html', {"form": formulario, "errores": errores})

            except Exception as err:
                print(f'Ocurrió un error: {err}')
                return render(request, 'apps/buscar_app.html', {"form": formulario, "errores": {"error": ["Error desconocido"]}})
        else:
            return render(request, 'apps/buscar_app.html', {"form": formulario})
    else:
        formulario = MobileAppBusquedaForm(None)

    return render(request, 'apps/buscar_app.html', {"form": formulario, "errores": errores})

def buscar_comentarios(request):
    errores = None  
    comentarios = []

    if len(request.GET) > 0:  
        formulario = ComentarioBusquedaForm(request.GET)
        
        if formulario.is_valid():
            try:
                headers = crear_cabecera()  
                response = requests.get(
                    "http://127.0.0.1:8000/api/v1/comentarios/buscar",
                    headers=headers,
                    params=formulario.cleaned_data
                )
                
                if response.status_code == requests.codes.ok:
                    comentarios = response.json()  
                else:
                    response.raise_for_status()
            
            except requests.exceptions.HTTPError as http_err:
                if response.status_code == 400:
                    errores = response.json()  
                    for error in errores:
                        formulario.add_error(error, errores[error])  
                    return render(request, 'comentarios/buscar_comentario.html', {"form": formulario, "errores": errores})
                else:
                    return render(request, 'error_500.html', status=500)  
            
            except Exception as err:
                return render(request, 'error_500.html', status=500)  

    else:
        formulario = ComentarioBusquedaForm(None)  

    return render(request, 'comentarios/buscar_comentario.html', {"form": formulario, "comentarios": comentarios, "errores": errores})


def usuario_crear(request):
    if request.method == "POST":
        try:
            formulario = UsuarioForm(request.POST)
            headers = crear_cabecera()

            if formulario.is_valid():
                datos = formulario.cleaned_data

                response = requests.post(
                    "http://127.0.0.1:8000/api/v1/usuarios/crear/",
                    headers=headers,
                    json=datos  
                )

                if response.status_code == requests.codes.ok:
                    messages.success(request, "Usuario creado correctamente.")
                    return redirect("lista_usuarios")
                else:
                    response.raise_for_status()

        except requests.exceptions.HTTPError as http_err:
            print(f"Error en la petición: {http_err}")
            if response.status_code == 400:
                errores = response.json()
                for error in errores:
                    formulario.add_error(error, errores[error])
                return render(request, "usuarios/crear_usuario.html", {"formulario": formulario})
            else:
                messages.error(request, "Error en el servidor.")
                return redirect("lista_usuarios")

        except Exception as err:
            print(f"Ocurrió un error: {err}")
            messages.error(request, "Error inesperado.")
            return redirect("lista_usuarios")

    else:
        formulario = UsuarioForm()

    return render(request, "usuarios/crear_usuario.html", {"formulario": formulario})


def comentario_crear(request):
    if request.method == "POST":
        try:
            formulario = ComentarioForm(request.POST)
            headers = crear_cabecera()

            if formulario.is_valid():
                datos = formulario.cleaned_data

                response = requests.post(
                    "http://127.0.0.1:8000/api/v1/comentarios/crear/",
                    headers=headers,
                    json=datos  
                )

                if response.status_code == requests.codes.ok:
                    messages.success(request, "Comentario creado correctamente.")
                    return redirect("lista_comentarios")
                else:
                    response.raise_for_status()

        except requests.exceptions.HTTPError as http_err:
            print(f"Error en la petición: {http_err}")
            if response.status_code == 400:
                errores = response.json()
                for error in errores:
                    formulario.add_error(error, errores[error])
                return render(request, "comentarios/crear_comentario.html", {"formulario": formulario})
            else:
                messages.error(request, "Error en el servidor.")
                return redirect("lista_comentarios")

        except Exception as err:
            print(f"Ocurrió un error: {err}")
            messages.error(request, "Error inesperado.")
            return redirect("lista_comentarios")

    else:
        formulario = ComentarioForm()

    return render(request, "comentarios/crear_comentario.html", {"formulario": formulario})

def comentario_editar(request, comentario_id):
    comentario = obtener_comentario(comentario_id)

    if not comentario:
        messages.error(request, "Comentario no encontrado.")
        return redirect("lista_comentarios")

    if request.method == "POST":
        formulario = ComentarioForm(request.POST, comentario=comentario)

        if formulario.is_valid():
            headers = crear_cabecera()

            datos = formulario.cleaned_data.copy()
            datos["editado"] = True  # Marcamos el comentario como editado

            response = requests.put(
                f"http://127.0.0.1:8000/api/v1/comentarios/editar/{comentario_id}",
                headers=headers,
                json=datos  
            )

            if response.status_code == 200:
                messages.success(request, "Comentario editado correctamente.")
                return redirect("lista_comentarios")
            else:
                messages.error(request, f"Error al actualizar comentario: {response.text}")
    else:
        formulario = ComentarioForm(comentario=comentario)

    return render(request, "comentarios/editar_comentario.html", {"form": formulario, "comentario": comentario})



def comentario_actualizar_texto(request, comentario_id):
    comentario = obtener_comentario(comentario_id)
    if not comentario:
        messages.error(request, "Comentario no encontrado.")
        return redirect("lista_comentarios")

    # Crear formulario con datos iniciales (solo 'texto')
    datos_iniciales = {
        'texto': comentario['texto'],  
    }
    formulario = ComentarioActualizarTextoForm(initial=datos_iniciales)

    if request.method == "POST":
        formulario = ComentarioActualizarTextoForm(request.POST)
        if formulario.is_valid():
            # Preparamos los datos
            datos = formulario.cleaned_data.copy()

            # Hacemos la petición PATCH
            headers = crear_cabecera()
            response = requests.patch(
                f"http://127.0.0.1:8000/api/v1/comentarios/actualizar-texto/{comentario_id}",
                headers=headers,
                data=json.dumps(datos)
            )

            if response.status_code == 200:
                messages.success(request, "Texto del comentario actualizado correctamente.")
                return redirect("lista_comentarios")
            else:
                messages.error(request, f"Error al actualizar comentario: {response.text}")
        else:
            messages.error(request, "Hay errores en el formulario.")

    return render(request, "comentarios/actualizar_texto.html", {
        "formulario": formulario,
        "comentario": comentario
    })
    
def comentario_eliminar(request, comentario_id):
    try:
        headers = crear_cabecera()
        response = requests.delete(
            f"http://127.0.0.1:8000/api/v1/comentarios/eliminar/{comentario_id}",
            headers=headers,
        )
        if response.status_code == requests.codes.ok:
            messages.success(request, "Comentario eliminado correctamente.")
            return redirect("lista_comentarios")
        else:
            print("Código de estado:", response.status_code)
            print("Contenido:", response.text)
            messages.error(request, f"Error al eliminar el comentario: {response.text}")
    except Exception as err:
        print(f"Ocurrió un error: {err}")
        messages.error(request, "Ha ocurrido un error interno al intentar eliminar el comentario.")
    
    return redirect("lista_comentarios")

##################################################################################################

def registrar_usuario(request):
    if request.method == "POST":
        try:
            formulario = RegistroForm(request.POST)
            if formulario.is_valid():
                headers = {
                    "Content-Type": "application/json"
                }

                response = requests.post(
                    "http://127.0.0.1:8000/api/v1/registrar/usuario",  # Ajusta según tu API
                    headers=headers,
                    data=json.dumps(formulario.cleaned_data)
                )

                if response.status_code == requests.codes.ok:
                    usuario = response.json()
                    token_acceso = obtener_token_session(
                        formulario.cleaned_data.get("username"),
                        formulario.cleaned_data.get("password1")
                    )

                    request.session["usuario"] = usuario
                    request.session["token"] = token_acceso
                    messages.success(request, "Registro exitoso. ¡Bienvenido!")
                    return redirect("index")
                else:
                    messages.error(request, f"Error al registrar usuario: {response.text}")
                    print(response.status_code, response.text)

        except requests.exceptions.RequestException as error:
            print(f"Error en la petición: {error}")
            messages.error(request, "Hubo un problema al comunicarse con la API.")
    
    else:
        formulario = RegistroForm()

    return render(request, "registration/signup.html", {"formulario": formulario})

def login(request):
    if request.method == "POST":
        formulario = LoginForm(request.POST)

        try:
            token_acceso = obtener_token_session(
                formulario.cleaned_data.get("usuario"),
                formulario.cleaned_data.get("password")
            )

            if not token_acceso:
                raise Exception("Credenciales inválidas")

            request.session["token"] = token_acceso
            headers = {'Authorization': f'Bearer {token_acceso}'}

            response = requests.get(
                f"http://127.0.0.1:8000/api/v1/usuario/token/{token_acceso}",
                headers=headers
            )

            if response.status_code == 200:
                usuario = response.json()
                request.session["usuario"] = usuario
                messages.success(request, "Inicio de sesión exitoso.")
                return redirect("index")
            else:
                messages.error(request, "No se pudo recuperar la información del usuario.")

        except requests.exceptions.RequestException as excepcion:
            print(f"Error en la petición: {excepcion}")
            messages.error(request, "Error de conexión con la API.")
            formulario.add_error("usuario", excepcion)
            formulario.add_error("password", excepcion)

    else:
        formulario = LoginForm()

    return render(request, "registration/login.html", {"form": formulario})

def logout(request):
    del request.session['token']
    return redirect('index')
