document.addEventListener('DOMContentLoaded', function() {
    try {
        const ctxOrden = document.getElementById('ordenMensual').getContext('2d');

        // Generar etiquetas para los días hasta el día actual
        const labels = Array.from({ length: dayOrdenfMonth }, (_, i) => (i + 1).toString());

        const ordenSemestralChart = new Chart(ctxOrden, {
            type: 'line',
            data: {
                labels: labels,
                datasets: [{
                    label: 'Ventas Diarias',
                    data: ordenDiarias,
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
        console.error('Error parsing ordenDiarias:', e);
    }
});
