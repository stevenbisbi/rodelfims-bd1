Rodelfims 🎥

Descripción del Proyecto

Rodelfims es una plataforma de gestión de películas y alquileres desarrollada como un proyecto académico, que incluye tanto el backend como la base de datos desplegados en producción. Permite a los usuarios explorar películas, gestionar alquileres y realizar operaciones administrativas mediante un sistema CRUD.

🚀 Tecnologías Utilizadas

Django: Framework web backend para gestionar la lógica del negocio y formularios.


MySQL: Sistema de gestión de bases de datos para almacenar películas, usuarios, y alquileres.


Bootstrap: Estilo frontend responsivo para mejorar la interfaz de usuario.


Railway: Plataforma utilizada para el despliegue del proyecto en producción.


GitHub: Control de versiones y colaboración del equipo.


🌐 Acceso al Proyecto

Aplicación Web: Rodelfims

Repositorio GitHub: stevenbisbi/rodelfims-bd1

📂 Estructura del Proyecto

Controladores: En views.py se encuentran las funciones para las operaciones.

Formularios: Desarrollados con la biblioteca forms de Django.

Consultas SQL:

Dentro de los controladores para gestionar datos manualmente.

🔑 Autenticación

Se utiliza el modelo AUTH_USER de Django para manejar los usuarios y la autenticación en la plataforma.


⚙️ Funcionalidades Principales

Películas (Sin sesión):

Muestra todas las películas disponibles en la base de datos.

Alquiler (Con sesión):

Muestra únicamente las películas disponibles para alquilar.

Administrador (Con sesión):

Visualiza los alquileres registrados.

CRUD completo: Agregar, actualizar y eliminar películas.
