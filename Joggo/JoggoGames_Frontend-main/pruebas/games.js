// Esperar a que el DOM esté completamente cargado antes de agregar funcionalidades
document.addEventListener('DOMContentLoaded', () => {
    console.log('Página de juegos cargada.');

    // Agregar funcionalidad a los botones de los juegos
    const gameButtons = document.querySelectorAll('.game-btn');
    
    gameButtons.forEach((button) => {
        button.addEventListener('click', async (event) => {
            const gameName = event.target.textContent;
            console.log(`El usuario ha seleccionado el juego: ${gameName}`);

            try {
                // Hacer una solicitud GET al backend para crear una nueva partida
                const response = await fetch(`http://localhost:5000/crear_partida?game_name=${gameName}`, { 
                    //se envia una solicitud al back end para que se cree la partida
                    method: 'GET'
                });

                // Procesar la respuesta del servidor backend
                if (response.ok) {
                    const result = await response.json();
                    console.log('Partida creada:', result);

                    // Mostrar la información de la partida en la consola o redirigir al usuario
                    alert(`Partida creada con éxito: ID ${result.id_partida}, URL: ${result.url_partida}`);
                    // Redirigir al usuario a la página de la partida creada ya que en la respuesta "result" esta la URL recibida del Back-End
                    window.location.href =  `/partida?id_partida=${result.id_partida}`; //Al ser partidas dinamicas --> se tiene que crear con el ID de la partida que se recibe desde el Back End --> Mirarlo
                } else {
                    console.error('Error al crear la partida:', response.statusText);
                }
            } catch (error) {
                console.error('Error al conectar con el servidor:', error);
            }
        });
    });
});

