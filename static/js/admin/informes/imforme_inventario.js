document.addEventListener('DOMContentLoaded', function() {
    try {
        const ctxInventario = document.getElementById('informeInventario').getContext('2d');
        // Generar las etiquetas de los últimos 6 meses
        const generateLastSixMonths = () => {
            const months = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre'];
            const today = new Date();
            let labels = [];

            for (let i = 5; i >= 0; i--) {
                const date = new Date(today.getFullYear(), today.getMonth() - i, 1);
                labels.push(months[date.getMonth()]);
            }

            return labels;
        };

        // Generar etiquetas para los meses del año
        const labelsMeses = generateLastSixMonths();
        // Gráfico de Nuevos Usuarios Diarios
        const inventarioChart = new Chart(ctxInventario, {
            type: 'bar',
            data: {
                labels: labelsMeses,
                datasets: [{
                    label: 'Usuarios Registrados por Mes',
                    data: inventarioData,
                    backgroundColor: 'rgba(255, 99, 132, 0.2)', 
                    borderColor: 'rgba(255, 99, 132, 1)',  
                    borderWidth: 1,
                    fill: true
                }]
            },
            options: {
                responsive: true,
                scales: {
                    y: {
                        beginAtZero: true
                    }
                }
            }
        });
    } catch (e) {
        console.error('Error parsing data:', e);
    }
});
