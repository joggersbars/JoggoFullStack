// Obtenemos el id_partida de la URL
function getIdPartidaFromURL() {
    const urlParams = new URLSearchParams(window.location.search);
    return urlParams.get("id_partida");
}
const id_actual_partida = getIdPartidaFromURL();

// URL actual
const currentUrl = window.location.href;

// Verifica si el juego ha comenzado mediante un llamado al backend
async function checkGameStart() {
    const response = await fetch(`${API_URL}/game/status/${id_actual_partida}`);
    const data = await response.json();
    
    if (data.estado === "comenzado") {
        window.location.href = currentUrl.replace("espera_jugador.html", "frase_jugador.html");
    }
}

// Ejecuta la verificación cada 300 milisegundos
setInterval(checkGameStart, 300);
