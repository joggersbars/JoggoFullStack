// Obtenemos parametros de la URL
const urlParams = new URLSearchParams(window.location.search);
const apodo_jugador = urlParams.get('apodo_jugador');
const id_partida = urlParams.get('id_partida');


// Función para MOSTRAR los datos del jugador en pantalla
function mostrarDatosJugador(data) {
    // Cambiar el título
    document.querySelector('.titulo-final').textContent = `Final de la partida de ${data.nombreJugador}`;
    
    // Formatear el resultado para que se muestre como "5/20" (frases pulsadas / frases totales)
    document.querySelector('.mensaje-final').innerHTML = `
        <span class="frases-pulsadas">${data.result}</span>
        <span class="separador">/</span>
        <span class="frases-totales">${data.frases_totales}</span>
    `;
}


// Función para obtener datos del jugador desde el backend
async function obtenerDatosJugador() {
    if (!idUsuario) {
        console.error("ID de usuario no encontrado en la URL");
        document.querySelector('.mensaje-final').textContent = "Error: No se pudo obtener la información del jugador.";
        return;
    }

    try {
        // Realizar la solicitud al backend
        const response = await fetch(`${API_URL}/resultado_jugador/${id_partida}/${apodo_jugador}`);
        if (!response.ok) throw new Error("Error al obtener los datos del jugador");

        const result = await response.json();
        mostrarDatosJugador(result); // Mostrar los datos en la pantalla
    } catch (error) {
        console.error("Error:", error);
        document.querySelector('.mensaje-final').textContent = "Error al cargar los datos del jugador.";
    }
}

// Llamamos a la función para obtener los datos del jugador
obtenerDatosJugador();