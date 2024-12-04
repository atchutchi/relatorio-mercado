document.addEventListener('DOMContentLoaded', function() {
    renderCharts();
    renderGrowthTable();
 });
 
 const operadoraColors = {
    MTN: {
        main: 'rgb(255, 206, 86)',
        background: 'rgba(255, 206, 86, 0.2)'
    },
    ORANGE: {
        main: 'rgb(255, 159, 64)',
        background: 'rgba(255, 159, 64, 0.2)'
    }
 };
 
 function renderCharts() {
    const currentOperadora = document.querySelector('h1').textContent.split(' ')[2]; // Gets "MTN" or "ORANGE" from title
    const color = operadoraColors[currentOperadora];
 
    renderAssinantesChart(color);
    renderReceitaInvestimentosChart(color);
    renderTrafegoChart(color);
    renderChamadasChart(color);
 }
 
 function renderAssinantesChart(color) {
    const ctx = document.getElementById('assinantesChart').getContext('2d');
    new Chart(ctx, {
        type: 'line',
        data: {
            labels: anos,
            datasets: [
                {
                    label: 'Rede Móvel',
                    data: evolutionData.assinantes_rede_movel,
                    borderColor: color.main,
                    backgroundColor: color.background,
                    tension: 0.1,
                    fill: true
                },
                {
                    label: 'Pós-pago',
                    data: evolutionData.assinantes_pos_pago,
                    borderColor: 'rgba(75, 192, 192)',
                    backgroundColor: 'rgba(75, 192, 192, 0.2)',
                    tension: 0.1,
                    fill: true
                },
                {
                    label: 'Pré-pago',
                    data: evolutionData.assinantes_pre_pago,
                    borderColor: 'rgba(54, 162, 235)',
                    backgroundColor: 'rgba(54, 162, 235, 0.2)',
                    tension: 0.1,
                    fill: true
                }
            ]
        },
        options: getChartOptions('Evolução de Assinantes')
    });
 }
 
 function renderReceitaInvestimentosChart(color) {
    const ctx = document.getElementById('receitaInvestimentosChart').getContext('2d');
    new Chart(ctx, {
        type: 'line',
        data: {
            labels: anos,
            datasets: [
                {
                    label: 'Receita Total',
                    data: evolutionData.receita_total,
                    borderColor: color.main,
                    backgroundColor: color.background,
                    tension: 0.1,
                    fill: true
                },
                {
                    label: 'Investimentos',
                    data: evolutionData.investimentos,
                    borderColor: 'rgba(75, 192, 192)',
                    backgroundColor: 'rgba(75, 192, 192, 0.2)',
                    tension: 0.1,
                    fill: true
                }
            ]
        },
        options: getChartOptions('Receita e Investimentos')
    });
 }
 
 function renderTrafegoChart(color) {
    const ctx = document.getElementById('trafegoChart').getContext('2d');
    new Chart(ctx, {
        type: 'line',
        data: {
            labels: anos,
            datasets: [
                {
                    label: 'Voz',
                    data: evolutionData.trafego_voz_originado,
                    borderColor: color.main,
                    backgroundColor: color.background,
                    tension: 0.1,
                    fill: true
                },
                {
                    label: 'SMS',
                    data: evolutionData.trafego_sms,
                    borderColor: 'rgba(75, 192, 192)',
                    backgroundColor: 'rgba(75, 192, 192, 0.2)',
                    tension: 0.1,
                    fill: true
                },
                {
                    label: 'Dados',
                    data: evolutionData.trafego_dados,
                    borderColor: 'rgba(54, 162, 235)',
                    backgroundColor: 'rgba(54, 162, 235, 0.2)',
                    tension: 0.1,
                    fill: true
                }
            ]
        },
        options: getChartOptions('Evolução de Tráfego')
    });
 }
 
 function renderChamadasChart(color) {
    const ctx = document.getElementById('chamadasChart').getContext('2d');
    new Chart(ctx, {
        type: 'line',
        data: {
            labels: anos,
            datasets: [
                {
                    label: 'Originadas',
                    data: evolutionData.chamadas_originadas,
                    borderColor: color.main,
                    backgroundColor: color.background,
                    tension: 0.1,
                    fill: true
                },
                {
                    label: 'Terminadas',
                    data: evolutionData.chamadas_terminadas,
                    borderColor: 'rgba(75, 192, 192)',
                    backgroundColor: 'rgba(75, 192, 192, 0.2)',
                    tension: 0.1,
                    fill: true
                }
            ]
        },
        options: getChartOptions('Evolução de Chamadas')
    });
 }
 
 function getChartOptions(title) {
    return {
        responsive: true,
        plugins: {
            title: {
                display: true,
                text: title,
                font: {
                    family: 'Poppins',
                    size: 16
                }
            },
            legend: {
                labels: {
                    font: {
                        family: 'Poppins'
                    }
                }
            },
            tooltip: {
                backgroundColor: 'rgba(0, 0, 0, 0.8)',
                titleFont: {
                    family: 'Poppins',
                    size: 14
                },
                bodyFont: {
                    family: 'Poppins',
                    size: 13
                }
            }
        },
        scales: {
            y: {
                beginAtZero: true,
                grid: {
                    color: 'rgba(0, 0, 0, 0.1)'
                }
            },
            x: {
                grid: {
                    color: 'rgba(0, 0, 0, 0.1)'
                }
            }
        }
    };
 }
 
 function renderGrowthTable() {
    const tableHead = document.querySelector('#growthTable thead tr');
    const tableBody = document.querySelector('#growthTable tbody');
    const currentOperadora = document.querySelector('h1').textContent.split(' ')[2];
    const color = operadoraColors[currentOperadora];
 
    let headerHtml = '<th>Indicador</th>';
    for (let i = 1; i < anos.length; i++) {
        headerHtml += `<th>${anos[i]}</th>`;
    }
    tableHead.innerHTML = headerHtml;
 
    let bodyHtml = '';
    for (const [indicador, dados] of Object.entries(growthData)) {
        bodyHtml += `
            <tr>
                <td>${formatIndicatorName(indicador)}</td>
                ${dados.map(valor => {
                    const growthColor = valor >= 0 ? color.main : '#dc3545';
                    return `<td style="color: ${growthColor}; font-weight: 500;">${formatNumber(valor, 2)}%</td>`;
                }).join('')}
            </tr>
        `;
    }
    tableBody.innerHTML = bodyHtml;
 }
 
 function formatIndicatorName(name) {
    return name.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase());
 }
 
 function formatNumber(number, decimals = 0) {
    return new Intl.NumberFormat('pt-BR', { 
        minimumFractionDigits: decimals,
        maximumFractionDigits: decimals 
    }).format(number);
 }