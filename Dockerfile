# Usa una imagen base oficial de Python
FROM python:3.11-slim

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia los archivos del proyecto al contenedor
COPY ./requirements.txt /app/requirements.txt
# Instala las dependencias
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

# Evita que Python haga buffering de logs
ENV PYTHONUNBUFFERED=1

# Expone el puerto en el que Flask correrá (por defecto 5000)
EXPOSE 5050

# Define la variable de entorno para que Flask se ejecute correctamente
ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0

# Comando para correr la aplicación
CMD ["python", "app.py"]