document.addEventListener('DOMContentLoaded', function() {
    console.log('Dados recebidos:', trafegoData);

    if (!trafegoData || !trafegoData.labels || trafegoData.labels.length === 0) {
        console.error('Dados de tráfego inválidos ou vazios');
        return;
    }

    // Gráfico de linha para tráfego total e on-net/off-net
    var ctxTotal = document.getElementById('trafegoTotalChart').getContext('2d');
    new Chart(ctxTotal, {
        type: 'line',
        data: {
            labels: trafegoData.labels,
            datasets: [{
                label: 'Total Tráfego',
                data: trafegoData.total_trafego,
                borderColor: 'rgb(75, 192, 192)',
                tension: 0.1
            }, {
                label: 'On-net',
                data: trafegoData.on_net,
                borderColor: 'rgb(255, 99, 132)',
                tension: 0.1
            }, {
                label: 'Off-net (Saída)',
                data: trafegoData.off_net_saida,
                borderColor: 'rgb(255, 205, 86)',
                tension: 0.1
            }, {
                label: 'Off-net (Entrada)',
                data: trafegoData.off_net_entrada,
                borderColor: 'rgb(54, 162, 235)',
                tension: 0.1
            }]
        },
        options: {
            responsive: true,
            plugins: {
                title: {
                    display: true,
                    text: 'Tráfego Total e On-net/Off-net'
                }
            }
        }
    });

    // Gráfico de linha para tráfego internacional
    var ctxInternacional = document.getElementById('trafegoInternacionalChart').getContext('2d');
    new Chart(ctxInternacional, {
        type: 'line',
        data: {
            labels: trafegoData.labels,
            datasets: [{
                label: 'Saída Internacional',
                data: trafegoData.saida_internacional,
                borderColor: 'rgb(255, 99, 132)',
                tension: 0.1
            }, {
                label: 'Entrada Internacional',
                data: trafegoData.entrada_internacional,
                borderColor: 'rgb(54, 162, 235)',
                tension: 0.1
            }]
        },
        options: {
            responsive: true,
            plugins: {
                title: {
                    display: true,
                    text: 'Tráfego Internacional'
                }
            }
        }
    });

    // Gráfico de barras para tráfego em roaming
    var ctxRoaming = document.getElementById('trafegoRoamingChart').getContext('2d');
    new Chart(ctxRoaming, {
        type: 'bar',
        data: {
            labels: trafegoData.labels,
            datasets: [{
                label: 'Roaming In',
                data: trafegoData.roaming_in,
                backgroundColor: 'rgba(75, 192, 192, 0.2)',
                borderColor: 'rgba(75, 192, 192, 1)',
                borderWidth: 1
            }, {
                label: 'Roaming Out',
                data: trafegoData.roaming_out,
                backgroundColor: 'rgba(255, 99, 132, 0.2)',
                borderColor: 'rgba(255, 99, 132, 1)',
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            plugins: {
                title: {
                    display: true,
                    text: 'Minutos em Roaming'
                }
            },
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });

    // Gráfico de pizza para repartição do tráfego de voz (usando dados do último trimestre)
    var ctxReparticao = document.getElementById('reparticaoTrafegoChart').getContext('2d');
    const lastIndex = trafegoData.labels.length - 1;
    new Chart(ctxReparticao, {
        type: 'pie',
        data: {
            labels: ['On-net', 'Off-net (Saída)', 'Off-net (Entrada)', 'Saída Internacional', 'Entrada Internacional'],
            datasets: [{
                data: [
                    trafegoData.on_net && trafegoData.on_net[lastIndex] || 0,
                    trafegoData.off_net_saida && trafegoData.off_net_saida[lastIndex] || 0,
                    trafegoData.off_net_entrada && trafegoData.off_net_entrada[lastIndex] || 0,
                    trafegoData.saida_internacional && trafegoData.saida_internacional[lastIndex] || 0,
                    trafegoData.entrada_internacional && trafegoData.entrada_internacional[lastIndex] || 0
                ],
                backgroundColor: [
                    'rgba(75, 192, 192, 0.2)',
                    'rgba(255, 99, 132, 0.2)',
                    'rgba(255, 205, 86, 0.2)',
                    'rgba(54, 162, 235, 0.2)',
                    'rgba(153, 102, 255, 0.2)'
                ],
                borderColor: [
                    'rgba(75, 192, 192, 1)',
                    'rgba(255, 99, 132, 1)',
                    'rgba(255, 205, 86, 1)',
                    'rgba(54, 162, 235, 1)',
                    'rgba(153, 102, 255, 1)'
                ],
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            plugins: {
                title: {
                    display: true,
                    text: 'Repartição do Tráfego de Voz (Último Trimestre)'
                }
            }
        }
    });

    // Preencher a tabela de detalhes do tráfego
    const tableBody = document.getElementById('detalhesTrafego');
    const tiposTrafego = ['Total Tráfego', 'On-net', 'Off-net (Saída)', 'Off-net (Entrada)', 'Saída Internacional', 'Entrada Internacional', 'Roaming In', 'Roaming Out'];
    const dadosTrafego = [trafegoData.total_trafego, trafegoData.on_net, trafegoData.off_net_saida, trafegoData.off_net_entrada, trafegoData.saida_internacional, trafegoData.entrada_internacional, trafegoData.roaming_in, trafegoData.roaming_out];

    tiposTrafego.forEach((tipo, index) => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${tipo}</td>
            <td>${dadosTrafego[index][dadosTrafego[index].length - 4].toLocaleString()}</td>
            <td>${dadosTrafego[index][dadosTrafego[index].length - 3].toLocaleString()}</td>
            <td>${dadosTrafego[index][dadosTrafego[index].length - 2].toLocaleString()}</td>
            <td>${dadosTrafego[index][dadosTrafego[index].length - 1].toLocaleString()}</td>
        `;
        tableBody.appendChild(row);
    });
});