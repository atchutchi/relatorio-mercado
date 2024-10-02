document.addEventListener('DOMContentLoaded', function() {
    renderAssinantesChart();
    renderReceitaInvestimentosChart();
    renderTrafegoChart();
    renderChamadasChart();
    renderGrowthTable();
});

function renderAssinantesChart() {
    const ctx = document.getElementById('assinantesChart').getContext('2d');
    new Chart(ctx, {
        type: 'line',
        data: {
            labels: anos,
            datasets: [
                {
                    label: 'Rede Móvel',
                    data: evolutionData.assinantes_rede_movel,
                    borderColor: 'rgb(75, 192, 192)',
                    tension: 0.1
                },
                {
                    label: 'Pós-pago',
                    data: evolutionData.assinantes_pos_pago,
                    borderColor: 'rgb(255, 99, 132)',
                    tension: 0.1
                },
                {
                    label: 'Pré-pago',
                    data: evolutionData.assinantes_pre_pago,
                    borderColor: 'rgb(54, 162, 235)',
                    tension: 0.1
                }
            ]
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
}

function renderReceitaInvestimentosChart() {
    const ctx = document.getElementById('receitaInvestimentosChart').getContext('2d');
    new Chart(ctx, {
        type: 'line',
        data: {
            labels: anos,
            datasets: [
                {
                    label: 'Receita Total',
                    data: evolutionData.receita_total,
                    borderColor: 'rgb(75, 192, 192)',
                    tension: 0.1
                },
                {
                    label: 'Investimentos',
                    data: evolutionData.investimentos,
                    borderColor: 'rgb(255, 99, 132)',
                    tension: 0.1
                }
            ]
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
}

function renderTrafegoChart() {
    const ctx = document.getElementById('trafegoChart').getContext('2d');
    new Chart(ctx, {
        type: 'line',
        data: {
            labels: anos,
            datasets: [
                {
                    label: 'Voz Originado',
                    data: evolutionData.trafego_voz_originado,
                    borderColor: 'rgb(75, 192, 192)',
                    tension: 0.1
                },
                {
                    label: 'SMS',
                    data: evolutionData.trafego_sms,
                    borderColor: 'rgb(255, 99, 132)',
                    tension: 0.1
                },
                {
                    label: 'Dados',
                    data: evolutionData.trafego_dados,
                    borderColor: 'rgb(54, 162, 235)',
                    tension: 0.1
                }
            ]
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
}

function renderChamadasChart() {
    const ctx = document.getElementById('chamadasChart').getContext('2d');
    new Chart(ctx, {
        type: 'line',
        data: {
            labels: anos,
            datasets: [
                {
                    label: 'Originadas',
                    data: evolutionData.chamadas_originadas,
                    borderColor: 'rgb(75, 192, 192)',
                    tension: 0.1
                },
                {
                    label: 'Terminadas',
                    data: evolutionData.chamadas_terminadas,
                    borderColor: 'rgb(255, 99, 132)',
                    tension: 0.1
                }
            ]
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
}

function renderGrowthTable() {
    const tableBody = document.querySelector('#growthTable tbody');
    let tableHtml = '';
    
    for (const [indicador, dados] of Object.entries(growthData)) {
        tableHtml += `
            <tr>
                <td>${formatIndicatorName(indicador)}</td>
                ${dados.map(valor => `<td>${formatNumber(valor, 2)}%</td>`).join('')}
            </tr>
        `;
    }
    
    tableBody.innerHTML = tableHtml;
}

function formatIndicatorName(name) {
    return name.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase());
}

function formatNumber(number, decimals = 0) {
    return new Intl.NumberFormat('fr-FR', { 
        minimumFractionDigits: decimals,
        maximumFractionDigits: decimals 
    }).format(number);
}