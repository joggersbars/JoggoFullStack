// Función para obtener el parámetro "id_partida" de la URL
function getIdPartidaFromURL() {
    const urlParams = new URLSearchParams(window.location.search);
    const id_partida = urlParams.get("id_partida")
    const apodoJugador = urlParams.get("apodo_jugador")
    return {id_partida, apodoJugador}; // Obtenemos el valor de id_partida que viene como parametro desde la URL
}

// Rellenar el campo id_partida si existe en la URL
document.addEventListener("DOMContentLoaded", function() {
    const data = getIdPartidaFromURL();
    if (data.id_partida && data.apodoJugador) {
        document.getElementById("id_partida").value = data.id_partida; // Rellenar el campo con el id_partida si viene desde el QR
        document.getElementById("apodo_jugador").value = data.apodoJugador 
    }

    // Asignar el evento de clic al botón "ENTRAR"
    const entrarBtn = document.getElementById("entrar-btn");
    entrarBtn.addEventListener("click", async function() {
        // Obtener los valores de los campos
        const id_partida = document.getElementById("id_partida").value;
        const apodoJugador = document.getElementById("apodo_jugador").value;
        const fraseJugador = document.getElementById("frase_usuario").value;

        const codigo_juego = id_partida 
        const apodo_jugador = apodoJugador
        const frase_jugador = fraseJugador

        const data = { codigo_juego, apodo_jugador, frase_jugador }

         // Loggear los datos que se están enviando
        console.log('Enviando datos al servidor:', data);

        try {   
            // Enviar la solicitud POST al servidor Python (Flask)
            //console.log('Iniciando solicitud al backend...',apiUrl);
            const response = await fetch('http://localhost:8002/anadiendo_frase', {  //${apiUrl}
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
                if (result.message.includes('Frase añadida correctamente')) {
                    // Redirigir a la pantalla /games si la autenticación fue exitosa
                    console.log('Autenticación exitosa. Redirigiendo a /espera_jugador...');
                    window.location.href = `/yonunca_jugador.html?id_partida=${id_partida}&apodo_jugador=${apodoJugador}`;
                } else if (result.message.includes('Esa frase ya está cogida')) {
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


