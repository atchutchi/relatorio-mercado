document.addEventListener('DOMContentLoaded', function() {
    console.log('Dados recebidos:', volumeData);  // Log para depuração

    // Função para formatar valores em FCFA
    function formatFCFA(value) {
        return new Intl.NumberFormat('fr-FR', { style: 'currency', currency: 'XOF' }).format(value);
    }

    // Gráfico de linha para evolução do volume de negócios
    var ctxVolume = document.getElementById('volumeNegocioChart').getContext('2d');
    new Chart(ctxVolume, {
        type: 'line',
        data: {
            labels: volumeData.labels,
            datasets: [{
                label: 'MTN',
                data: volumeData.mtn,
                borderColor: 'rgb(255, 204, 0)',
                tension: 0.1
            }, {
                label: 'Orange',
                data: volumeData.orange,
                borderColor: 'rgb(255, 140, 0)',
                tension: 0.1
            }, {
                label: 'Total',
                data: volumeData.total,
                borderColor: 'rgb(75, 192, 192)',
                tension: 0.1
            }]
        },
        options: {
            responsive: true,
            plugins: {
                title: {
                    display: true,
                    text: 'Evolução do Volume de Negócios'
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        callback: function(value) {
                            return formatFCFA(value);
                        }
                    }
                }
            }
        }
    });

    // Gráfico de pizza para distribuição do volume de negócios
    var ctxDistribuicao = document.getElementById('distribuicaoVolumeChart').getContext('2d');
    const lastIndex = volumeData.labels.length - 1;
    new Chart(ctxDistribuicao, {
        type: 'pie',
        data: {
            labels: ['MTN', 'Orange'],
            datasets: [{
                data: [
                    volumeData.percentagem_mtn[lastIndex],
                    volumeData.percentagem_orange[lastIndex]
                ],
                backgroundColor: [
                    'rgba(255, 204, 0, 0.7)', // Amarelo para MTN
                    'rgba(255, 140, 0, 0.7)', // Laranja para Orange
                ],
                borderColor: [
                    'rgb(255, 204, 0)',
                    'rgb(255, 140, 0)',
                ],
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            plugins: {
                title: {
                    display: true,
                    text: 'Distribuição do Volume de Negócios (Último Trimestre)'
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            let label = context.label || '';
                            if (label) {
                                label += ': ';
                            }
                            if (context.parsed !== null) {
                                label += new Intl.NumberFormat('pt-BR', { style: 'percent', minimumFractionDigits: 2 }).format(context.parsed / 100);
                            }
                            return label;
                        }
                    }
                }
            }
        }
    });

    // Exibir o volume de negócios global
    const volumeGlobal = document.getElementById('volumeGlobal');
    volumeGlobal.textContent = `Volume Global de Negócios: ${formatFCFA(volumeData.total[lastIndex])}`;

    // Preencher a tabela de detalhes do volume de negócios
    const tableBody = document.getElementById('detalhesVolumeNegocio');
    volumeData.labels.forEach((label, index) => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${label}</td>
            <td>${formatFCFA(volumeData.mtn[index])} (${volumeData.percentagem_mtn[index].toFixed(2)}%)</td>
            <td>${formatFCFA(volumeData.orange[index])} (${volumeData.percentagem_orange[index].toFixed(2)}%)</td>
            <td>${formatFCFA(volumeData.total[index])}</td>
        `;
        tableBody.appendChild(row);
    });
});