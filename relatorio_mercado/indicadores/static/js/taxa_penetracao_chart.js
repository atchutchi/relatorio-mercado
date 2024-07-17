document.addEventListener('DOMContentLoaded', function() {
    console.log('Dados recebidos:', taxaData);  // Log para depuração

    // Gráfico de linha para evolução da taxa de penetração
    var ctxTaxa = document.getElementById('taxaPenetracaoChart').getContext('2d');
    new Chart(ctxTaxa, {
        type: 'line',
        data: {
            labels: taxaData.labels,
            datasets: [{
                label: 'Taxa de Penetração',
                data: taxaData.taxa_penetracao,
                borderColor: 'rgb(75, 192, 192)',
                tension: 0.1
            }, {
                label: 'Taxa de Penetração 3G',
                data: taxaData.taxa_penetracao_3g,
                borderColor: 'rgb(255, 99, 132)',
                tension: 0.1
            }, {
                label: 'Taxa de Penetração 4G',
                data: taxaData.taxa_penetracao_4g,
                borderColor: 'rgb(54, 162, 235)',
                tension: 0.1
            }]
        },
        options: {
            responsive: true,
            plugins: {
                title: {
                    display: true,
                    text: 'Evolução da Taxa de Penetração'
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    max: 100,
                    ticks: {
                        callback: function(value) {
                            return value + '%';
                        }
                    }
                }
            }
        }
    });

    // Preencher a tabela de detalhes da taxa de penetração
    const tableBody = document.getElementById('detalhesTaxaPenetracao');
    taxaData.labels.forEach((label, index) => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${label}</td>
            <td>${taxaData.numero_estacoes[index].toLocaleString()}</td>
            <td>${taxaData.variacao[index].toLocaleString()}</td>
            <td>${taxaData.taxa_penetracao[index].toFixed(2)}%</td>
            <td>${taxaData.numero_estacoes_3g[index].toLocaleString()} (${taxaData.variacao_3g[index].toLocaleString()}) - ${taxaData.taxa_penetracao_3g[index].toFixed(2)}%</td>
            <td>${taxaData.numero_estacoes_4g[index].toLocaleString()} (${taxaData.variacao_4g[index].toLocaleString()}) - ${taxaData.taxa_penetracao_4g[index].toFixed(2)}%</td>
        `;
        tableBody.appendChild(row);
    });
});