# Usar una imagen base de Node.js
FROM node:14

# Establecer el directorio de trabajo
WORKDIR /app

# Copiar los archivos de dependencias
COPY package*.json ./

# Instalar las dependencias
RUN npm install

# Copiar el resto del código del frontend
COPY . .

# Exponer el puerto en el que corre tu servidor (por defecto 3000)
EXPOSE 8001

# Iniciar tu servidor Node.js
CMD ["npm", "start"]
