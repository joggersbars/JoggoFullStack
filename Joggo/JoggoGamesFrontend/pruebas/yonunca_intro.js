// Declaración global de la variable idPartida para que sea accesible en todo el archivo
let idPartida;

document.addEventListener('DOMContentLoaded', async () => {
    try {
        // Hacer una solicitud GET al servidor para obtener el ID de la partida
        const response = await fetch(`${API_URL}/crear_partida/${'Yo_nunca'}`, { 
            method: 'GET',
        });

        if (response.ok) {
            const result = await response.json();
            idPartida = result.id_partida;  // Obtener el ID de la partida del backend
            console.log('ID de la partida recibido:', idPartida);

            // Mostrar el ID de la partida en el HTML
            document.getElementById('id_partida').textContent = idPartida;

            // Generar el código QR con el ID de la partida
            const qr = new QRious({
                element: document.getElementById('qrPartida'),
                value: `https://www.play.joggo.es/intro_jugador.html?id_partida=${idPartida}`, // URL con el ID de la partida
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

 // Definicion de la función para enviar una solicitud POST a /empezar_partida con el id de la partida
 async function empezarPartida() {
    try {
        const response = await fetch(`${API_URL}/empezar_partida`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                mensaje_inicio: "vamos a empezar partida yo nunca",
                id_partida: idPartida   //mandamos el id partida
            })
        });

        if (response.ok) {
            const result = await response.json();
            console.log('Respuesta del servidor al empezar partida:', result);
        } else {
            console.error('Error al iniciar la partida:', response.statusText);
        }

    } catch (error) {
        console.error('Error al enviar la solicitud para empezar la partida:', error);
    }
}

// Evento de clic en el botón "Comenzar" para iniciar la partida
document.getElementById("start-game-btn").addEventListener("click", async () => {
    if (idPartida) {
        await empezarPartida();
        localStorage.setItem("ComienzaPartida", "true"); //Guardar señal de inicio en localStorage
        localStorage.setItem("idPartida", idPartida);
        window.location.href = `/yonunca_frase.html?id_partida=${idPartida}`;
    } else {
        console.error("No se ha obtenido un ID de partida válido.");
    }
});



