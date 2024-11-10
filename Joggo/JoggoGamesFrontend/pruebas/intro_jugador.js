import { API_URL } from './config'

// Función para obtener el parámetro "id_partida" de la URL
function getIdPartidaFromURL() {
    const urlParams = new URLSearchParams(window.location.search);
    return urlParams.get("id_partida"); // Obtenemos el valor de id_partida que viene como parametro desde la URL
}

// Rellenar el campo id_partida si existe en la URL
document.addEventListener("DOMContentLoaded", function() {
    const idPartida = getIdPartidaFromURL();
    if (idPartida) {
        document.getElementById("id_partida").value = idPartida; // Rellenar el campo con el id_partida si viene desde el QR
    }

    // Asignar el evento de clic al botón "ENTRAR"
    const entrarBtn = document.getElementById("entrar-btn");
    entrarBtn.addEventListener("click", async function() {
        // Obtener los valores de los campos
        const id_partida = document.getElementById("id_partida").value;
        const apodo_jugador = document.getElementById("apodo_jugador").value;

        const data = { id_partida, apodo_jugador }

         // Loggear los datos que se están enviando
        console.log('Enviando datos al servidor:', data);

        try {   
            //console.log('Iniciando solicitud al backend...',apiUrl);
            const response = await fetch(`${API_URL}/crear_jugador`, {  //${apiUrl}
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data) // Convertir los datos a JSON para enviarlos
            });
    
            // Loggear el estado de la respuesta del servidor
            console.log('Respuesta del servidor (status):', response.status);
            // Procesar la respuesta del servidor
            // Procesar la respuesta del servidor
            if (response.ok) {
                const result = await response.json();
                // Loggear el mensaje recibido del servidor
                console.log('Mensaje recibido del servidor:', result.message);
    
                // Comprobar si el mensaje es "Bienvenido"
                if (result.message.includes('Jugador conectado correctamente')) {
                    // Redirigir a la pantalla /games si la autenticación fue exitosa
                    console.log('Autenticación exitosa. Redirigiendo a /espera_jugador...');
                    window.location.href = `/espera_jugador.html?id_partida=${id_partida}&apodo_jugador=${apodo_jugador}`;
                } else if (result.message.includes('El nombre del jugador ya existe')) {
                    alert('Error de autenticación: ' + result.message); // Mostrar el mensaje de error
                }
            } else {
                alert('Error de autenticación: ' + response.statusText); // Mostrar error si la autenticación falla
            }
        } catch (error) {
            console.error('Error al conectar con el servidor:', error);
            alert('Hubo un problema al conectar con el servidor.');
        }
    });
});


