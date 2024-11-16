// Obtenemos parametros de la URL
const urlParams = new URLSearchParams(window.location.search);
const apodo_jugador = urlParams.get('apodo_jugador');
const id_partida = urlParams.get('id_partida');


// Función para MOSTRAR los datos del jugador en pantalla
function mostrarDatosJugador(result) {
    // Cambiar el título
    document.querySelector('.titulo-final').textContent = `Final de la partida de ${apodo_jugador}`;
    
    // Formatear el resultado para que se muestre como "5/20" (frases pulsadas / frases totales)
    document.querySelector('.mensaje-final').innerHTML = `
        <span class="frases-pulsadas"> ${result.result}></span>
        <span class="separador">/</span>
        <span class="frases-totales">${result.frases_totales}</span>`;
}

// Función para obtener datos del jugador desde el backend
async function obtenerDatosJugador() {
    if (!apodo_jugador || !id_partida) {
        console.error("Apodo o ID de partida del usuario no encontrado en la URL");
        document.querySelector('.mensaje-final').textContent = " Cargando datos....";
        return;
    }
    
    const url = `${API_URL}/resultado_jugador/${id_partida}/${apodo_jugador}`;
    console.log("URL para obtener datos:", url);
    try {
        // Realizar la solicitud al backend
        
        const response = await fetch(url, {
            method: 'GET', 
            mode: "cors",
            headers: {
                'Content-Type': 'application/json'
            }
        });

        // Verifica si la respuesta es un 404 (no encontrado)
        if (response.status === 404) {
            throw new Error("Datos no encontrados para el jugador o la partida.");
        }

        if (!response.ok) throw new Error("Error al obtener los datos del jugador");

        const result = await response.json();
        console.log("Datos recibidos:", result);
        mostrarDatosJugador(result); // Mostrar los datos en la pantalla
    } catch (error) {
        console.error("Error:", error);
        document.querySelector('.mensaje-final').textContent = "Error al cargar los datos del jugador.";
    }
}

// Llamamos a la función para obtener los datos del jugador
obtenerDatosJugador();