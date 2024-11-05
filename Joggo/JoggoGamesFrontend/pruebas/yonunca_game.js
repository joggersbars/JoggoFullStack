// Función para obtener el parámetro "id_partida" de la URL
function getIdPartidaFromURL() {
    const urlParams = new URLSearchParams(window.location.search);
    return urlParams.get("id_partida"); 
}

const id_actual_partida = getIdPartidaFromURL();
const id_partida = { id_partida: id_actual_partida };

// Configuración de la animación Lottie

let animation = lottie.loadAnimation({
    container: document.getElementById('lottie-container'),
    renderer: 'svg',
    loop: false,
    autoplay: false, // No empezar automáticamente, la manejaremos nosotros
    path: 'src/lotties/Loading_bar1.json'
});

   // animation.setSpeed(0.033);
   animation.setSpeed(0.133);

    // Detectar cuando la animación del temporizador termina
    animation.addEventListener('complete', function() {
        solicitarNuevaFrase();
    });

    function iniciarTemporizadorLottie() {
        animation.goToAndPlay(0); // Volver al inicio de la animación y reproducirla
    }

// Lista de frases simulada
const frasesSimuladas = [
    "Yo nunca he viajado al extranjero",
    "Yo nunca he comido sushi",
    "Yo nunca he cantado en público",
    "Yo nunca he practicado un deporte extremo",
    "Yo nunca he visto una película de terror solo"
];

let fraseIndex = 0; // Índice para llevar el seguimiento de la frase actual

// Función para solicitar una nueva frase al backend
async function solicitarNuevaFrase() {

    /*
    try {
        // Preparar el cuerpo de la solicitud en formato JSON
        const data = { id_partida: id_actual_partida };

        const response = await fetch('http://localhost:8002/coger_frase', { 
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data) // Enviar `id_partida` en formato JSON
        });

        if (response.ok) {
            const result = await response.json();
            console.log("Respuesta del backend:", result);

            if (result.message === "Fin_frases") {
                // Si el backend responde con "Fin_frases", redirigimos a /yonunca_stats.html
                window.location.href = "/yonunca_stats.html?id_partida=" + id_actual_partida;
            } else {
                // Si se recibe una nueva frase, actualizar el contenido de la frase
                document.querySelector(".phrase p").textContent = result.frase;

                // Reiniciar el temporizador Lottie para la próxima frase
                iniciarTemporizadorLottie();
            }
        } else {
            console.error("Error en la respuesta del backend:", response.statusText);
        }
    } catch (error) {
        console.error("Error al conectar con el backend:", error);
    }*/
       // Comprobar si hay más frases en la lista simulada
       if (fraseIndex < frasesSimuladas.length) {
        const nuevaFrase = frasesSimuladas[fraseIndex];
        fraseIndex++; // Pasar a la siguiente frase en la próxima llamada

        // Actualizar el contenido de la frase en la pantalla
        document.querySelector(".phrase p").textContent = nuevaFrase;

        // Reiniciar el temporizador Lottie para la próxima frase
        iniciarTemporizadorLottie();
    } else {
        // Simulación de "Fin_frases": redirigir a /yonunca_stats.html
        window.location.href = "/yonunca_stats.html?id_partida=" + id_actual_partida;
    }
}
// Mostrar la primera frase al cargar la página
document.addEventListener("DOMContentLoaded", function() {
    document.querySelector(".phrase p").textContent = frasesSimuladas[fraseIndex];
    fraseIndex++; // Avanzar el índice para la próxima frase
    iniciarTemporizadorLottie(); // Iniciar el temporizador Lottie para la primera frase
});