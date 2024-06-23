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

        const ctxVentasSemestral = document.getElementById('ventasSemestral').getContext('2d');
        const ventasSemestralChart = new Chart(ctxVentasSemestral, {
            type: 'line',
            data: {
                labels: labelsMeses,
                datasets: [{
                    label: 'Ventas Semestral',
                    data: ventasSemestralData,
                    backgroundColor: 'rgba(75, 192, 192, 0.2)',
                    borderColor: 'rgba(75, 192, 192, 1)',
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
        console.error('Error parsing ventasSemestralData:', e);
    }
});
