// Obtenemos el id_partida de la URL
function getIdPartidaFromURL() {
    const urlParams = new URLSearchParams(window.location.search);
    return urlParams.get("id_partida");
}
const id_actual_partida = getIdPartidaFromURL();

// URL actual
const currentUrl = window.location.href;

// Verifica si el temporizador ha terminado
async function checkAllphrasesDoneStart() {
    const response = await fetch(`${API_URL}/game/status/${id_actual_partida}`);
    const data = await response.json();
    
    if (data.estado === "frases") {
        window.location.href = currentUrl.replace("espera_frases_jugador.html", "yonunca_jugador.html");
    }
}

// Ejecuta la verificación cada 300 milisegundos
setInterval(checkAllphrasesDoneStart, 100);
