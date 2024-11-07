// Obtener parámetros url
function getParamsFromURL() {
    const urlParams = new URLSearchParams(window.location.search);
    const id_partida = urlParams.get("id_partida");
    const apodo_jugador = urlParams.get("apodo_jugador");
    console.log("id_partida:", id_partida);
    console.log("apodo_jugador:", apodo_jugador);
    return { id_partida, apodo_jugador };
}

// Función para obtener la frase desde `localStorage` y actualizar el HTML
function mostrarFraseDesdeLocalStorage() {
    // Obtener la frase guardada en `localStorage`
    const frase = localStorage.getItem("frase_juego");

    // Verificar si existe una frase en `localStorage` y actualizar el HTML
    if (frase) {
        document.querySelector(".main-heading").textContent = frase; // Actualiza el `<h1>`
    } else {
        console.log("No hay frase guardada en localStorage");
    }
}

// Función para enviar la respuesta al endpoint
async function enviarRespuesta(respuesta) {
    const { id_partida, apodo_jugador } = getParamsFromURL();
    const frase = localStorage.getItem("frase_juego");
    const url = `http://localhost:8002/recibir_respuesta/${id_partida}/${apodo_jugador}/${encodeURIComponent(frase)}/${respuesta}`

    try {
        const response = await fetch(url, {
            method: 'POST', 
            mode: "no-cors",
            headers: {
                'Content-Type': 'application/json'
            }
        });

        if (response.ok) {
            const result = await response.json();
            console.log("Respuesta del backend:", result.message);
            // Aquí podrías hacer algo, como mostrar un mensaje de confirmación o cambiar la frase
        } else {
            console.error("Error en la respuesta del backend:", response.statusText);
        }
    } catch (error) {
        console.error("Error al conectar con el backend:", error);
    }
}

// Ejecutar `mostrarFraseDesdeLocalStorage` cuando la página cargue
document.addEventListener("DOMContentLoaded", function() {
    mostrarFraseDesdeLocalStorage();

    // Añadir eventos a los botones para capturar la respuesta
    document.querySelector(".btn-Si").addEventListener("click", function() {
        enviarRespuesta("Si");
    });

    document.querySelector(".btn-No").addEventListener("click", function() {
        enviarRespuesta("No");
    });

    setInterval(mostrarFraseDesdeLocalStorage, 100);
});

