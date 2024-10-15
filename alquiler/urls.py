from django.urls import path
from alquiler import views  # Asegúrate de importar tus vistas correctamente

urlpatterns = [
    path('', views.home, name='home'),
    path('alquiler/', views.alquiler, name='alquiler'),
    path('signin/', views.signin, name='signin'),
    path('signup/', views.signup, name='signup'),
    path('signout/', views.signout, name='signout'),
    path('administrador/', views.admin, name='administrador'),
    path('alquileres_socio/', views.alquileres_socio, name='alquileres_socio'),
    path('agregar_pelicula/', views.agregar_pelicula, name='agregar_pelicula'),
    path('editar_pelicula/<int:id_pelicula>/', views.editar_pelicula, name='editar_pelicula'),
    path('borrar_pelicula/<int:id_pelicula>/', views.borrar_pelicula, name='borrar_pelicula'),
    path('peliculas/', views.peliculas, name='peliculas'),
    path('mis_alquileres/', views.mis_alquileres, name='mis_alquileres'),
    path('error/', views.error, name='error'),
    path('alquilar/<int:movie_id>/', views.alquilar_pelicula, name='alquilar'),
]