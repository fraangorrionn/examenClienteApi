from django.urls import path
from .import views

urlpatterns = [
    path('', views.index, name='index'),
    
    path('usuarios/', views.lista_usuarios, name='lista_usuarios'),
    path('apps/', views.lista_apps, name='lista_apps'),
    path('comentarios/', views.lista_comentarios, name='lista_comentarios'),
    
    
    path('usuarios/buscar/', views.buscar_usuarios, name='buscar_usuarios'),
    path('usuarios/crear/', views.usuario_crear, name='usuario_crear'),
    
    path('apps/buscar/', views.buscar_apps, name='buscar_apps'),
    
    
    path('comentarios/buscar/', views.buscar_comentarios, name='buscar_comentarios'),
    path('comentarios/crear/', views.comentario_crear, name='comentario_crear'),
    path('comentarios/editar/<int:comentario_id>/', views.comentario_editar, name='comentario_editar'),
    path('comentarios/actualizar-texto/<int:comentario_id>/', views.comentario_actualizar_texto, name='comentario_actualizar_texto'),
    path('comentarios/eliminar/<int:comentario_id>/', views.comentario_eliminar, name='comentario_eliminar'),

    path('registrar',views.registrar_usuario,name='registrar_usuario'),
    path('accounts/login/',views.login,name='login'),
    path('accounts/logout/',views.logout,name='logout'),

]