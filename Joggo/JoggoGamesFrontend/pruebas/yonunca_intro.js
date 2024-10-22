document.addEventListener('DOMContentLoaded', () => {
    // Obtener el ID de la partida desde la URL
    const urlParams = new URLSearchParams(window.location.search);
    const idPartida = urlParams.get('id_partida');

    console.log("ID de la partida obtenido:", idPartida);

    // Mostrar el ID de la partida en el HTML
    const idPartidaElement = document.getElementById('id_partida');
    if (idPartida) {
        idPartidaElement.textContent = idPartida;
    } else {
        console.error("ID de partida no encontrado en la URL.");
    }

    // Generar el código QR si el ID de la partida está disponible
    if (idPartida) {
        console.log("Generando QR con la URL: http://localhost:5000/partida?id_partida=" + idPartida);
        const qr = new QRious({
            element: document.getElementById('qrPartida'),
            value: `http://localhost:5000/partida?id_partida=${idPartida}`, // URL con el ID de la partida
            size: 250,
            backgroundAlpha: 0, // fondo transparente
            foreground: '#000',  // color del código QR
            level: 'H'  // nivel de corrección de errores
        });
    }
});
