// Función para obtener los parámetros "id_partida" y "apodo_jugador" de la URL
function getParamsFromURL() {
    const urlParams = new URLSearchParams(window.location.search);
    const id_partida = urlParams.get("id_partida");
    const apodo_jugador = urlParams.get("apodo_jugador");
    console.log("id_partida:", id_partida);
    console.log("apodo_jugador:", apodo_jugador);
    return { id_partida, apodo_jugador };
}

// Rellenar el campo id_partida si existe en la URL
document.addEventListener("DOMContentLoaded", function() {
    const { id_partida, apodo_jugador } = getParamsFromURL();

    // Asignar el evento de clic al botón "Enviar"
    const entrarBtn = document.getElementById("entrar-btn");
    entrarBtn.addEventListener("click", async function() {
        // Obtener los valores de los campos
        const frase_jugador = document.getElementById("frase_usuario").value; //almacenamos la frase para enviar al servidor BackEnd

        // Crear el objeto de datos para enviar
        const data = { id_partida, apodo_jugador, frase_jugador };

        console.log('Enviando datos al servidor:', data);

        try {
            // Enviar la solicitud POST al servidor
            const response = await fetch(`${API_URL}/añadir_frase`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data) // Convertir los datos a JSON para enviarlos
            });

            if (response.ok) {
                const result = await response.json();
                console.log('Mensaje recibido del servidor:', result.message);
                //Si todo ha ido bien --> servidor BackEnd aprueba continuar la ejecucion
                if (result.message.includes('Frase añadida correctamente')) {
                    console.log('Frase añadida exitosamente.');
                    window.location.href = `/espera_jugador.html?id_partida=${id_partida}&apodo_jugador=${apodo_jugador}`;
                } else {
                    alert('Error: ' + result.message);
                }
            } else {
                alert('Error: ' + response.statusText);
            }
        } catch (error) {
            console.error('Error al conectar con el servidor:', error);
            alert('Hubo un problema en la respuesta dl servidor.');
        }
    });
});
