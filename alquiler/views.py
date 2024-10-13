from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.db import connection

# Create your views here.
def home(request):
    #actores = Actor.objects.all()
    return render(request, 'home.html')

#@login_required
def alquiler(request):
    #peliculas = Pelicula.objects.all()
    return render(request, 'alquiler.html',)

def signin(request):
    return render(request, 'signin.html')

def signup(request):
    if request.method == 'GET':
        return render(request, 'signup.html')
    else:
        if request.POST['password1'] == request.POST['password2']:
            #registrar usuario
            try:
                user = User.objects.create_user(username=request.POST['username'], password=request.POST['password1'])
                user.save() #guarda el ususario en el modelo
                login(request, user)
                return redirect('home')
            except IntegrityError:
                return render(request, 'signup.html', {'form': UserCreationForm, 'error': 'username already exists'})
        return render(request, 'signup.html', {'form': UserCreationForm, 'error': 'Nombre de usuario o contraseña incorrectos'})

@login_required 
def signout(request):
    logout(request)
    return redirect('home')

def obtener_datos():
    with connection.cursor() as cursor:
        # Ejecutar una consulta SQL
        cursor.execute("SELECT * FROM django_content_type;")
        
        # Obtener los resultados
        resultados = cursor.fetchall()

    return resultados

from django.http import JsonResponse

def mi_vista(request):
    datos = obtener_datos()
    return JsonResponse(datos, safe=False)
