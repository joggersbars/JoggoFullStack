# JoggoGames_Frontend
 Repositorio de almacenamiento de los archivos relacionados con el Front-end

- Necesario instalar en la maquina Windows Node.js (npm viene integrado)
- https://nodejs.org/en
- Ejecutamos el .exe para que instale las depedencias necesarias 
- Reiniciamos el ordenador

1.- Creacion del entorno y dependencias
    
    - npm run setup    # Ejecuta la instalación y arranca el servidor

2.- Como cargar el servidor de pruebas Back-end:
    - Ir al directorio /Joggo/JoggoGamesFrontend/pruebas
        > cd /Joggo/JoggoGamesFrontend/pruebas
        > py.exe servidor_pruebas.py 
        (Instalar las librerias pertinentes para que se ejecute correctamente)
    - NOTA: TENER EN CUENTA QUE LA DIRECCION DE ESTE SERVIDOR ES http://localhost:5000 (no es el mismo que el que vamos a tener en realidad)

3.- Conceptos: 

    - Biblioteca Axios:  Biblioteca de JavaScript que se usa para realizar solicitudes HTTP desde el navegador o desde Node.js.Se utiliza para hacer llamadas a APIs (por ejemplo, para conectarse a un back-end y obtener o enviar datos).
    - "start": "live-server publico" --> Crea un servidor de pruebas en http://127.0.0.1:8080 --> pasado a servidor en local "server.js"

