// Función para obtener el parámetro "id_partida" de la URL
function getIdPartidaFromURL() {
    const urlParams = new URLSearchParams(window.location.search);
    return urlParams.get("id_partida"); // Obtenemos el valor de id_partida que viene como parametro desde la URL
}

// Rellenar el campo id_partida si existe en la URL
document.addEventListener("DOMContentLoaded", function() {
    const idPartida = getIdPartidaFromURL();
    if (idPartida) {
        document.getElementById("id_partida").value = idPartida; // Rellenar el campo con el id_partida si viene desde el QR
    }

    // Asignar el evento de clic al botón "ENTRAR"
    const entrarBtn = document.getElementById("entrar-btn");
    entrarBtn.addEventListener("click", function() {
        // Obtener los valores de los campos
        const idPartidaValue = document.getElementById("id_partida").value;
        const apodoJugador = document.getElementById("apodo_jugador").value;

        // Validar que ambos campos estén completos
        if (idPartidaValue && apodoJugador) {
            // Redirigir a /espera_jugador si ambos campos están completos
            window.location.href = "/espera_jugador";
        } else {
            // Mostrar mensaje de error si algún campo está vacío
            alert("Por favor, completa todos los campos para entrar en la partida.");
        }
    });
});


