document.addEventListener('DOMContentLoaded', function() {
    const criarGrafico = (elementId, label, data, color) => {
        const ctx = document.getElementById(elementId).getContext('2d');
        new Chart(ctx, {
            type: 'line',
            data: {
                labels: dadosEvolucao.anos,
                datasets: [{
                    label: label,
                    data: data,
                    borderColor: color,
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
    };

    criarGrafico('assinantesEvolucaoChart', 'Assinantes Rede Móvel', dadosEvolucao.assinantes_rede_movel, 'rgb(75, 192, 192)');
    criarGrafico('volumeNegocioEvolucaoChart', 'Volume de Negócio (FCFA)', dadosEvolucao.volume_negocio, 'rgb(255, 99, 132)');
    criarGrafico('trafegoDadosEvolucaoChart', 'Tráfego de Dados (MB)', dadosEvolucao.trafego_dados, 'rgb(54, 162, 235)');

    // Criar gráficos para todos os outros indicadores
    Object.keys(dadosEvolucao).forEach((indicador, index) => {
        if (!['anos', 'assinantes_rede_movel', 'volume_negocio', 'trafego_dados'].includes(indicador)) {
            const elementId = `chart-${indicador}`;
            const canvas = document.createElement('canvas');
            canvas.id = elementId;
            document.querySelector('.container').appendChild(canvas);

            criarGrafico(elementId, indicador.replace(/_/g, ' ').toUpperCase(), dadosEvolucao[indicador], `hsl(${index * 137.5 % 360}, 70%, 50%)`);
        }
    });
});