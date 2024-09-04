from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'), 
    path('login', views.login, name='login'),
    path('home', views.menu, name='menu'),
    path('gestionRutinas', views.gestionRutinas, name='gestionRutinas'),
    path('visualizarRutina/<int:id>', views.visualizarRutina, name='visualizarRutina'),
    path('registrarRutina/', views.registrarRutina, name='registrarRutina'),
    path('editarRutina/<int:id>/', views.editarRutina, name='editarRutina'),
    path('eliminarRutina/<int:id>/', views.eliminarRutina, name='eliminarRutina'),
    ## Filtros
    path('obtener-instructores/', views.obtener_instructores_por_especialidad, name='obtener_instructores_por_especialidad'),
    path('obtener-frecuencias/', views.obtener_frecuencias_por_instructor, name='obtener_frecuencias_por_instructor'),
    path('obtener-rangos-de-fechas/', views.obtener_rangos_de_fechas, name='obtener_rangos_de_fechas'),
    path('obtener_rangos_de_fechas_excluyendo/', views.obtener_rangos_de_fechas_excluyendo, name='obtener_rangos_de_fechas_excluyendo'),
]
