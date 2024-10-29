# Usa una imagen base de Python
FROM python:3.10

# Establece el directorio de trabajo dentro del contenedor
WORKDIR /app

# Copia el código de la aplicación
COPY . .

# Copia el archivo de requisitos y las instala
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Exponer el puerto que usará la aplicación
EXPOSE 8002

# Ejecutar Uvicorn con la aplicación de FastAPI
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8002"]