document.addEventListener('DOMContentLoaded', function() {
    populateYearSelect();
    renderMarketShareChart(anos[anos.length - 1]);
    renderHHIChart();
    renderVolumeNegocioChart();
    renderInvestimentosChart();
    renderTrafegoDadosChart();
    renderEmpregoChart();
    updateCompetitiveAnalysis();
});

function populateYearSelect() {
    const yearSelect = document.getElementById('yearSelect');
    anos.forEach(ano => {
        const option = document.createElement('option');
        option.value = ano;
        option.textContent = ano;
        yearSelect.appendChild(option);
    });
    yearSelect.value = anos[anos.length - 1];
    yearSelect.addEventListener('change', function() {
        renderMarketShareChart(this.value);
    });
}

function renderMarketShareChart(selectedYear) {
    const ctx = document.getElementById('marketShareChart').getContext('2d');
    
    // Verifica se o gráfico já existe antes de tentar destruí-lo
    if (window.marketShareChart instanceof Chart) {
        window.marketShareChart.destroy();
    }

    // Verifica se os dados existem para o ano selecionado
    if (!marketShareData[selectedYear]) {
        console.error(`Não há dados de participação de mercado para o ano ${selectedYear}`);
        return;
    }

    window.marketShareChart = new Chart(ctx, {
        type: 'pie',
        data: {
            labels: operadoras,
            datasets: [{
                data: operadoras.map(op => marketShareData[selectedYear][op] || 0),
                backgroundColor: [
                    'rgba(255, 99, 132, 0.8)',
                    'rgba(54, 162, 235, 0.8)',
                    'rgba(255, 206, 86, 0.8)',
                    'rgba(75, 192, 192, 0.8)'
                ]
            }]
        },
        options: {
            responsive: true,
            plugins: {
                title: {
                    display: true,
                    text: `Participação de Mercado em ${selectedYear}`
                }
            }
        }
    });
}

function renderHHIChart() {
    renderLineChart('hhiChart', 'HHI', anos, anos.map(ano => hhiData[ano]));
}

function renderVolumeNegocioChart() {
    renderStackedBarChart('volumeNegocioChart', 'Volume de Negócio', volumeNegocioData);
}

function renderInvestimentosChart() {
    renderStackedBarChart('investimentosChart', 'Investimentos', investimentosData);
}

function renderTrafegoDadosChart() {
    renderStackedBarChart('trafegoDadosChart', 'Tráfego de Dados', trafegoDadosData);
}

function renderEmpregoChart() {
    renderStackedBarChart('empregoChart', 'Emprego', empregoData);
}

function renderLineChart(canvasId, label, labels, data) {
    const ctx = document.getElementById(canvasId).getContext('2d');
    new Chart(ctx, {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
                label: label,
                data: data,
                borderColor: 'rgb(75, 192, 192)',
                tension: 0.1
            }]
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

function renderStackedBarChart(canvasId, title, data) {
    const ctx = document.getElementById(canvasId).getContext('2d');
    const datasets = operadoras.map((op, index) => ({
        label: op,
        data: anos.map(ano => data[ano][op] || 0),
        backgroundColor: `rgba(${index * 50}, ${255 - index * 50}, ${index * 100}, 0.8)`
    }));

    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: anos,
            datasets: datasets
        },
        options: {
            responsive: true,
            scales: {
                x: { stacked: true },
                y: { stacked: true }
            },
            plugins: {
                title: {
                    display: true,
                    text: title
                }
            }
        }
    });
}

function updateCompetitiveAnalysis() {
    const analysisDiv = document.getElementById('competitiveAnalysis');
    let latestYear = anos[anos.length - 1];
    let latestHHI = hhiData[latestYear];
    
    let analysis = `<p>No ano de ${latestYear}, o Índice Herfindahl-Hirschman (HHI) do mercado é ${latestHHI.toFixed(2)}.</p>`;
    
    if (latestHHI < 1500) {
        analysis += '<p>O mercado é considerado não concentrado, indicando um alto nível de competição.</p>';
    } else if (latestHHI < 2500) {
        analysis += '<p>O mercado é considerado moderadamente concentrado, indicando um nível médio de competição.</p>';
    } else {
        analysis += '<p>O mercado é considerado altamente concentrado, indicando um baixo nível de competição.</p>';
    }

    // Adicionar análise de tendências
    let hhiTrend = (hhiData[latestYear] - hhiData[anos[0]]) / anos.length;
    if (hhiTrend > 0) {
        analysis += `<p>A concentração do mercado tem aumentado em média ${hhiTrend.toFixed(2)} pontos por ano.</p>`;
    } else if (hhiTrend < 0) {
        analysis += `<p>A concentração do mercado tem diminuído em média ${Math.abs(hhiTrend).toFixed(2)} pontos por ano.</p>`;
    } else {
        analysis += '<p>A concentração do mercado tem se mantido relativamente estável ao longo dos anos.</p>';
    }
    
    analysisDiv.innerHTML = analysis;
}

function formatNumber(number, decimals = 0) {
    return new Intl.NumberFormat('pt-BR', { 
        minimumFractionDigits: decimals,
        maximumFractionDigits: decimals 
    }).format(number);
}


console.log('Anos:', anos);
console.log('Operadoras:', operadoras);
console.log('Dados de participação de mercado:', marketShareData);
console.log('Dados de HHI:', hhiData);
console.log('Dados de volume de negócio:', volumeNegocioData);
console.log('Dados de investimentos:', investimentosData);
console.log('Dados de tráfego de dados:', trafegoDadosData);
console.log('Dados de emprego:', empregoData);