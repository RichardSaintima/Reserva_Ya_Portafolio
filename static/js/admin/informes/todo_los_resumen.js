document.addEventListener('DOMContentLoaded', function() {
    try {
        const ctx = document.getElementById('informeMensual').getContext('2d');

        const labelsDias = Array.from({ length: dayOrdenfMonth }, (_, i) => (i + 1).toString());

        const informeMensualChart = new Chart(ctx, {
            type: 'bar',
            data: {
                labels: labelsDias,
                datasets: [
                    {
                        type: 'bar',
                        label: 'Ventas Diarias',
                        data: ventasDiariasGeneral,
                        backgroundColor: 'rgba(75, 192, 192, 0.2)',
                        borderColor: 'rgba(75, 192, 192, 1)',
                        borderWidth: 1,
                        yAxisID: 'y',
                    },
                    {
                        type: 'bar',
                        label: 'Cancha Data',
                        data: canchaDataGeneral,
                        backgroundColor: 'rgba(255, 99, 132, 0.2)', 
                        borderColor: 'rgba(255, 99, 132, 1)',  
                        borderWidth: 2,
                        fill: false,
                        yAxisID: 'y',
                    },
                    {
                        type: 'bar',
                        label: 'Orden Data',
                        data: ordenDataGeneral,
                        backgroundColor: 'rgba(255, 205, 86, 0.2)',
                        borderColor: 'rgba(255, 205, 86, 1)',
                        borderWidth: 1,
                        yAxisID: 'y',
                    }
                ]
            },
            options: {
                responsive: true,
                scales: {
                    y: {
                        beginAtZero: true,
                        type: 'linear',
                        position: 'left',
                    },
                    y1: {
                        beginAtZero: true,
                        type: 'linear',
                        position: 'right',
                        grid: {
                            drawOnChartArea: false, 
                        },
                    },
                }
            }
        });
    } catch (e) {
        console.error('Error parsing data:', e);
    }
});
