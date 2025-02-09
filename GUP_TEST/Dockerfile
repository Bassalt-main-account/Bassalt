# Usamos Python 3.11
FROM python:3.11

# Establecemos el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiamos las dependencias
COPY requirements.txt requirements.txt

# Instalamos las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copiamos el código de la aplicación
COPY . .

# Exponemos el puerto 8000
EXPOSE 8000

# Ejecutamos FastAPI con Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
