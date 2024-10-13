# Usa una imagen base de Python
FROM python:3.11-slim

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Instala las dependencias del sistema necesarias para mysqlclient
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    pkg-config \         
    default-libmysqlclient-dev \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copia los archivos del proyecto al contenedor
COPY . .

# Crea y activa un entorno virtual
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Instala las dependencias de Python
RUN pip install --upgrade pip \
    && pip install -r requirements.txt

# Expone el puerto que usará la app
EXPOSE 8000
# Ejecuta collectstatic sin interacción
RUN python manage.py collectstatic --noinput

# Comando de inicio para la aplicación
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "rodelfims.wsgi:application"]
