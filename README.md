# JoggoFullStack
Frontend and Backend of Joggo
Para cargar todo el setup: 

    - Descargar docker desktop en windows o docker-compose en linux
    - cd C:\Users\Vito\Documents\GitHub\JoggoFullStack\Joggo
    - docker-compose up --build 

# Activacion de winSCP
    - Logearte en la cuenta de digitalOcean
    - Entrar en la consola web mediante usuario root
    - Entrar en configuracion ssh: sudo nano /etc/ssh/sshd_config
    - Habilitar con yes: 
            - 
            - # Configurar el acceso de root solo con clave pública
                        PermitRootLogin yes

            - # Deshabilitar acceso con contraseña
                        PasswordAuthentication no --> cambiar a si para habilitar clave

            - # Asegurar autenticación con clave pública
                        PubkeyAuthentication yes
                        KbdInteractiveAuthentication no --> habilitar a yes 

