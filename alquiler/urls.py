from django.urls import path
from alquiler import views  # Asegúrate de importar tus vistas correctamente

urlpatterns = [
    path('', views.home, name='home'),
    path('alquiler/', views.alquiler, name='alquiler'),
    path('signin/', views.signin, name='signin'),
    path('signup/', views.signup, name='signup'),
    path('ver/', views.mi_vista, name='ver'),
]