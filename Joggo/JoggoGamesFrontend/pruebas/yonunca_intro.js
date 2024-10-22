
document.addEventListener('DOMContentLoaded', async () => {
    try {
        // Hacer una solicitud GET al servidor para obtener el ID de la partida
        const response = await fetch('http://localhost:5000/crear_partida?game_name=Yo%20Nunca', { 
            method: 'GET',
        });

        if (response.ok) {
            const result = await response.json();
            const idPartida = result.id_partida;  // Obtener el ID de la partida del backend
            console.log('ID de la partida recibido:', idPartida);

            // Mostrar el ID de la partida en el HTML
            document.getElementById('id_partida').textContent = idPartida;

            // Generar el código QR con el ID de la partida
            const qr = new QRious({
                element: document.getElementById('qrPartida'),
                value: `http://localhost:8001/partida_${idPartida}`, // URL con el ID de la partida
                size: 250,
                backgroundAlpha: 0, // Fondo transparente
                foreground: '#000',  // Color del QR
                level: 'H'  // Nivel de corrección de errores
            });
        } else {
            console.error('Error al obtener el ID de la partida:', response.statusText);
        }
    } catch (error) {
        console.error('Error al conectar con el servidor:', error);
    }
});








