document.addEventListener('DOMContentLoaded', function() {
    const assinantesCtx = document.getElementById('assinantesChart').getContext('2d');
    new Chart(assinantesCtx, {
        type: 'line',
        data: {
            labels: dadosGraficos.anos,
            datasets: [{
                label: 'Assinantes Rede Móvel',
                data: dadosGraficos.assinantes_rede_movel,
                borderColor: 'rgb(75, 192, 192)',
                tension: 0.1
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

    const volumeNegocioCtx = document.getElementById('volumeNegocioChart').getContext('2d');
    new Chart(volumeNegocioCtx, {
        type: 'bar',
        data: {
            labels: dadosGraficos.anos,
            datasets: [{
                label: 'Volume de Negócio (FCFA)',
                data: dadosGraficos.volume_negocio,
                backgroundColor: 'rgba(255, 99, 132, 0.8)'
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
});