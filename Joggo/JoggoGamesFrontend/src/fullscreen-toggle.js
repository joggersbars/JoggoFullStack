// Función para verificar si está en modo pantalla completa
function isFullScreen() {
    return (
        document.fullscreenElement ||
        document.webkitFullscreenElement ||
        document.mozFullScreenElement ||
        document.msFullscreenElement
    );
}

// Función para entrar y salir de pantalla completa
function toggleFullScreen() {
    if (!isFullScreen()) {
        // Entra en pantalla completa
        if (document.documentElement.requestFullscreen) {
            document.documentElement.requestFullscreen();
        } else if (document.documentElement.mozRequestFullScreen) { // Firefox
            document.documentElement.mozRequestFullScreen();
        } else if (document.documentElement.webkitRequestFullscreen) { // Chrome, Safari y Opera
            document.documentElement.webkitRequestFullscreen();
        } else if (document.documentElement.msRequestFullscreen) { // IE/Edge
            document.documentElement.msRequestFullscreen();
        }
    } else {
        // Salir de pantalla completa
        if (document.exitFullscreen) {
            document.exitFullscreen();
        } else if (document.mozCancelFullScreen) { // Firefox
            document.mozCancelFullScreen();
        } else if (document.webkitExitFullscreen) { // Chrome, Safari y Opera
            document.webkitExitFullscreen();
        } else if (document.msExitFullscreen) { // IE/Edge
            document.msExitFullscreen();
        }
    }
}

// Escuchar la tecla F11
document.addEventListener('keydown', function(event) {
    if (event.key === 'F11') {
        event.preventDefault(); // Evita el comportamiento por defecto de F11 en el navegador
        toggleFullScreen(); // Llama a la función de alternar pantalla completa
    }
});

// Detectar cambios en el modo de pantalla completa
document.addEventListener("fullscreenchange", function() {
    if (isFullScreen()) {
        // Estilos para modo pantalla completa
        document.body.style.padding = "0";
        document.body.style.margin = "0";
    } else {
        // Revertir los estilos si sales de pantalla completa
        document.body.style.padding = "";
        document.body.style.margin = "";
    }
});
