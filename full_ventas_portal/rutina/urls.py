from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'), 
    path('login', views.login, name='login'),
    path('gestionRutinas', views.gestionRutinas, name='gestionRutinas'),
    path('visualizarRutina/<int:id>', views.visualizarRutina, name='visualizarRutina'),
    path('registrarRutina/', views.registrarRutina, name='registrarRutina'),
    path('editarRutina/<int:id>/', views.editarRutina, name='editarRutina'),
    path('eliminarRutina/<int:id>/', views.eliminarRutina, name='eliminarRutina'),

    ## Filtros
    path('obtener-instructores/', views.obtener_instructores_por_especialidad, name='obtener_instructores_por_especialidad'),
    path('obtener_metas_por_tipo_de_rutina/', views.obtener_metas_por_tipo_de_rutina, name='obtener_metas_por_tipo_de_rutina'),

    ## Tipo de Rutinas
    path('gestionTipoDeRutinas/', views.gestionTipoDeRutinas, name='gestionTipoDeRutinas'),
    path('registrarTipoDeRutina/', views.registrarTipoDeRutina, name='registrarTipoDeRutina'),
    path('editarTipoDeRutina/<int:id>/', views.editarTipoDeRutina, name='editarTipoDeRutina'),
    path('visualizarTipoDeRutina/<int:id>/', views.visualizarTipoDeRutina, name='visualizarTipoDeRutina'),
    path('eliminarTipoDeRutina/<int:id>/', views.eliminarTipoDeRutina, name='eliminarTipoDeRutina'),

    path('logout/', views.logout, name='logout'),
    
    path('listarRutinasDelCliente/<int:id>/', views.listarRutinasDelCliente, name='listarRutinasDelCliente'),
]
