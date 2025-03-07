from django import forms
from django import forms
from .helper import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class BusquedaAvanzadaUsuarioForm(forms.Form):
    query = forms.CharField(
        required=False,
        label="Búsqueda Global",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Buscar en todos los campos'})
    )
    username = forms.CharField(
        required=False, 
        label="Nombre de Usuario",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    email = forms.EmailField(
        required=False, 
        label="Correo Electrónico",
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    rol = forms.ChoiceField(
        required=False, 
        label="Rol", 
        choices=[('', 'Todos'), (1, 'Administrador'), (2, 'Creador de Aplicaciones'), (3, 'ClienteAPP')],
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    fecha_registro_desde = forms.DateField(
        required=False,
        label="Registrado Desde",
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )
    fecha_registro_hasta = forms.DateField(
        required=False,
        label="Registrado Hasta",
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )

    def clean(self):
        cleaned_data = super().clean()
        fecha_registro_desde = cleaned_data.get('fecha_registro_desde')
        fecha_registro_hasta = cleaned_data.get('fecha_registro_hasta')

        if fecha_registro_desde and fecha_registro_hasta and fecha_registro_desde > fecha_registro_hasta:
            self.add_error('fecha_registro_hasta', "La fecha de registro hasta no puede ser menor que la fecha de registro desde.")

        return cleaned_data

class MobileAppBusquedaForm(forms.Form):
    query = forms.CharField(
        required=False,
        label="Buscar Aplicación",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre o Descripción'})
    )
    categoria = forms.CharField(
        required=False,
        label="Categoría",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    desarrollador = forms.CharField(
        required=False,
        label="Desarrollador",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    fecha_creacion_desde = forms.DateField(
        required=False,
        label="Creada Desde",
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )
    fecha_creacion_hasta = forms.DateField(
        required=False,
        label="Creada Hasta",
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )


    def clean(self):
        cleaned_data = super().clean()
        fecha_creacion_desde = cleaned_data.get('fecha_creacion_desde')
        fecha_creacion_hasta = cleaned_data.get('fecha_creacion_hasta')

        if fecha_creacion_desde and fecha_creacion_hasta and fecha_creacion_desde > fecha_creacion_hasta:
            self.add_error('fecha_creacion_hasta', "La fecha de creación hasta no puede ser menor que la fecha desde.")


        return cleaned_data


class ComentarioBusquedaForm(forms.Form):
    query = forms.CharField(
        required=False,
        label="Texto del Comentario",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Buscar por texto o respuesta'})
    )
    app = forms.CharField(
        required=False,
        label="Aplicación",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre de la app'})
    )
    usuario = forms.CharField(
        required=False,
        label="Usuario",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre de usuario'})
    )
    fecha_creacion_desde = forms.DateField(
        required=False,
        label="Fecha Desde",
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )
    fecha_creacion_hasta = forms.DateField(
        required=False,
        label="Fecha Hasta",
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )
    calificacion_minima = forms.IntegerField(
        required=False,
        label="Calificación Mínima",
        widget=forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 5})
    )
    calificacion_maxima = forms.IntegerField(
        required=False,
        label="Calificación Máxima",
        widget=forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 5})
    )
    editado = forms.BooleanField(
        required=False,
        label="Editado",
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )

    def clean(self):
        cleaned_data = super().clean()
        query = cleaned_data.get('query')
        app = cleaned_data.get('app')
        usuario = cleaned_data.get('usuario')
        fecha_creacion_desde = cleaned_data.get('fecha_creacion_desde')
        fecha_creacion_hasta = cleaned_data.get('fecha_creacion_hasta')
        calificacion_minima = cleaned_data.get('calificacion_minima')
        calificacion_maxima = cleaned_data.get('calificacion_maxima')

        if not any([query, app, usuario, fecha_creacion_desde, fecha_creacion_hasta, calificacion_minima, calificacion_maxima]):
            self.add_error(None, "Debes ingresar al menos un criterio de búsqueda.")

        if fecha_creacion_desde and fecha_creacion_hasta and fecha_creacion_desde > fecha_creacion_hasta:
            self.add_error('fecha_creacion_hasta', "La fecha hasta no puede ser menor que la fecha desde.")

        if calificacion_minima and calificacion_maxima and calificacion_minima > calificacion_maxima:
            self.add_error('calificacion_maxima', "La calificación máxima no puede ser menor que la mínima.")

        return cleaned_data


class UsuarioForm(forms.Form):
    username = forms.CharField(
        label="Nombre de Usuario",
        max_length=150,
        required=True
    )

    email = forms.EmailField(
        label="Correo Electrónico",
        required=True
    )

    password = forms.CharField(   # Agregar el campo password
        label="Contraseña",
        widget=forms.PasswordInput,
        required=True
    )

    rol = forms.ChoiceField(
        label="Rol",
        choices=[
            (1, "Administrador"),
            (2, "Creador de Aplicaciones"),
            (3, "Cliente")
        ],
        required=True
    )

    email_confirmado = forms.BooleanField(
        label="Email Confirmado",
        required=False
    )

    biografia = forms.CharField(
        label="Biografía",
        widget=forms.Textarea,
        required=False
    )

    telefono = forms.CharField(
        label="Teléfono",
        max_length=15,
        required=False
    )

    usuario = forms.ChoiceField(
        label="Usuarios Disponibles",
        choices=[],
        required=False
    )

    def __init__(self, *args, **kwargs):
        super(UsuarioForm, self).__init__(*args, **kwargs)
        self.fields["usuario"].choices = obtener_usuarios_select()
        
class ComentarioForm(forms.Form):
    texto = forms.CharField(
        label="Comentario",
        widget=forms.Textarea(attrs={"rows": 3}),
        required=True
    )
    
    calificacion = forms.IntegerField(
        label="Calificación",
        min_value=1,
        max_value=5,
        required=True
    )
    
    usuario = forms.ChoiceField(
        label="Usuario",
        choices=[],
        required=True
    )

    app = forms.ChoiceField(
        label="Aplicación",
        choices=[],
        required=True
    )

    respuesta = forms.CharField(
        label="Respuesta (Opcional)",
        widget=forms.Textarea(attrs={"rows": 2}),
        required=False
    )

    def __init__(self, *args, **kwargs):
        comentario = kwargs.pop('comentario', None)
        super(ComentarioForm, self).__init__(*args, **kwargs)

        self.fields["usuario"].choices = obtener_usuarios_select()
        self.fields["app"].choices = obtener_apps_select()

        if comentario:
            self.initial["texto"] = comentario["texto"]
            self.initial["calificacion"] = comentario["calificacion"]
            self.initial["app"] = comentario["app"]
            self.initial["respuesta"] = comentario["respuesta"]
            
class ComentarioActualizarTextoForm(forms.Form):
    texto = forms.CharField(
        label="Texto del Comentario",
        required=True,
        max_length=255,  # Ajusta según lo que necesites
        widget=forms.Textarea(attrs={'rows': 3})
    )
    
    
class RegistroForm(UserCreationForm):
    roles = (
        (1, 'Administrador'),
        (2, 'CreadorDeAplicaciones'),
        (3, 'ClienteAPP'),
    )
    rol = forms.ChoiceField(choices=roles)
    
    nombre = forms.CharField()
    correo = forms.EmailField()
    edad = forms.IntegerField()
    telefono = forms.CharField()

    class Meta:
        model = User 
        fields = (
            'nombre',
            'correo',
            'edad',
            'telefono',
            'password1',
            'password2',
            'rol',
        )


class LoginForm(forms.Form):
    usuario = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())