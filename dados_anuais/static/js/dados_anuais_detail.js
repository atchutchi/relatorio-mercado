document.addEventListener('DOMContentLoaded', function() {
    function createPieChart(elementId, data, labels, title) {
        const ctx = document.getElementById(elementId).getContext('2d');
        new Chart(ctx, {
            type: 'pie',
            data: {
                labels: labels,
                datasets: [{
                    data: data,
                    backgroundColor: [
                        'rgba(255, 99, 132, 0.8)',
                        'rgba(54, 162, 235, 0.8)',
                        'rgba(255, 206, 86, 0.8)',
                        'rgba(75, 192, 192, 0.8)',
                        'rgba(153, 102, 255, 0.8)',
                        'rgba(255, 159, 64, 0.8)'
                    ]
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        position: 'top',
                    },
                    title: {
                        display: true,
                        text: title
                    }
                }
            }
        });
    }

    function createBarChart(elementId, data, labels, title) {
        const ctx = document.getElementById(elementId).getContext('2d');
        new Chart(ctx, {
            type: 'bar',
            data: {
                labels: labels,
                datasets: [{
                    label: title,
                    data: data,
                    backgroundColor: 'rgba(75, 192, 192, 0.8)'
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
                        text: title
                    }
                }
            }
        });
    }

    // Assinantes por Tecnologia
    createPieChart('assinantesTecnologiaChart', 
        [dadosDetalhados.assinantes_3g, dadosDetalhados.assinantes_4g],
        ['3G', '4G'],
        'Assinantes por Tecnologia'
    );

    // Tráfego de Voz
    createBarChart('trafegoVozChart',
        [dadosDetalhados.trafego_voz_on_net, dadosDetalhados.trafego_voz_off_net, dadosDetalhados.trafego_voz_internacional],
        ['On-Net', 'Off-Net', 'Internacional'],
        'Tráfego de Voz (minutos)'
    );

    // Tráfego de Dados
    createBarChart('trafegoDadosChart',
        [dadosDetalhados.trafego_dados_2g, dadosDetalhados.trafego_dados_3g, dadosDetalhados.trafego_dados_4g],
        ['2G', '3G', '4G'],
        'Tráfego de Dados'
    );

    // Distribuição de Receitas
    createPieChart('receitasChart',
        [dadosDetalhados.receita_servicos_voz, dadosDetalhados.receita_servicos_mensagens, dadosDetalhados.receita_dados_moveis, dadosDetalhados.receita_roaming_out],
        ['Serviços de Voz', 'Serviços de Mensagens', 'Dados Móveis', 'Roaming Out'],
        'Distribuição de Receitas'
    );
});