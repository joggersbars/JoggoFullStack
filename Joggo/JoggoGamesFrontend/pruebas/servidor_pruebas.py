from flask import Flask, request, jsonify,  send_from_directory
from flask_cors import CORS  # Importar CORS
import os
import logging

# Configurar el logger
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

app = Flask(__name__)
CORS(app)  # Habilitar CORS para todas las rutas

# Ruta para manejar la autenticación
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()  # Recibimos los datos enviados en formato JSON
    username = data.get('username')
    password = data.get('password')

      # Registrar la solicitud (lo que se envía)
    logging.info(f"Datos recibidos: Usuario: {username}, Contraseña: {password}")

    # Ejemplo simple de autenticación (normalmente, deberías validar con una base de datos)
    if username == 'admin' and password == 'admin':                                                 #configuracion de credenciales segun usuario --> hacerlo para BBDD
        return jsonify({'message': f'Bienvenido, {username}!'}), 200
    else:
        logging.info("Autenticación fallida para el usuario: " + username)  # Registrar intentos fallidos
        return jsonify({'message': 'Credenciales incorrectas'}), 401  # 401 es el código de no autorizado

@app.route('/games')
def games():
    directory = directory = r'C:\Users\Vito\Documents\GitHub\JoggoFullStack\Joggo\JoggoGames_Frontend-main\public\Recursos'
    return send_from_directory(directory, 'games.html')
# Ruta para manejar la creación de una partida

@app.route('/crear_partida', methods=['GET'])
def crear_partida():
    # Obtener el nombre del juego desde los parámetros de la solicitud
    game_name = request.args.get('game_name', 'Desconocido')
    
    # Generar un id_partida y url_partida
    id_partida = random.randint(1000, 9999)  # ID de partida aleatorio
    url_partida = f"http://localhost:8001/{game_name.lower().replace(' ', '_')}_{id_partida}"

    # Log para depuración
    print(f"Creando partida: La partida de {game_name} tiene ID {id_partida} y URL {url_partida}")

    # Devolver los datos de la partida como respuesta JSON
    response = {
        'id_partida': id_partida,
        'url_partida': url_partida
    }

    return jsonify(response), 200

# Endpoint dinamico para cargar la página de "pantalla_user" donde se identificara el user y donde el QR apuntará
@app.route('/partida_<int:id_partida>', methods=['GET']) # --> cuando se reciba un Get /partida_{id_partida} mandamos al usuario a la pantalla /partida
def partida(id_partida):
    # Renderizar una plantilla HTML para la partida específica
    directory = r'C:\Users\Vito\Documents\GitHub\JoggoGames_Frontend\public\Recursos'
    return send_from_directory(directory, 'partida.html')

if __name__ == '__main__':
    app.run(debug=True, port=5000)

