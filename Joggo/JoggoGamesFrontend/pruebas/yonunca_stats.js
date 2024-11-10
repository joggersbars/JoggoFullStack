let myChart; // Variable global para almacenar el gráfico

// Función para obtener el parámetro "id_partida" de la URL
function getIdPartidaFromURL() {
    const urlParams = new URLSearchParams(window.location.search);
    return urlParams.get("id_partida"); 
}

function getResponsiveFontSize() {
    return Math.max(window.innerWidth * 0.02, 12); // Mínimo de 12px
}

// Función para renderizar el gráfico
async function renderChart() {
    const id_partida = getIdPartidaFromURL(); // Obtiene el id_partida de la URL
    if (!id_partida) {
        console.error("No se encontró el parámetro 'id_partida' en la URL.");
        return;
    }

    try {
        const response = await fetch(`${API_URL}/mandar_stats/${id_partida}`);
        const data = await response.json();
        
        // Convertir el diccionario de estadísticas en arrays de jugadores y conteo
        const jugadores = Object.keys(data.estadisticas);
        const conteo = Object.values(data.estadisticas);

        // Si el gráfico ya existe, destrúyelo antes de crear uno nuevo
        if (myChart) {
            myChart.destroy();
        }

        // Crear el gráfico de barras con Chart.js
        const ctx = document.getElementById('myChart').getContext('2d');
        myChart = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: jugadores,
                datasets: [{
                    label: 'Nº Si',
                    data: conteo,
                    color: 'white',
                    backgroundColor: 'rgba(255, 255, 255, 1)',
                    borderColor: 'rgba(0, 0, 0, 1)',
                    borderWidth: 2,
                    borderRadius: 10
                }]
            },
            options: {
                scales: {
                    y: {
                        beginAtZero: true,
                        ticks: {
                            color: 'white', // Color del texto en el eje Y
                            font: {   
                                family: 'ChauPhilomeneOne-Regular',
                                size: getResponsiveFontSize()
                            }
                        }
                    },
                    x: {
                        ticks: {
                            color: 'white', // Color del texto en el eje X
                            font: {
                                family: 'ChauPhilomeneOne-Regular',
                                size: getResponsiveFontSize()
                            }
                        }
                    }
                },
                plugins: {
                    legend: {
                        labels: {
                            color: 'white', // Cambia el color del texto de la leyenda aquí
                            font: {
                                family: 'ChauPhilomeneOne-Regular',
                                size: getResponsiveFontSize() // Tamaño del texto en la leyenda
                            }
                        }
                    },
                    tooltip: {
                        titleFont: {
                            size: getResponsiveFontSize()
                        },
                        bodyFont: {
                            size: getResponsiveFontSize()
                        }
                    }
                }
            }
        });
    } catch (error) {
        console.error('Error al cargar las estadísticas:', error);
    }
}

// Llamar a renderChart al cargar la página
renderChart();

// Escuchar el evento de cambio de tamaño de la ventana para redimensionar
window.addEventListener('resize', () => {
    renderChart(); // Volver a renderizar el gráfico con el nuevo tamaño de fuente
});
