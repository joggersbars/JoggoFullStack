# Usar una imagen base de Python
FROM python:3.9-slim

# Establecer el directorio de trabajo
WORKDIR /app

# Copiar el archivo de requisitos
COPY requirements.txt .

# Instalar las dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copiar todo el código del backend
COPY . .

# Exponer el puerto en el que corre la aplicación (8000 por defecto para Uvicorn)
EXPOSE 8002

# Comando para ejecutar la aplicación usando Uvicorn
CMD ["python", "Run.py"]
