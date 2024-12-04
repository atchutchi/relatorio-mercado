// static/js/market_evolution.js
document.addEventListener('DOMContentLoaded', function() {
    if (evolution_data && evolution_data.length > 0) {
        renderCharts();
        renderAnalise();
    } else {
        document.querySelector('.container').innerHTML += '<p class="alert alert-warning">Nenhum dado disponível.</p>';
    }
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
    renderAssinantesChart();
    renderBandaLargaMovelChart();
    renderBandaLargaFixaChart();
    renderReceitaChart();
    renderTrafegoDadosChart();
    renderInvestimentosChart();
}

function renderAssinantesChart() {
    const ctx = document.getElementById('assinantesChart').getContext('2d');
    new Chart(ctx, {
        type: 'line',
        data: {
            labels: anos,
            datasets: [{
                label: 'Total de Assinantes',
                data: assinantesTotal,
                borderColor: operadoraColors.MTN.main,
                backgroundColor: operadoraColors.MTN.background,
                tension: 0.1,
                fill: true
            }]
        },
        options: getChartOptions('Evolução de Assinantes')
    });
}

function renderBandaLargaMovelChart() {
    const ctx = document.getElementById('bandaLargaMovelChart').getContext('2d');
    new Chart(ctx, {
        type: 'line',
        data: {
            labels: anos,
            datasets: [
                {
                    label: 'Total',
                    data: evolution_data.map(d => d.banda_larga_movel.total),
                    borderColor: operadoraColors.MTN.main,
                    backgroundColor: operadoraColors.MTN.background,
                    tension: 0.1,
                    fill: true
                },
                {
                    label: '3G',
                    data: evolution_data.map(d => d.banda_larga_movel['3g']),
                    borderColor: operadoraColors.ORANGE.main,
                    backgroundColor: operadoraColors.ORANGE.background,
                    tension: 0.1,
                    fill: true
                },
                {
                    label: '4G',
                    data: evolution_data.map(d => d.banda_larga_movel['4g']),
                    borderColor: 'rgb(75, 192, 192)',
                    backgroundColor: 'rgba(75, 192, 192, 0.2)',
                    tension: 0.1,
                    fill: true
                }
            ]
        },
        options: getChartOptions('Evolução da Banda Larga Móvel')
    });
}

function renderBandaLargaFixaChart() {
    const ctx = document.getElementById('bandaLargaFixaChart').getContext('2d');
    new Chart(ctx, {
        type: 'line',
        data: {
            labels: anos,
            datasets: [
                {
                    label: 'Total',
                    data: evolution_data.map(d => d.banda_larga_fixa.total),
                    borderColor: operadoraColors.MTN.main,
                    backgroundColor: operadoraColors.MTN.background,
                    tension: 0.1,
                    fill: true
                },
                {
                    label: '256 Kbps',
                    data: evolution_data.map(d => d.banda_larga_fixa['256k']),
                    borderColor: operadoraColors.ORANGE.main,
                    backgroundColor: operadoraColors.ORANGE.background,
                    tension: 0.1,
                    fill: true
                },
                {
                    label: '256K-2M',
                    data: evolution_data.map(d => d.banda_larga_fixa['256k_2m']),
                    borderColor: 'rgb(75, 192, 192)',
                    backgroundColor: 'rgba(75, 192, 192, 0.2)',
                    tension: 0.1,
                    fill: true
                },
                {
                    label: '2M-4M',
                    data: evolution_data.map(d => d.banda_larga_fixa['2m_4m']),
                    borderColor: 'rgb(54, 162, 235)',
                    backgroundColor: 'rgba(54, 162, 235, 0.2)',
                    tension: 0.1,
                    fill: true
                }
            ]
        },
        options: getChartOptions('Evolução da Banda Larga Fixa')
    });
}

function renderReceitaChart() {
    const ctx = document.getElementById('receitaChart').getContext('2d');
    new Chart(ctx, {
        type: 'line',
        data: {
            labels: anos,
            datasets: [{
                label: 'Receita Total (Bilhões FCFA)',
                data: receitaTotal.map(value => Number(value) / 1000000000),
                borderColor: operadoraColors.MTN.main,
                backgroundColor: operadoraColors.MTN.background,
                tension: 0.1,
                fill: true
            }]
        },
        options: getChartOptions('Evolução da Receita')
    });
}

function renderTrafegoDadosChart() {
    const ctx = document.getElementById('trafegoDadosChart').getContext('2d');
    new Chart(ctx, {
        type: 'line',
        data: {
            labels: anos,
            datasets: [{
                label: 'Tráfego de Dados (TB)',
                data: trafegoDadosTotal.map(value => value / 1000000),
                borderColor: operadoraColors.ORANGE.main,
                backgroundColor: operadoraColors.ORANGE.background,
                tension: 0.1,
                fill: true
            }]
        },
        options: getChartOptions('Evolução do Tráfego de Dados')
    });
}

function renderInvestimentosChart() {
    const ctx = document.getElementById('investimentosChart').getContext('2d');
    new Chart(ctx, {
        type: 'line',
        data: {
            labels: anos,
            datasets: [{
                label: 'Investimentos (Bilhões FCFA)',
                data: investimentosTotal.map(value => Number(value) / 1000000000),
                borderColor: operadoraColors.MTN.main,
                backgroundColor: operadoraColors.MTN.background,
                tension: 0.1,
                fill: true
            }]
        },
        options: getChartOptions('Evolução dos Investimentos')
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
                    display: false
                }
            }
        }
    };
 }
 
 function renderAnalise() {
    const analiseDiv = document.getElementById('analiseTexto');
    const ultimoAno = anos[anos.length - 1];
    const penultimoAno = anos.length > 1 ? anos[anos.length - 2] : null;
    
    let lastYearData = evolution_data.find(d => d.ano == ultimoAno);
    let prevYearData = penultimoAno ? evolution_data.find(d => d.ano == penultimoAno) : null;
 
    let analiseHtml = `
        <p>Em ${ultimoAno}, o mercado apresentou:</p>
        <ul>
            <li>Assinantes: ${formatNumber(lastYearData.assinantes_total)}</li>
            <li>Banda Larga Móvel: 
                <ul>
                    <li>Total: ${formatNumber(lastYearData.banda_larga_movel.total)}</li>
                    <li>3G: ${formatNumber(lastYearData.banda_larga_movel['3g'])}</li>
                    <li>4G: ${formatNumber(lastYearData.banda_larga_movel['4g'])}</li>
                </ul>
            </li>
            <li>Banda Larga Fixa:
                <ul>
                    <li>Total: ${formatNumber(lastYearData.banda_larga_fixa.total)}</li>
                    <li>256 Kbps: ${formatNumber(lastYearData.banda_larga_fixa['256k'])}</li>
                    <li>256K-2M: ${formatNumber(lastYearData.banda_larga_fixa['256k_2m'])}</li>
                    <li>2M-4M: ${formatNumber(lastYearData.banda_larga_fixa['2m_4m'])}</li>
                </ul>
            </li>
            <li>Receita: ${formatNumber(lastYearData.receita_total)} FCFA</li>
            <li>Tráfego de Dados: ${formatNumber(lastYearData.trafego_dados)} MB</li>
            <li>Investimentos: ${formatNumber(lastYearData.investimentos)} FCFA</li>
        </ul>
    `;
 
    if (prevYearData) {
        const indicadores = {
            assinantes: ['assinantes_total', 'Assinantes'],
            bandaLargaMovelTotal: ['banda_larga_movel.total', 'Banda Larga Móvel Total'],
            bandaLargaMovel3G: ['banda_larga_movel.3g', '3G'],
            bandaLargaMovel4G: ['banda_larga_movel.4g', '4G'],
            bandaLargaFixaTotal: ['banda_larga_fixa.total', 'Banda Larga Fixa Total'],
            receita: ['receita_total', 'Receita'],
            trafego: ['trafego_dados', 'Tráfego de Dados'],
            investimentos: ['investimentos', 'Investimentos']
        };
 
        let crescimentoHtml = '<p>Crescimento em relação ao ano anterior:</p><ul>';
        
        Object.entries(indicadores).forEach(([key, [campo, nome]]) => {
            const campoPath = campo.split('.');
            let atual = lastYearData;
            let anterior = prevYearData;
            
            // Acessar propriedades aninhadas se necessário
            for(const prop of campoPath) {
                atual = atual[prop];
                anterior = anterior[prop];
            }
            
            const crescimento = ((atual - anterior) / anterior) * 100;
            
            crescimentoHtml += `
                <li>${nome}: <span style="color: ${crescimento >= 0 ? operadoraColors.MTN.main : '#dc3545'}; font-weight: 500;">
                    ${crescimento > 0 ? '+' : ''}${formatNumber(crescimento, 2)}%
                </span></li>`;
        });
 
        analiseHtml += crescimentoHtml + '</ul>';
    }
 
    analiseDiv.innerHTML = analiseHtml;
 }
 
 function formatNumber(number, decimals = 0) {
    return new Intl.NumberFormat('pt-BR', {
        minimumFractionDigits: decimals,
        maximumFractionDigits: decimals
    }).format(number);
 }