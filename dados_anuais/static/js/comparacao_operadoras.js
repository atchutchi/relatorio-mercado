document.addEventListener('DOMContentLoaded', function() {
    function createComparisonChart(elementId, label, dataKey, chartType = 'bar') {
        const ctx = document.getElementById(elementId).getContext('2d');
        new Chart(ctx, {
            type: chartType,
            data: {
                labels: ['MTN', 'Orange', 'Total'],
                datasets: [{
                    label: label,
                    data: [
                        dadosComparacao.mtn[dataKey],
                        dadosComparacao.orange[dataKey],
                        dadosComparacao.total[dataKey]
                    ],
                    backgroundColor: [
                        'rgba(255, 206, 86, 0.8)',
                        'rgba(255, 99, 132, 0.8)',
                        'rgba(54, 162, 235, 0.8)'
                    ]
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
                    legend: {
                        display: false
                    },
                    title: {
                        display: true,
                        text: label
                    }
                }
            }
        });
    }

    function createStackedBarChart(elementId, label, dataKeys) {
        const ctx = document.getElementById(elementId).getContext('2d');
        new Chart(ctx, {
            type: 'bar',
            data: {
                labels: ['MTN', 'Orange', 'Total'],
                datasets: dataKeys.map((key, index) => ({
                    label: key,
                    data: [
                        dadosComparacao.mtn[key],
                        dadosComparacao.orange[key],
                        dadosComparacao.total[key]
                    ],
                    backgroundColor: `rgba(${index * 100}, ${255 - index * 50}, ${index * 75}, 0.8)`
                }))
            },
            options: {
                responsive: true,
                scales: {
                    x: {
                        stacked: true,
                    },
                    y: {
                        stacked: true,
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

    createComparisonChart('assinantesComparacaoChart', 'Assinantes Rede Móvel', 'assinantes_rede_movel');
    createComparisonChart('volumeNegocioComparacaoChart', 'Volume de Negócio (FCFA)', 'volume_negocio');
    createComparisonChart('trafegoVozComparacaoChart', 'Tráfego de Voz (minutos)', 'trafego_voz_originado');

    createStackedBarChart('assinantesTecnologiaComparacaoChart', 'Assinantes por Tecnologia', ['assinantes_3g', 'assinantes_4g']);
    createStackedBarChart('trafegoDadosComparacaoChart', 'Tráfego de Dados', ['trafego_dados_2g', 'trafego_dados_3g', 'trafego_dados_4g']);
});