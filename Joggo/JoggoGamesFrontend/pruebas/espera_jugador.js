// Obtenemos el id_partida de la URL
function getIdPartidaFromURL() {
    const urlParams = new URLSearchParams(window.location.search);
    return urlParams.get("id_partida");
}
const id_actual_partida = getIdPartidaFromURL();

// URL actual
const currentUrl = window.location.href;

// Verifica si el juego ha comenzado mediante un llamado al backend
const intervalId = setInterval(async () => {
    try {
        const response = await fetch(`${API_URL}/game/status/${id_actual_partida}`);
        const data = await response.json();
        
        if (data.estado === "comenzado") {
            clearInterval(intervalId); // Detiene el intervalo para que no se ejecute más
            window.location.href = currentUrl.replace("espera_jugador.html", "frase_jugador.html");
        }
    } catch (error) {
        console.error("Error al verificar el estado del juego:", error);
    }
}, 3000);

// Verifica si el temporizador ha terminado
async function checkAllphrasesDoneStart() {
    const response = await fetch(`${API_URL}/game/status/${id_actual_partida}`);
    const data = await response.json();
    
    if (data.estado === "mostrar_frases") {
        window.location.href = currentUrl.replace("espera_jugador.html", "yonunca_jugador.html");
    }
}

// Ejecuta la verificación cada 300 milisegundos
setInterval(checkAllphrasesDoneStart, 300);
