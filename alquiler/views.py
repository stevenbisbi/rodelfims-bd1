from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.db import connection
from django.http import JsonResponse
from .forms import PeliculaForm
import random

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
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM Pelicula")
        columns = [col[0] for col in cursor.description]  # Nombres de las columnas
        datos = [dict(zip(columns, row)) for row in cursor.fetchall()]
        print(datos)  # Imprime los datos para verificar
        return datos
    except Exception as e:
        print(f"Error al obtener datos: {e}")
        return []




def mi_vista(request):
    datos = obtener_datos()
    return JsonResponse(datos, safe=False)

def peliculas(request):
    img_random = random.randint(1, 10)
    peliculas = obtener_datos()
    return render(request, 'alquiler.html', {'peliculas': peliculas, 'img_random':img_random})
    
def menu(request):
    form = PeliculaForm()
    return render(request, 'administrador.html', {'form':form})