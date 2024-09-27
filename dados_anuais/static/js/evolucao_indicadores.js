document.addEventListener('DOMContentLoaded', function() {
    function createEvolutionChart(elementId, label, dataKey, chartType = 'line') {
        const ctx = document.getElementById(elementId).getContext('2d');
        new Chart(ctx, {
            type: chartType,
            data: {
                labels: dadosGraficos.anos,
                datasets: [{
                    label: label,
                    data: dadosGraficos[dataKey],
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
                },
                plugins: {
                    title: {
                        display: true,
                        text: label
                    }
                }
            }
        });
    }

    createEvolutionChart('assinantesEvolucaoChart', 'Assinantes Rede Móvel', 'assinantes_rede_movel');
    createEvolutionChart('volumeNegocioEvolucaoChart', 'Volume de Negócio (FCFA)', 'volume_negocio');
    createEvolutionChart('trafegoDadosEvolucaoChart', 'Tráfego de Dados', 'trafego_dados');
    createEvolutionChart('trafegoVozEvolucaoChart', 'Tráfego de Voz (minutos)', 'trafego_voz_originado');

    // Gráfico de múltiplas linhas para Indicadores Chave
    const ctx = document.getElementById('indicadoresChaveEvolucaoChart').getContext('2d');
    new Chart(ctx, {
        type: 'line',
        data: {
            labels: dadosGraficos.anos,
            datasets: [
                {
                    label: 'Assinantes Rede Móvel',
                    data: dadosGraficos.assinantes_rede_movel,
                    borderColor: 'rgb(75, 192, 192)',
                },
                {
                    label: 'Volume de Negócio',
                    data: dadosGraficos.volume_negocio,
                    borderColor: 'rgb(255, 99, 132)',
                },
                {
                    label: 'Tráfego de Voz',
                    data: dadosGraficos.trafego_voz_originado,
                    borderColor: 'rgb(255, 205, 86)',
                },
                {
                    label: 'Tráfego de Dados',
                    data: dadosGraficos.trafego_dados,
                    borderColor: 'rgb(54, 162, 235)',
                },
                {
                    label: 'Receita Total',
                    data: dadosGraficos.receita_total,
                    borderColor: 'rgb(153, 102, 255)',
                }
            ]
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: true
                }
            },
            plugins: {
                title: {
                    display: true,
                    text: 'Evolução de Indicadores Chave'
                }
            }
        }
    });
});