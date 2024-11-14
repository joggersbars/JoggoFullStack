// Función para obtener el parámetro "id_partida" de la URL
function getIdPartidaFromURL() {
    const urlParams = new URLSearchParams(window.location.search);
    return urlParams.get("id_partida"); 
}

function getResponsiveFontSize() {
    return Math.max(window.innerWidth * 0.02, 12); // Mínimo de 12px
}


// Animación Lottie


const lottieBackground = document.getElementById("lottie-background");
const animation = lottie.loadAnimation({
    container: lottieBackground, // Contenedor para la animación
    renderer: 'svg',
    loop: true,
    autoplay: true,
    path: '/src/lotties/Party.json' // Cambia a la ruta de tu archivo Lottie
});
    