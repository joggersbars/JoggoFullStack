// Esperar a que el DOM esté completamente cargado antes de agregar funcionalidades
document.addEventListener('DOMContentLoaded', () => {
    console.log('Página de juegos cargada.');

    // Agregar funcionalidad a los botones de los juegos
    const gameButtons = document.querySelectorAll('.game-btn');
    
    gameButtons.forEach((button) => {
        button.addEventListener('click', async (event) => {
            const gameName = event.target.textContent;
            console.log(`El usuario ha seleccionado el juego: ${gameName}`);
            window.location.href = `/yonunca_intro`;
        });
    });
});

