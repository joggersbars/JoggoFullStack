// Obtenemos el id_partida de la URL
function getIdPartidaFromURL() {
    const urlParams = new URLSearchParams(window.location.search);
    id_partida = urlParams.get("id_partida")
    apodo_jugador = urlParams.get("apodo_jugador")
    return { id_partida, apodo_jugador };
}

// URL actual
const currentUrl = window.location.href;

// Verifica si el juego ha comenzado mediante un llamado al backend
async function checkGameStart() {

    const { id_actual_partida, apodo_jugador } = getIdPartidaFromURL();
    const response = await fetch(`${API_URL}/game/status/${id_actual_partida}`);
    const data = await response.json();
    
    if (data.estado === "comenzado") {
        window.location.href = currentUrl.replace("espera_jugador.html", "frase_jugador.html");
        const response_jugador_connected = await fetch(`${API_URL}/game/is_jugador_connected/${id_partida_actual}/${apodo_jugador}`,{
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            },
        });

        data_jugador_connected = await response_jugador_connected.json()
        if (data_jugador_connected.connected == false){
            const response_conect = await fetch(`${API_URL}/game/jugador_conectado/${id_partida_actual}/${apodo_jugador}`,{
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
            });
        }
        
        const response_all_connected = await fetch(`${API_URL}/game/all_connected/${id_partida_actual}`,{
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            },
        }); 
        data = await response_all_connected.json()
        if (data.connected) {
            response = await fetch(`${API_URL}/game/pause/${id_actual_partida}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
            });
        }
    }
}

// Verifica si el temporizador ha terminado
async function checkAllphrasesDoneStart() {
    const response = await fetch(`${API_URL}/game/status/${id_actual_partida}`);
    const data = await response.json();
    
    if (data.estado === "mostrar_frases") {
        window.location.href = currentUrl.replace("espera_jugador.html", "yonunca_jugador.html");
    }
}

// Ejecuta la verificación cada 300 milisegundos
setInterval(checkGameStart, 30);
setInterval(checkAllphrasesDoneStart, 300);
