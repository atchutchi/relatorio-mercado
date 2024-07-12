document.addEventListener('DOMContentLoaded', function() {
    // Dados da quota de mercado (você precisará passar esses dados do backend)
    const quotaData = {{ quota_data|safe }};

    // Gráfico de pizza para quota de mercado atual
    var ctxQuota = document.getElementById('quotaEstacoesChart').getContext('2d');
    const lastIndex = quotaData.labels.length - 1;
    new Chart(ctxQuota, {
        type: 'pie',
        data: {
            labels: ['MTN', 'Orange'],
            datasets: [{
                data: [
                    quotaData.mtn[lastIndex],
                    quotaData.orange[lastIndex]
                ],
                backgroundColor: [
                    'rgba(255, 206, 86, 0.2)',
                    'rgba(75, 192, 192, 0.2)'
                ],
                borderColor: [
                    'rgba(255, 206, 86, 1)',
                    'rgba(75, 192, 192, 1)'
                ],
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            plugins: {
                title: {
                    display: true,
                    text: 'Quota de Mercado Atual'
                }
            }
        }
    });

    // Gráfico de linha para evolução da quota de mercado
    var ctxEvolucao = document.getElementById('evolucaoQuotaChart').getContext('2d');
    new Chart(ctxEvolucao, {
        type: 'line',
        data: {
            labels: quotaData.labels,
            datasets: [{
                label: 'MTN',
                data: quotaData.mtn,
                borderColor: 'rgba(255, 206, 86, 1)',
                tension: 0.1
            }, {
                label: 'Orange',
                data: quotaData.orange,
                borderColor: 'rgba(75, 192, 192, 1)',
                tension: 0.1
            }]
        },
        options: {
            responsive: true,
            plugins: {
                title: {
                    display: true,
                    text: 'Evolução da Quota de Mercado'
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

    // Preencher a tabela de detalhes da quota de mercado
    const tableBody = document.getElementById('detalhesQuota');
    quotaData.labels.forEach((label, index) => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${label}</td>
            <td>${quotaData.mtn[index].toFixed(2)}%</td>
            <td>${quotaData.orange[index].toFixed(2)}%</td>
        `;
        tableBody.appendChild(row);
    });
});