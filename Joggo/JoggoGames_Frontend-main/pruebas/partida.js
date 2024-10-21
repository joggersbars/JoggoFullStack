        // Obtener el parámetro id_partida de la URL
        const urlParams = new URLSearchParams(window.location.search);
        const id_partida = urlParams.get('id_partida');

        // Mostrar el ID de la partida en la página
        document.getElementById('partida-id').textContent = id_partida;

        // Manejar el formulario para que el usuario ingrese su id_user_partida
        document.getElementById('user-form').addEventListener('submit', function(event) {
            event.preventDefault(); // Evitar que el formulario recargue la página

            const userId = document.getElementById('user-id').value;

            // Redirigir al usuario a /yonunca_intro pasando el id_partida y id_user_partida
            //  window.location.href = `/yonunca_intro?id_partida=${id_partida}&id_user_partida=${userId}`; --> tenemos que ver como vamos a gestionar la URL
            window.location.href = '/yonunca_intro';
        });