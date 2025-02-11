# Usa Python 3.11 como base
FROM python:3.11

# Establecer directorio de trabajo
WORKDIR /app

# Copiar e instalar dependencias primero (optimización de capas)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto del código después de instalar las dependencias
COPY . .

# Exponer el puerto 8000
EXPOSE 8000

# Ejecutar FastAPI con Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
