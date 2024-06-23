document.addEventListener('DOMContentLoaded', function() {
    try {
        const ctxVentas = document.getElementById('ventasMensual').getContext('2d');

        // Generar etiquetas para los días hasta el día actual
        const labels = Array.from({ length: dayOfMonth }, (_, i) => (i + 1).toString());

        const ventasChart = new Chart(ctxVentas, {
            type: 'line',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Ventas Diarias',
                    data: ventasDiarias,
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
        console.error('Error parsing ventasDiarias:', e);
    }
});
