document.addEventListener('DOMContentLoaded', function() {
    console.log('Dados recebidos:', quotaData);  // Log para depuração

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
                borderColor: 'rgb(255, 204, 0)',
                tension: 0.1
            }, {
                label: 'Orange',
                data: quotaData.orange,
                borderColor: 'rgb(255, 140, 0)',
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