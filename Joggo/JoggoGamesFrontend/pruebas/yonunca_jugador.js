

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
let fraseActual = localStorage.getItem("frase_juego"); // Guardar la frase actual

function mostrarFraseDesdeLocalStorage() {
    // Obtener la frase guardada en `localStorage`
    const frase = localStorage.getItem("frase_juego");

    // Verificar si existe una frase en `localStorage` y actualizar el HTML
    if (frase) {
        // Solo actualizar si la frase ha cambiado
        document.querySelector(".main-heading").textContent = frase; // Actualiza el `<h1>`
        fraseActual = frase; // Actualizar `fraseActual`
        habilitarBoton(); // Habilitar el botón si la frase cambió
        
    } else {
        console.log("No hay frase guardada en localStorage");
    }
}

// Función para enviar la respuesta al endpoint
async function enviarRespuesta(respuesta) {
    const { id_partida, apodo_jugador } = getParamsFromURL();

    const url = `${API_URL}/recibir_respuesta/${id_partida}/${apodo_jugador}/${respuesta}`;

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
        } else {
            console.error("Error en la respuesta del backend:", response.statusText);
        }
    } catch (error) {
        console.error("Error al conectar con el backend:", error);
    }

    // Desactivar el botón después de enviar la respuesta
    deshabilitarBoton();
}

// Función para deshabilitar el botón "Si"
function deshabilitarBoton() {
    document.querySelector(".btn-Si").disabled = true;
}

// Función para habilitar el botón "Si"
function habilitarBoton() {
    document.querySelector(".btn-Si").disabled = false;
}

// Ejecutar `mostrarFraseDesdeLocalStorage` cuando la página cargue
document.addEventListener("DOMContentLoaded", function() {
    mostrarFraseDesdeLocalStorage();

    // Añadir eventos a los botones para capturar la respuesta
    document.querySelector(".btn-Si").addEventListener("click", function() {
        enviarRespuesta("Si");
    });

    setInterval(mostrarFraseDesdeLocalStorage, 10);
});
