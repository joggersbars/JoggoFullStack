//# Pruebas unitarias o de integración
document.getElementById('login-form').addEventListener('submit', async (event) => {
    event.preventDefault(); // Evitar que el formulario recargue la página
    //const apiUrl = process.env.REACT_APP_API_URL;
    //console.log('API URL:', process.env.REACT_APP_API_URL);
    // Capturar los datos del formulario
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    // Crear un objeto con los datos
    const data = { username, password };

    // Loggear los datos que se están enviando
    console.log('Enviando datos al servidor:', data);

    try {   
        // Enviar la solicitud POST al servidor Python (Flask)
        //console.log('Iniciando solicitud al backend...',apiUrl);
        const response = await fetch(`${API_URL}/login_user`, {  //${apiUrl}
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data) // Convertir los datos a JSON para enviarlos
        });

        // Loggear el estado de la respuesta del servidor
        console.log('Respuesta del servidor (status):', response.status);
        // Procesar la respuesta del servidor
        // Procesar la respuesta del servidor
        if (response.ok) {
            const result = await response.json();
            // Loggear el mensaje recibido del servidor
            console.log('Mensaje recibido del servidor:', result.message);

            // Comprobar si el mensaje es "Bienvenido"
            if (result.message.includes('Bienvenido')) {
                // Redirigir a la pantalla /games si la autenticación fue exitosa
                console.log('Autenticación exitosa. Redirigiendo a /games...');
                window.location.href = '/games';
            } else if (result.message.includes('El usuario no está registrado')) {
                alert('Error de autenticación: ' + result.message); // Mostrar el mensaje de error
            }
        } else {
            alert('Error de autenticación: ' + response.statusText); // Mostrar error si la autenticación falla
        }
    } catch (error) {
        console.error('Error al conectar con el servidor:', error);
        alert('Hubo un problema al conectar con el servidor.');
    }
});

