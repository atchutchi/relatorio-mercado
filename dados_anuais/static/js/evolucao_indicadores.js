document.addEventListener('DOMContentLoaded', function() {
    function createEvolutionChart(elementId, label, dataKey, chartType = 'line') {
        const ctx = document.getElementById(elementId).getContext('2d');
        new Chart(ctx, {
            type: chartType,
            data: {
                labels: dadosEvolucao.anos,
                datasets: [{
                    label: label,
                    data: dadosEvolucao[dataKey],
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

    function createMultiLineChart(elementId, datasets) {
        const ctx = document.getElementById(elementId).getContext('2d');
        new Chart(ctx, {
            type: 'line',
            data: {
                labels: dadosEvolucao.anos,
                datasets: datasets.map((dataset, index) => ({
                    label: dataset.label,
                    data: dadosEvolucao[dataset.dataKey],
                    borderColor: `hsl(${index * 360 / datasets.length}, 70%, 50%)`,
                    tension: 0.1
                }))
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
    }

    createEvolutionChart('assinantesEvolucaoChart', 'Assinantes Rede Móvel', 'assinantes_rede_movel');
    createEvolutionChart('volumeNegocioEvolucaoChart', 'Volume de Negócio (FCFA)', 'volume_negocio');
    createEvolutionChart('trafegoDadosEvolucaoChart', 'Tráfego de Dados', 'trafego_dados');
    createEvolutionChart('trafegoVozEvolucaoChart', 'Tráfego de Voz (minutos)', 'trafego_voz_originado');

    createMultiLineChart('indicadoresChaveEvolucaoChart', [
        { label: 'Assinantes Rede Móvel', dataKey: 'assinantes_rede_movel' },
        { label: 'Volume de Negócio', dataKey: 'volume_negocio' },
        { label: 'Investimentos', dataKey: 'investimentos' },
        { label: 'Receita Total', dataKey: 'receita_total' }
    ]);
});