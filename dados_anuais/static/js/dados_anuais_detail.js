document.addEventListener('DOMContentLoaded', function() {
    const assinantesTecnologiaCtx = document.getElementById('assinantesTecnologiaChart').getContext('2d');
    new Chart(assinantesTecnologiaCtx, {
        type: 'pie',
        data: {
            labels: ['3G', '4G'],
            datasets: [{
                data: [dados.assinantes_3g, dados.assinantes_4g],
                backgroundColor: [
                    'rgba(255, 99, 132, 0.8)',
                    'rgba(54, 162, 235, 0.8)'
                ]
            }]
        },
        options: {
            responsive: true,
            plugins: {
                title: {
                    display: true,
                    text: 'Assinantes por Tecnologia'
                }
            }
        }
    });

    const trafegoVozCtx = document.getElementById('trafegoVozChart').getContext('2d');
    new Chart(trafegoVozCtx, {
        type: 'bar',
        data: {
            labels: ['On-Net', 'Off-Net', 'Internacional'],
            datasets: [{
                label: 'Tráfego de Voz (minutos)',
                data: [
                    dados.trafego_voz_on_net,
                    dados.trafego_voz_off_net,
                    dados.trafego_voz_internacional
                ],
                backgroundColor: [
                    'rgba(75, 192, 192, 0.8)',
                    'rgba(153, 102, 255, 0.8)',
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
});