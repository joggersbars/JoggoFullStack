let fraseActual = ""; // Almacena la frase anterior para detectar cambios

// Obtener parámetros url
function getParamsFromURL() {
    const urlParams = new URLSearchParams(window.location.search);
    const id_partida = urlParams.get("id_partida");
    const apodo_jugador = urlParams.get("apodo_jugador");
    console.log("id_partida:", id_partida);
    console.log("apodo_jugador:", apodo_jugador);
    return { id_partida, apodo_jugador };
}

async function mostrarFraseDesdeLocalStorage() {
    const { id_partida, apodo_jugador } = getParamsFromURL();
    try {
        const response = await fetch(`${API_URL}/coger_frase_jugador/${id_partida}`,{
            method: 'GET', 
            mode: "cors",
            headers: {
                'Content-Type': 'application/json'
            }    
        });
        if (response.ok) {
            result = await response.json();
            console.log("Respuesta del backend:", result.frase);

            if (result.frase !== fraseActual) { 
                document.querySelector(".main-heading").textContent = result.frase; // Actualiza el `<h1>`
                fraseActual = result.frase; //Actualiza `fraseActual` con la nueva frase
                habilitarBoton(); //Habilita los botones cuando cambia la frase
                resetBotones(); // Limpia el estado de los botones para la nueva frase
            }     
        } else {
            console.error("Error en la respuesta del backend:", response.statusText);
        }       
    } catch (error) {
        console.error("Error al conectar con el backend:", error);
    }
}
// Función para enviar la respuesta al endpoint
async function enviarRespuesta(respuesta) {
    const { id_partida, apodo_jugador } = getParamsFromURL();
    const url = `${API_URL}/recibir_respuesta/${id_partida}/${apodo_jugador}/${respuesta}`;
    try {
        const response = await fetch(url, {
            method: 'POST', 
            mode: "cors",
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
    document.querySelector(".btn-No").disabled = true;
}

// Función para habilitar el botón "Si"
function habilitarBoton() {
    document.querySelector(".btn-Si").disabled = false;
    document.querySelector(".btn-No").disabled = false;
}

// Función para resetear el estado visual de los botones
function resetBotones() {
    document.querySelector(".btn-Si").classList.remove("active");
    document.querySelector(".btn-No").classList.remove("active");
    document.querySelector(".btn-like").classList.remove("active");
}

// Ejecutar `mostrarFraseDesdeLocalStorage` cuando la página cargue
document.addEventListener("DOMContentLoaded", function() {
    mostrarFraseDesdeLocalStorage();

    // Añadir eventos a los botones para capturar la respuesta
    document.querySelector(".btn-Si").addEventListener("click", function() {
        enviarRespuesta("Si");
        this.classList.add("active");
    });
    document.querySelector(".btn-No").addEventListener("click", function() {
        this.classList.add("active");
    });
    document.querySelector(".btn-like").addEventListener("click", function() {
        document.querySelector(".btn-No").disabled = false;
        enviarRespuesta("like");
        this.classList.add("active");
    });

    setInterval(mostrarFraseDesdeLocalStorage,10005); // Mirar para ajustar cuando se cambie de frase
});
// Verifica si el juego ha finalizado mediante un llamado al backend
async function checkGameFinish() {
    const response = await fetch(`${API_URL}/game/status/${id_actual_partida}`);
    const data = await response.json();
    
    if (data.estado === "finalizado") {
        window.location.href = currentUrl.replace("yonunca_jugador.html", `yonunca_final_jugador.html/${id_partida}${apodo_jugador}`);
    }
}
// Ejecuta la verificación cada 300 milisegundos
setInterval(checkGameFinish, 5000);
