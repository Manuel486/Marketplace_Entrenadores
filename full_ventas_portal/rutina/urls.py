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
]
