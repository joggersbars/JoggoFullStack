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
        const response = await fetch(`${API_URL}/coger_frase_jugador/${id_partida},${apodo_jugador}`, {
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

async function enviarLike() {
    const { id_partida, apodo_jugador } = getParamsFromURL();
    const frase = encodeURIComponent(fraseActual);
    const url = `${API_URL}/enviar_like?id_partida=${id_partida}&apodo_jugador=${apodo_jugador}&frase=${frase}`;
 
    try {
        const response = await fetch(url, {
            method: 'GET',
            mode: "cors",
            headers: {
                'Content-Type': 'application/json'
            }
        });

        if (response.ok) {
            const result = await response.json();
            console.log("Like enviado correctamente:", result.message);
        } else {
            console.error("Error al enviar el like:", response.statusText);
        }
    } catch (error) {
        console.error("Error al conectar con el backend:", error);
    }
}

// Función para enviar la respuesta Si o No al endpoint
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

// Función para deshabilitar los botones
function deshabilitarBoton() {
    document.querySelector(".btn-Si").disabled = true;
    document.querySelector(".btn-No").disabled = true;
    document.querySelector(".btn-like").disabled = true;
}
// Función para habilitar los botones
function habilitarBoton() {
    document.querySelector(".btn-Si").disabled = false;
    document.querySelector(".btn-No").disabled = false;
    document.querySelector(".btn-like").disabled = false;
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
        enviarLike();
        this.classList.add("active");
    });

    setInterval(mostrarFraseDesdeLocalStorage,5000); 
    checkGameInterval = setInterval(checkGameFinish, 5000);
});
// Verifica si el juego ha finalizado mediante un llamado al backend
async function checkGameFinish() {
    const { id_partida, apodo_jugador } = getParamsFromURL();
    try {
        const response = await fetch(`${API_URL}/game/status/${id_partida}`);
        const data = await response.json();
        
        if (data.estado === "finalizado") {
            clearInterval(checkGameInterval); // Detiene el intervalo al detectar el estado "finalizado"
            
            const redirectUrl = `${window.location.origin}/yonunca_final_jugador.html?id_partida=${id_partida}&apodo_jugador=${apodo_jugador}`;
            window.location.href = redirectUrl;
        }
    } catch (error) {
        console.error("Error al verificar el estado del juego:", error);
    }
}
