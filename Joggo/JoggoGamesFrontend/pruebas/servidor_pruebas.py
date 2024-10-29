from flask import Flask, request, jsonify
from flask_cors import CORS  # Importar CORS
import os
import random
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

@app.route('/crear_partida/Yo_nunca', methods=['GET'])
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

    print(f"La ID dentro de respuesta es {response['id_partida']}")

    return jsonify(response), 200

@app.route('/empezar_partida', methods=['POST'])
def empezar_partida():
    data = request.get_json()  # Obtener el JSON del cuerpo de la solicitud
    mensaje = data.get('mensaje_inicio')
    id_partida = data.get('codigo_partida')

    # Aquí podrías añadir lógica para manejar el inicio de la partida
    print(f"Mensaje recibido: {mensaje}")
    print(f"ID de la partida para comenzar: {id_partida}")

    # Devolvemos una respuesta de éxito
    return jsonify({'status': 'Partida iniciada', 'id_partida': id_partida}), 200

# Ruta para servir las páginas HTML desde /public/Recursos
# @app.route('/<path:filename>')
# def serve_html(filename):
#     directory = os.path.join(os.getcwd(), 'JoggoGamesFrontend/public/Recursos')
#     return send_from_directory(directory, filename)


# Endpoint dinamico para cargar la página de "pantalla_user" donde se identificara el user y donde el QR apuntará
#@app.route('/partida_<int:id_partida>', methods=['GET']) # --> cuando se reciba un Get /partida_{id_partida} mandamos al usuario a la pantalla /partida
#def partida(id_partida):
    # Renderizar una plantilla HTML para la partida específica
 #   directory = r'C:\Users\Vito\Documents\GitHub\JoggoGames_Frontend\public\Recursos'
 #   return send_from_directory(directory, 'partida.html')

if __name__ == '__main__':
    app.run(debug=True, port=5000)

