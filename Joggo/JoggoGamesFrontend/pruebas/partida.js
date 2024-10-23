        // Obtener el parámetro id_partida de la URL
        const urlParams = new URLSearchParams(window.location.search);
        const id_partida = urlParams.get('id_partida');


         // Si existe el ID de la partida, lo mostramos en el elemento correspondiente
        if (idPartida) {
        const partidaIdElement = document.getElementById('partida-id');
        partidaIdElement.textContent = idPartida;
        }

        // Manejar el formulario para que el usuario ingrese su id_user_partida
        document.getElementById('user-form').addEventListener('submit', function(event) {
            event.preventDefault(); // Evitar que el formulario recargue la página

            const userId = document.getElementById('user-id').value;
            console.log(`Jugador con ID: ${userId} se une a la partida con ID: ${idPartida}`);
            // Redirigir al usuario a /yonunca_intro pasando el id_partida y id_user_partida
            //  window.location.href = `/yonunca_intro?id_partida=${id_partida}&id_user_partida=${userId}`; --> tenemos que ver como vamos a gestionar la URL
            window.location.href = '/yonunca_intro';
        });

        