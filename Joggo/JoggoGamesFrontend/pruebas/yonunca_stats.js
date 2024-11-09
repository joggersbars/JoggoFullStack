let myChart; // Variable global para almacenar el gráfico

function getResponsiveFontSize() {
    // Ajusta el tamaño de fuente en función del ancho de la ventana
    return Math.max(window.innerWidth * 0.02, 12); // Mínimo de 12px
}

// Plugin para agregar sombra
/*const shadowPlugin = {
    id: 'shadowPlugin',
    beforeDatasetDraw: (chart, args, options) => {
        const ctx = chart.ctx;
        const datasetIndex = args.index;
        const dataset = chart.data.datasets[datasetIndex];
        const meta = chart.getDatasetMeta(datasetIndex);

        meta.data.forEach((bar) => {
            ctx.save();
            ctx.shadowColor = 'rgba(0, 0, 0, 0.5)'; // Color de la sombra
            ctx.shadowBlur = 10; // Nivel de desenfoque
            ctx.shadowOffsetX = 4; // Desplazamiento en X
            ctx.shadowOffsetY = 4; // Desplazamiento en Y

            // Dibujar la barra con sombra
            ctx.fillStyle = dataset.backgroundColor;
            ctx.fillRect(bar.x - bar.width / 2, bar.y, bar.width, bar.base - bar.y);
            ctx.restore();
        });
    }
};*/

function renderChart() {
    fetch('pruebas/yonunca_result10.json')
        .then(response => response.json())
        .then(data => {
            // Obtener los datos del JSON
            const jugadores = data.jugadores;
            const conteo = data.conteo;

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
                        color: 'yellow',
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
                                    size: getResponsiveFontSize() // Tamaño del texto en el eje Y
                                }
                            }
                        },
                        x: {
                            ticks: {
                                color: 'white', // Color del texto en el eje X
                                font: {
                                    family: 'ChauPhilomeneOne-Regular',
                                    size: getResponsiveFontSize() // Tamaño del texto en el eje X
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
                                size: getResponsiveFontSize() // Tamaño del texto en el título del tooltip
                            },
                            bodyFont: {
                                size: getResponsiveFontSize() // Tamaño del texto en el cuerpo del tooltip
                            }
                        }
                    },
                    //plugins: [shadowPlugin] // Activar el plugin de sombra
                }
            });
        })
        .catch(error => console.error('Error al cargar el archivo JSON:', error));
}

// Llamar a renderChart al cargar la página
renderChart();

// Escuchar el evento de cambio de tamaño de la ventana para redimensionar
window.addEventListener('resize', () => {
    renderChart(); // Volver a renderizar el gráfico con el nuevo tamaño de fuente
});
