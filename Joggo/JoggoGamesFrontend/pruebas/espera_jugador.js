function getIdPartidaFromURL() {
    const urlParams = new URLSearchParams(window.location.search);
    return urlParams.get("id_partida"); // Obtenemos el valor de id_partida que viene como parametro desde la URL
}
//obtenemos el valor de id partida proveniente de la URL como parametro
const id_actual_partida = getIdPartidaFromURL();


      // Obtener la URL actual
      const currentUrl = window.location.href;

        // Función para verificar si el juego ha comenzado
        async function checkGameStart() {
            const gameStarted = localStorage.getItem("ComienzaPartida");
            const id_partida =  localStorage.getItem("idPartida");
            // Se comprueba que se ha pulsado el boton comenzar y que el id corresponde a dicha partida
            if (gameStarted === "true" && id_partida === id_actual_partida) {

                // Eliminar el indicador para evitar redirecciones futuras
                localStorage.removeItem("ComienzaPartida");
                localStorage.removeItem("idPartida");
                window.location.href = currentUrl.replace("espera_jugador.html", "frase_jugador.html");; //redireccion a la pantalla /frase_jugador.html
            }
        }
        async function checkAllphrasesDoneStart() {
            const Fin_temporizador = localStorage.getItem("Fin_temporizador");
            const id_partida =  localStorage.getItem("idPartida");
            // Si el temporizardor termina , se redirige a yonunca_jugador.html asociado al ID_partida
            if (Fin_temporizador === "true" && id_partida === id_actual_partida) {

                // Eliminar el indicador para evitar redirecciones futuras
                localStorage.removeItem("Fin_temporizador");
                localStorage.removeItem("idPartida");
                window.location.href = currentUrl.replace("espera_jugador.html", "yonunca_jugador.html");; //redireccion a la pantalla /yonunca_jugador.html --> EMPIEZA EL JUEGO
            }
        }

    // Verifica cada 0.3 segundos (300 milisegundos) si se ha pulsado COMENZAR en la pantalla /yonunca_intro
    setInterval(checkGameStart, 300);
    // Verifica cada 0.3 segundos (300 milisegundos) si se terminado el contador en la pantalla /yonunca_frase
    setInterval(checkAllphrasesDoneStart, 300);

