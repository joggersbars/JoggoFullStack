// Función para obtener el parámetro "id_partida" de la URL
function getIdPartidaFromURL() {
    const urlParams = new URLSearchParams(window.location.search);
    return urlParams.get("id_partida"); 
}

const id_actual_partida = getIdPartidaFromURL();// Obtenemos el valor de id_partida que viene como parámetro desde la URL

// Animación Lottie para el contenedor principal
var animation = lottie.loadAnimation({
    container: document.getElementById('lottie-container'), // Contenedor donde se cargará la animación
    renderer: 'svg', // Renderización en formato SVG
    loop: false, // No repetir la animación
    autoplay: true, // Reproducir automáticamente
    path: 'src/lotties/Loading_bar1.json' // Ruta de la animación en formato JSON
});

animation.setSpeed(0.033);

// Animación Lottie para el temporizador
var animation_timer = lottie.loadAnimation({
    container: document.getElementById('lottie-container-timer'), // Contenedor donde se cargará la animación
    renderer: 'svg', // Renderización en formato SVG
    loop: false, // No repetir la animación
    autoplay: true, // Reproducir automáticamente
    path: 'src/lotties/Timer.json' // Ruta de la animación en formato JSON
});

// Detectar el final de la animación del temporizador
animation_timer.addEventListener('complete', async function() {
    console.log("El temporizador ha terminado");

    // 1. Generar la señal en el localStorage para que la otra pantalla pueda detectar que el temporizador terminó
    localStorage.setItem("Fin_temporizador", "true");
    localStorage.setItem("idPartida", id_actual_partida); 

    console.log("Id partida",id_actual_partida)
    const id_partida = { id_partida: id_actual_partida };

    // 2. Enviar la solicitud `fetch` al backend con `id_partida` en formato JSON
    try {
        const response = await fetch('http://localhost:8002/establecer_indices_frases', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(id_partida)
        });

        if (response.ok) {
            console.log("Solicitud al backend exitosa: cantidad de frases establecida.");
        } else {
            console.error("Error en la respuesta del backend:", response.statusText);
        }
    } catch (error) {
        console.error("Error al conectar con el backend:", error);
    }

    // 3. Redirigir a la pantalla /yonunca_game.html pasando `id_partida`
    window.location.href = `/yonunca_game.html?id_partida=${id_actual_partida}`;
});
