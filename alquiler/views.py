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
import mysql.connector
from django.conf import settings

# Create your views here.
def home(request):
    #actores = Actor.objects.all()
    return render(request, 'home.html')

#@login_required
def alquiler(request):
    #peliculas = Pelicula.objects.all()
    return render(request, 'alquiler.html',)

def signin(request):
    if request.method == 'GET':
        return render(request, 'signin.html', {'form': AuthenticationForm} )
    else:
        user = authenticate(
            request, username=request.POST['username'], password=request.POST['password'])
        
        if user is None:
            return render(request, 'signin.html', {
                'form': AuthenticationForm, 'error': 'Nombre de usuario o contraseña incorrectos'
            })
        else:
            login(request, user)
            return redirect('home')

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
   
def admin(request):
    img_random = random.randint(1, 10)
    peliculas = obtener_datos()
    return render(request, 'administrador.html', {'peliculas': peliculas, 'img_random':img_random})


def agregar_pelicula(request):
    try:
        conexion = mysql.connector.connect(
            host=settings.DATABASES['default']['HOST'],
            user=settings.DATABASES['default']['USER'],
            password=settings.DATABASES['default']['PASSWORD'],
            database=settings.DATABASES['default']['NAME'],
            port=settings.DATABASES['default']['PORT']
        )
        cursor = conexion.cursor()
    except mysql.connector.Error as err:
        print(f"Error de conexión: {err}")
        return render(request, "error.html", {"mensaje": "Error de conexión a la base de datos."})

    pelicula_form = PeliculaForm(request.POST or None)

    if request.method == 'POST':
        if pelicula_form.is_valid():
            pelicula_data = pelicula_form.cleaned_data
            print(pelicula_data)  # Mostrar los datos en la consola

            try:
                # Insertar el director
                director_query = """
                    INSERT INTO Director (Nombre, Nacionalidad) 
                    VALUES (%s, %s)
                    ON DUPLICATE KEY UPDATE ID_Director = LAST_INSERT_ID(ID_Director);
                """
                director_data = (
                    pelicula_data['Director'],
                    pelicula_data['Nacionalidad_Director']
                )
                cursor.execute(director_query, director_data)
                print("Director insertado o actualizado.")

                # Obtener el ID del director
                id_director = cursor.lastrowid
                print(f"ID del director: {id_director}")

                # Insertar la película
                query_pelicula = """
                    INSERT INTO Pelicula (Titulo, Fecha, Nacionalidad, Productora, ID_Director) 
                    VALUES (%s, %s, %s, %s, %s)
                """
                datos_pelicula = (
                    pelicula_data['Titulo'],
                    pelicula_data['Fecha'],
                    pelicula_data['Nacionalidad'],
                    pelicula_data['Productora'],
                    id_director
                )
                cursor.execute(query_pelicula, datos_pelicula)
                print("Película insertada.")

                # Obtener el ID de la película recién insertada
                id_pelicula = cursor.lastrowid

                # Insertar el actor
                query_actor = """
                    INSERT INTO Actor (Nombre, Nacionalidad, Sexo) 
                    VALUES (%s, %s, %s)
                """
                actor_data = (
                    pelicula_data['Actor_Nombre'],
                    pelicula_data['Actor_Nacionalidad'],
                    pelicula_data['Actor_Sexo']
                )
                cursor.execute(query_actor, actor_data)
                print("Actor insertado.")

                conexion.commit()  # Confirmar los cambios
                print("Cambios confirmados.")
            except mysql.connector.Error as e:
                print(f"Error al insertar en la base de datos: {e}")
                conexion.rollback()  # Deshacer cambios en caso de error

    cursor.close()
    conexion.close()

    return render(request, "agregar_pelicula.html", {
        "pelicula_form": pelicula_form,
    })

