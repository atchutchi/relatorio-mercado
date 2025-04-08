document.addEventListener('DOMContentLoaded', function() {
    if (marketData && marketData.length > 0) {
        renderChart();
        renderMarketSummary();
        // A tabela agora é renderizada diretamente no template via Django
    } else {
        document.querySelector('.container').innerHTML += '<p class="alert alert-warning">Nenhum dado disponível para exibição.</p>';
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
 
 function renderChart() {
    if (!anos || !assinantesTotal || !receitaTotal || !trafegoDadosTotal || !investimentosTotal) {
        return;
    }
    const ctx = document.getElementById('mainIndicatorsChart').getContext('2d');
    new Chart(ctx, {
        type: 'line',
        data: {
            labels: anos,
            datasets: [
                {
                    label: 'Assinantes',
                    data: assinantesTotal,
                    borderColor: operadoraColors.MTN.main,
                    backgroundColor: operadoraColors.MTN.background,
                    tension: 0.1,
                    fill: true
                },
                {
                    label: 'Receita (Bilhões FCFA)',
                    data: receitaTotal.map(value => Number(value) / 1000000000),
                    borderColor: operadoraColors.ORANGE.main,
                    backgroundColor: operadoraColors.ORANGE.background,
                    tension: 0.1,
                    fill: true
                },
                {
                    label: 'Tráfego de Dados (TB)',
                    data: trafegoDadosTotal.map(value => value / 1000000),
                    borderColor: 'rgb(54, 162, 235)',
                    backgroundColor: 'rgba(54, 162, 235, 0.2)',
                    tension: 0.1,
                    fill: true
                },
                {
                    label: 'Investimentos (Bilhões FCFA)',
                    data: investimentosTotal.map(value => Number(value) / 1000000000),
                    borderColor: 'rgb(75, 192, 192)',
                    backgroundColor: 'rgba(75, 192, 192, 0.2)',
                    tension: 0.1,
                    fill: true
                }
            ]
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: true
                }
            },
            plugins: {
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
            }
        }
    });
 }
 
 function renderMarketSummary() {
    if (!marketData || marketData.length === 0) return;
    
    const lastYear = marketData[marketData.length - 1];
    const penultimateYear = marketData.length > 1 ? marketData[marketData.length - 2] : null;
    
    let summaryHtml = `
        <p>Em ${lastYear.ano}, o mercado de telecomunicações atingiu ${formatNumber(lastYear.assinantes_total)} assinantes,
        com uma receita total de ${formatCurrency(lastYear.receita_total)} FCFA.
        O tráfego de dados totalizou ${formatNumber(lastYear.trafego_dados_total)} MB,
        enquanto os investimentos no setor chegaram a ${formatCurrency(lastYear.investimentos_total)} FCFA.</p>
    `;
 
    if (penultimateYear) {
        const indicators = {
            assinantes: {
                atual: lastYear.assinantes_total,
                anterior: penultimateYear.assinantes_total,
                label: 'assinantes'
            },
            receita: {
                atual: lastYear.receita_total,
                anterior: penultimateYear.receita_total,
                label: 'receita'
            },
            trafego: {
                atual: lastYear.trafego_dados_total,
                anterior: penultimateYear.trafego_dados_total,
                label: 'tráfego de dados'
            },
            investimentos: {
                atual: lastYear.investimentos_total,
                anterior: penultimateYear.investimentos_total,
                label: 'investimentos'
            }
        };
 
        let crescimentoHtml = '<p>Comparado ao ano anterior:';
        
        Object.values(indicators).forEach(({ atual, anterior, label }) => {
            const crescimento = ((atual - anterior) / anterior) * 100;
            const cssClass = crescimento >= 0 ? 'positive-growth' : 'negative-growth';
            crescimentoHtml += `
                <br>• ${label}: <span class="${cssClass}">${formatNumber(crescimento, 2)}%</span>`;
        });
 
        summaryHtml += crescimentoHtml + '</p>';
    }
    
    document.getElementById('marketSummary').innerHTML = summaryHtml;
 }
 
 // Função para formatação de números (para uso no JavaScript)
 function formatNumber(number, decimals = 0) {
    return new Intl.NumberFormat('pt-BR', { 
        minimumFractionDigits: decimals,
        maximumFractionDigits: decimals 
    }).format(number);
 }
 
 // Função para formatação de valores monetários
 function formatCurrency(value) {
    return new Intl.NumberFormat('pt-BR', { 
        minimumFractionDigits: 2,
        maximumFractionDigits: 2 
    }).format(value);
 }