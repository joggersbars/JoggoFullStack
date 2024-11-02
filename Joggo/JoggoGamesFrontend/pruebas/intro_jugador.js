// Función para obtener el parámetro "id_partida" de la URL
function getIdPartidaFromURL() {
    const urlParams = new URLSearchParams(window.location.search);
    return urlParams.get("id_partida"); // Obtenemos el valor de id_partida que viene como parametro desde la URL
}

// Rellenar el campo id_partida si existe en la URL
document.addEventListener("DOMContentLoaded", function() {
    const idPartida = getIdPartidaFromURL();
    if (idPartida) {
        document.getElementById("id_partida").value = idPartida; //se rellena en el caso de que se entre en la URL desde el QR
    }
});
