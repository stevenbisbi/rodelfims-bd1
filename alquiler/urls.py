from django.urls import path
from alquiler import views  # Asegúrate de importar tus vistas correctamente

urlpatterns = [
    path('', views.home, name='home'),
    path('alquiler/', views.peliculas, name='alquiler'),
    path('signin/', views.signin, name='signin'),
    path('signup/', views.signup, name='signup'),
    path('ver/', views.mi_vista, name='ver'),
    path('administrador/', views.admin, name='administrador'),
    path('agregar_pelicula/', views.agregar_pelicula, name='agregar_pelicula'),
]