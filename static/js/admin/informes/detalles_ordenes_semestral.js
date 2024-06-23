document.addEventListener('DOMContentLoaded', function() {
    try {
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

        const labelsMeses = generateLastSixMonths();

        const ctxOrden = document.getElementById('ordenSemestral').getContext('2d');
        const ordenChart = new Chart(ctxOrden, {
            type: 'line',
            data: {
                labels: labelsMeses,
                datasets: [{
                    label: 'Ordenes Semestral',
                    data: ordenSemestralData,
                    backgroundColor: 'rgba(255, 205, 86, 0.2)',
                    borderColor: 'rgba(255, 205, 86, 1)',
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
        console.error('Error parsing ventasData:', e);
    }
});
