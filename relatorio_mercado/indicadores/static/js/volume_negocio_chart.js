document.addEventListener('DOMContentLoaded', function() {
    // Dados do volume de negócios (você precisará passar esses dados do backend)
    const volumeData = {{ volume_data|safe }};

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
                borderColor: 'rgb(255, 206, 86)',
                tension: 0.1
            }, {
                label: 'Orange',
                data: volumeData.orange,
                borderColor: 'rgb(255, 99, 132)',
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
                    volumeData.mtn[lastIndex],
                    volumeData.orange[lastIndex]
                ],
                backgroundColor: [
                    'rgba(255, 206, 86, 0.2)',
                    'rgba(255, 99, 132, 0.2)'
                ],
                borderColor: [
                    'rgba(255, 206, 86, 1)',
                    'rgba(255, 99, 132, 1)'
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
            <td>${formatFCFA(volumeData.mtn[index])}</td>
            <td>${formatFCFA(volumeData.orange[index])}</td>
            <td>${formatFCFA(volumeData.total[index])}</td>
        `;
        tableBody.appendChild(row);
    });
});