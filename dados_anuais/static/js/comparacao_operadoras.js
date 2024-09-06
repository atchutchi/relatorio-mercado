document.addEventListener('DOMContentLoaded', function() {
    const assinantesCtx = document.getElementById('assinantesComparacaoChart').getContext('2d');
    new Chart(assinantesCtx, {
        type: 'bar',
        data: {
            labels: ['MTN', 'Orange'],
            datasets: [{
                label: 'Assinantes Rede Móvel',
                data: [
                    dadosComparacao.mtn.assinantes_rede_movel,
                    dadosComparacao.orange.assinantes_rede_movel
                ],
                backgroundColor: [
                    'rgba(255, 206, 86, 0.8)',
                    'rgba(255, 159, 64, 0.8)'
                ]
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

    const volumeNegocioCtx = document.getElementById('volumeNegocioComparacaoChart').getContext('2d');
    new Chart(volumeNegocioCtx, {
        type: 'pie',
        data: {
            labels: ['MTN', 'Orange'],
            datasets: [{
                data: [
                    dadosComparacao.mtn.volume_negocio,
                    dadosComparacao.orange.volume_negocio
                ],
                backgroundColor: [
                    'rgba(255, 206, 86, 0.8)',
                    'rgba(255, 159, 64, 0.8)'
                ]
            }]
        },
        options: {
            responsive: true,
            plugins: {
                title: {
                    display: true,
                    text: 'Distribuição do Volume de Negócio'
                }
            }
        }
    });
});