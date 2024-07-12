document.addEventListener('DOMContentLoaded', function() {
    // Dados da taxa de penetração (você precisará passar esses dados do backend)
    const taxaData = {{ taxa_data|safe }};

    // Gráfico de linha para evolução da taxa de penetração
    var ctxTaxa = document.getElementById('taxaPenetracaoChart').getContext('2d');
    new Chart(ctxTaxa, {
        type: 'line',
        data: {
            labels: taxaData.labels,
            datasets: [{
                label: 'Taxa de Penetração',
                data: taxaData.taxa_geral,
                borderColor: 'rgb(75, 192, 192)',
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

    // Gráfico de linha para taxa de penetração 3G
    var ctx3G = document.getElementById('taxaPenetracao3GChart').getContext('2d');
    new Chart(ctx3G, {
        type: 'line',
        data: {
            labels: taxaData.labels,
            datasets: [{
                label: 'Taxa de Penetração 3G',
                data: taxaData.taxa_3g,
                borderColor: 'rgb(255, 99, 132)',
                tension: 0.1
            }]
        },
        options: {
            responsive: true,
            plugins: {
                title: {
                    display: true,
                    text: 'Evolução da Taxa de Penetração 3G'
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

    // Gráfico de linha para taxa de penetração 4G
    var ctx4G = document.getElementById('taxaPenetracao4GChart').getContext('2d');
    new Chart(ctx4G, {
        type: 'line',
        data: {
            labels: taxaData.labels,
            datasets: [{
                label: 'Taxa de Penetração 4G',
                data: taxaData.taxa_4g,
                borderColor: 'rgb(54, 162, 235)',
                tension: 0.1
            }]
        },
        options: {
            responsive: true,
            plugins: {
                title: {
                    display: true,
                    text: 'Evolução da Taxa de Penetração 4G'
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
            <td>${taxaData.taxa_geral[index].toFixed(2)}%</td>
            <td>${taxaData.taxa_3g[index].toFixed(2)}%</td>
            <td>${taxaData.taxa_4g[index].toFixed(2)}%</td>
        `;
        tableBody.appendChild(row);
    });
});