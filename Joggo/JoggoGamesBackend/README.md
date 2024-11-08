# JoggoGames

**1**.- To use Makefile and execute scripts in windows use the following command ($ se usa para interpretar que esa línea se ejecuta en el powershell de windows)

   - Haz clic derecho en "Windows PowerShell" y selecciona "Ejecutar como administrador".
   - Si aparece una ventana de Control de Cuentas de Usuario (UAC), haz clic en "Sí" para otorgar permisos de administrador.
   - Ejecuta el siguiente comando para permitir la ejecución de scripts:
      '$Set-ExecutionPolicy Bypass -Scope Process -Force'
   - Ejecuta el siguiente comando para instalar Chocolatey:
      '$[System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))'
   - Ahora que tienes Chocolatey instalado, puedes instalar Make ejecutando:
      '$choco install make'
   - Ahora desde el PowerShell instalar las dependencias con Make haciendo cd a la ruta del proyecto:
      '$cd C:\ruta\de\tu\proyecto'
      '$make create-environment'

**2**.- To access al SWAGGER UI http://127.0.0.1:8000/docs

**3**.- To create a docker container with the database use the following commands in terminal:
   $ docker load -i database_joggo.tar
   $ docker run --name db -d database_joggo

**4**.- Para correr la base de datos seguir los siguiente comandos:
   - Tener el contenedor corriendo en docker desktop.
   - Escribir en terminal:
      * $ docker exec -it db bash
   - Cuando entre os ponda a la izquierda `mysql>`, ejecutar el siguiente comando:
      * `mysql>` mysql - p
      * Introduce password: 12345
   - Escoger base de datos que estamos usando, en este caso se llama `test`: 
       `mysql>` use test;
   - Mostrar tablas:
       `mysql>` show tables;
   - Tenemos 4 <tablas>:
      * `juego`: Almacena el id partida, el juego que se está jugando, y el número de jugadores (esto está pendiente de arreglar)
      * `jugadores`: Almacena apodo del jugador, id de la partida, frase jugador y el id de la frase.
      * `respuestas`: Almacena id partida, apodo jugador, frase jugador y respuesta jugador (Cantidad de síes que el jugador dice).
      * `users`: Almacena el username del bar y el password del bar (pantalla de login)
   - Si queremos acceder a las tablas y verlas usar:
       `mysql>` select * from <tabla>;
   - Si queremos ver información de los tipos de las variables:
       `mysql>` describe <tabla>;     



