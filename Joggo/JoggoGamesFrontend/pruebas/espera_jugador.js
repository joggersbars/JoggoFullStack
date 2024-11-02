function getIdPartidaFromURL() {
    const urlParams = new URLSearchParams(window.location.search);
    return urlParams.get("id_partida"); // Obtenemos el valor de id_partida que viene como parametro desde la URL
}
const id_actual_partida = getIdPartidaFromURL();


      // Obtener la URL actual
      const currentUrl = window.location.href;

        // Función para verificar si el juego ha comenzado
        async function checkGameStart() {
            const gameStarted = localStorage.getItem("ComienzaPartida");
            const id_partida =  localStorage.getItem("idPartida");
            // Si el juego ha comenzado, redirigir a frase_jugador.html
            if (gameStarted === "true" && id_partida == id_actual_partida) {

                // Eliminar el indicador para evitar redirecciones futuras
                localStorage.removeItem("ComienzaPartida");
                window.location.href = currentUrl.replace("espera_jugador.html", "frase_jugador.html");; //redireccion a la pantalla /frase_jugador.html
            }
        }

    // Verificar cada 0.5 segundos (500 milisegundos) si se ha pulsado COMENZAR en la pantalla /yonunca_intro
    setInterval(checkGameStart, 300);

