document.addEventListener('DOMContentLoaded', function() {
    const assinantesCtx = document.getElementById('assinantesEvolucaoChart').getContext('2d');
    new Chart(assinantesCtx, {
        type: 'line',
        data: {
            labels: dadosEvolucao.anos,
            datasets: [{
                label: 'Assinantes Rede Móvel',
                data: dadosEvolucao.assinantes_rede_movel,
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

    const volumeNegocioCtx = document.getElementById('volumeNegocioEvolucaoChart').getContext('2d');
    new Chart(volumeNegocioCtx, {
        type: 'line',
        data: {
            labels: dadosEvolucao.anos,
            datasets: [{
                label: 'Volume de Negócio (FCFA)',
                data: dadosEvolucao.volume_negocio,
                borderColor: 'rgb(255, 99, 132)',
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

    const trafegoDadosCtx = document.getElementById('trafegoDadosEvolucaoChart').getContext('2d');
    new Chart(trafegoDadosCtx, {
        type: 'line',
        data: {
            labels: dadosEvolucao.anos,
            datasets: [{
                label: 'Tráfego de Dados (MB)',
                data: dadosEvolucao.trafego_dados,
                borderColor: 'rgb(54, 162, 235)',
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
});