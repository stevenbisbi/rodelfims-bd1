from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from mysql.connector import Error
from django.db import IntegrityError
from django.db import connection
from django.http import JsonResponse
from .forms import PeliculaForm, SocioForm
import random
from django.contrib import messages
import mysql.connector
from django.conf import settings
from functools import wraps

#decorador
def with_db_connection(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        try:
            conexion = mysql.connector.connect(
                host=settings.DATABASES['default']['HOST'],
                user=settings.DATABASES['default']['USER'],
                password=settings.DATABASES['default']['PASSWORD'],
                database=settings.DATABASES['default']['NAME'],
                port=settings.DATABASES['default']['PORT']
            )
            cursor = conexion.cursor()
            kwargs['cursor'] = cursor
            kwargs['conexion'] = conexion
        except mysql.connector.Error as err:
            print(f"Error de conexión: {err}")
            return render(request, "error.html", {"mensaje": "Error de conexión a la base de datos."})

        response = view_func(request, *args, **kwargs)
        cursor.close()
        conexion.close()
        return response

    return wrapper



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
@with_db_connection
def signup(request, *args, **kwargs):
    cursor = kwargs.get('cursor')
    conexion = kwargs.get('conexion')

    # Obtener la lista de socios al inicio
    cursor.execute("SELECT DNI, Nombre FROM Socio")
    socios = cursor.fetchall()

    # Inicializar el formulario
    socioForm = SocioForm(request.POST or None, socios=socios)

    if request.method == 'POST':
        print(f"Método de solicitud: {request.method}")
        if request.POST['password1'] == request.POST['password2']:
            if socioForm.is_valid():
                print('formularo valido')
                try:
                    dni = socioForm.cleaned_data['Dni']
                    # Validar si ya existe el socio
                    cursor.execute("SELECT DNI FROM Socio WHERE DNI = %s", (dni,))
                    resultado = cursor.fetchall()

                    if not resultado:
                        print('socio no existe')
                        # Crear el usuario usando correo como username
                        user = User.objects.create_user(
                        username=socioForm.cleaned_data['email'],
                        email=socioForm.cleaned_data['email'],
                        password=request.POST['password1']
                        )
                        print('usuario insertado')
                        socio_query = """
                        INSERT INTO Socio (DNI, Nombre, Direccion, Telefono, Avalado_por, usuario_id) 
                        VALUES (%s, %s, %s, %s, %s, %s)
                        """
                        socio_data = (
                            socioForm.cleaned_data['Dni'],
                            socioForm.cleaned_data['Nombre'],
                            socioForm.cleaned_data['Direccion'],
                            socioForm.cleaned_data['Telefono'],
                            socioForm.cleaned_data['Avalado_por'],
                            user.id  # Aquí guardas el ID del usuario recién creado
                        )
                        print(f"Consulta: {socio_query}")
                        print(f"Datos enviados: {socio_data}")

                        try:
                            cursor.execute(socio_query, socio_data)
                            conexion.commit()
                            print("Socio insertado.")
                        except Exception as e:
                            conexion.rollback()
                            print(f"Error al insertar en la base de datos: {e}")
                            messages.error(request, f"Error SQL: {str(e)}")
                        print("Socio insertado.")
                        user.save()
                        login(request, user)
                        return redirect('home')  # Redirigir a la página principal
                    else:
                        messages.error(request, "El socio con este DNI ya está registrado.")
                        print('socio no insertado')
                except Error as e:
                    conexion.rollback()  # Revertir cambios en caso de error
                    messages.error(request, f"Error al registrar: {str(e)}")
            else:
                print(f"Errores en el formulario: {socioForm.errors}")
        else:
            messages.error(request, 'Las contraseñas ingresadas no coinciden.')

    return render(request, 'signup.html', {'form': socioForm, 'socios': socios})


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

def obetener_detalles():
    try:
        cursor = connection.cursor()
        cursor.execute('''
                SELECT 
                    P.ID_Pelicula,
                    P.Titulo,
                    P.Nacionalidad,
                    P.Productora,
                    P.Fecha,
                    D.Nombre AS Director,
                    GROUP_CONCAT(A.Nombre || CASE WHEN PA.Principal THEN ' (Principal)' ELSE '' END SEPARATOR ', ') AS Actores,
                    E.ID_Ejemplar,
                    E.Estado_Conservación,
                    CASE 
                        WHEN COUNT(AL.ID_Ejemplar) > 0 AND MAX(AL.Fecha_devolucion) IS NULL THEN 'No Disponible'
                        ELSE 'Disponible'
                    END AS Disponibilidad
                FROM Pelicula P
                LEFT JOIN Director D ON P.ID_Director = D.ID_Director
                LEFT JOIN Pelicula_Actor PA ON P.ID_Pelicula = PA.ID_Pelicula
                LEFT JOIN Actor A ON PA.ID_Actor = A.ID_Actor
                LEFT JOIN Ejemplar E ON P.ID_Pelicula = E.ID_Pelicula
                LEFT JOIN Alquiler AL ON E.ID_Ejemplar = AL.ID_Ejemplar
                GROUP BY 
                    P.ID_Pelicula, 
                    E.ID_Ejemplar, 
                    P.Titulo, 
                    P.Nacionalidad, 
                    P.Productora, 
                    P.Fecha, 
                    D.Nombre, 
                    E.Estado_Conservación
                LIMIT 1000;
            ''')
        columns = [col[0] for col in cursor.description]  # Nombres de las columnas
        datos = [dict(zip(columns, row)) for row in cursor.fetchall()]
        print(datos)  # Imprime los datos para verificar
        return datos
    except Exception as e:
        print(f"Error al obtener datos: {e}")
        return []
    
def peliculas(request):
    img_random = random.randint(1, 10)
    detalles = obetener_detalles()
    return render(request, 'alquiler.html', {'peliculas': peliculas, 'detalles':detalles})
   
def admin(request):
    img_random = random.randint(1, 10)
    peliculas = obtener_datos()
    return render(request, 'administrador.html', {'peliculas': peliculas, 'img_random':img_random})

@with_db_connection
def agregar_pelicula(request, cursor, conexion):
    pelicula_form = PeliculaForm(request.POST or None)

    if request.method == 'POST':
        if pelicula_form.is_valid():
            pelicula_data = pelicula_form.cleaned_data
            print(pelicula_data)  # Mostrar los datos en consola

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

                # Confirmar los cambios en la base de datos
                conexion.commit()
                print("Cambios confirmados.")
                messages.success(request, "Película agregada con éxito.")
            except mysql.connector.Error as e:
                print(f"Error al insertar en la base de datos: {e}")
                conexion.rollback()  # Deshacer los cambios en caso de error

    return render(request, "agregar_pelicula.html", {"pelicula_form": pelicula_form})

def borrar_pelicula(request, id_pelicula):
    if request.method == 'POST':
        try:
            # Conectar a la base de datos
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
            messages.error(request, "Error de conexión a la base de datos.")
            return redirect('administrador')

        try:
            # Eliminar relaciones si es necesario
            query_relacion = "DELETE FROM Película_Actor WHERE ID_Pelicula = %s;"
            cursor.execute(query_relacion, (id_pelicula,))

            # Eliminar la película
            query_pelicula = "DELETE FROM Pelicula WHERE ID_Pelicula = %s;"
            cursor.execute(query_pelicula, (id_pelicula,))

            conexion.commit()  # Confirmar los cambios
            messages.success(request, "Película eliminada con éxito.")
        except mysql.connector.Error as e:
            print(f"Error al eliminar: {e}")
            conexion.rollback()  # Deshacer cambios en caso de error
            messages.error(request, "Error al eliminar la película.")

        cursor.close()
        conexion.close()

        # Redirigir a la página anterior o a otra
        return redirect('administrador')

    return redirect('administrador') # Si no es POST, redirige al inicio.