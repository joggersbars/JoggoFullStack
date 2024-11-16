let fraseActual = ""; // Almacena la frase anterior para detectar cambios

// Obtener parámetros URL
function getParamsFromURL() {
    const urlParams = new URLSearchParams(window.location.search);
    const id_partida = urlParams.get("id_partida");
    const apodo_jugador = urlParams.get("apodo_jugador");
    console.log("id_partida:", id_partida);
    console.log("apodo_jugador:", apodo_jugador);
    return { id_partida, apodo_jugador };
}

// Mostrar frase desde el servidor y actualizar el DOM si cambia
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
            const result = await response.json();
            console.log("Respuesta del backend:", result.frase);

            if (result.frase !== fraseActual) { 
                document.querySelector(".main-heading").textContent = result.frase;
                fraseActual = result.frase;
                habilitarBoton(); // Habilita todos los botones al cambiar la frase
                resetBotones(); // Limpia el estado visual de los botones
            }
        } else {
            console.error("Error en la respuesta del backend:", response.statusText);
        }
    } catch (error) {
        console.error("Error al conectar con el backend:", error);
    }
}

// Enviar "Like" al backend
async function enviarLike() {
    const { id_partida, apodo_jugador } = getParamsFromURL();
    const frase = encodeURIComponent(fraseActual);
    const url = `${API_URL}/enviar_like/${id_partida}/${frase}`;
 
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
            console.log("Like enviado correctamente:", result.message);
        } else {
            console.error("Error al enviar el like:", response.statusText);
        }
    } catch (error) {
        console.error("Error al conectar con el backend:", error);
    } 
}

// Enviar respuesta "Si" o "No" al backend y deshabilitar los botones correspondientes
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
    // Desactiva solo los botones "Si" y "No" despues de enviarlo
    deshabilitarBotonesRespuesta();
}

// Función para deshabilitar solo los botones de respuesta "Si" y "No"
function deshabilitarBotonesRespuesta() {
    document.querySelector(".btn-Si").disabled = true;
    document.querySelector(".btn-No").disabled = true;
}

// Habilitar todos los botones
function habilitarBoton() {
    document.querySelector(".btn-Si").disabled = false;
    document.querySelector(".btn-No").disabled = false;
    document.querySelector(".btn-like").disabled = false;
}

// Limpiar el estado visual de los botones
function resetBotones() {
    // Limpia las clases "active" de todos los botones
    const botones = document.querySelectorAll(".btn-Si, .btn-No, .btn-like");
    botones.forEach((boton) => {
        boton.classList.remove("active");
    });
}
// Ejecutar `mostrarFraseDesdeLocalStorage` al cargar la página
document.addEventListener("DOMContentLoaded", function() {
    mostrarFraseDesdeLocalStorage();

    // Añadir eventos a los botones
    document.querySelector(".btn-Si").addEventListener("click", function() {
        enviarRespuesta("Si");
        this.classList.add("active");
    });
    document.querySelector(".btn-No").addEventListener("click", function() {
        enviarRespuesta("No");
        this.classList.add("active");
    });
    document.querySelector(".btn-like").addEventListener("click", function() {
        enviarLike();
        this.classList.add("active");
        // Deshabilita el botón de like después de enviarlo
        document.querySelector(".btn-like").disabled = true;
    });

    // Refrescar la frase cada 10 segundos y verificar el estado del juego cada 20 segundos
    setInterval(() => {
        mostrarFraseDesdeLocalStorage();
        resetBotones(); // Llamar a resetBotones aquí también, por si acaso.
    }, 10000);
    
    checkGameInterval = setInterval(checkGameFinish, 5000);
});

// Verificar si el juego ha finalizado y redirigir
async function checkGameFinish() {
    const { id_partida, apodo_jugador } = getParamsFromURL();
    try {
        const response = await fetch(`${API_URL}/game/status/${id_partida}`);
        const data = await response.json();
        
        if (data.estado === "finalizado") {
            clearInterval(checkGameInterval);
            const redirectUrl = `${window.location.origin}/yonunca_final_jugador.html?id_partida=${id_partida}&apodo_jugador=${apodo_jugador}`;
            window.location.href = redirectUrl;
        }
    } catch (error) {
        console.error("Error al verificar el estado del juego:", error);
    }
}
