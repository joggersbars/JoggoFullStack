// Obtenemos parametros de la URL
const urlParams = new URLSearchParams(window.location.search);
const apodo_jugador = urlParams.get('apodo_jugador');
const id_partida = urlParams.get('id_partida');