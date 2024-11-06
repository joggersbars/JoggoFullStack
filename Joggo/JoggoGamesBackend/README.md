# JoggoGames

1.- To use Makefile and execute scripts in windows use the following command ($ se usa para interpretar que esa línea se ejecuta en el powershell de windows)

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

2.- To access al SWAGGER UI http://127.0.0.1:8000/docs

3.- To create a docker container with the database use the following commands in terminal:
   $ docker load -i database_joggo.tar
   $ docker run --name db -d database_joggo

