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
    
    if (window.marketShareChart instanceof Chart) {
        window.marketShareChart.destroy();
    }
 
    if (!marketShareData[selectedYear]) {
        console.error(`Não há dados de participação de mercado para o ano ${selectedYear}`);
        return;
    }
 
    const backgroundColors = operadoras.map(op => operadoraColors[op].background);
    const borderColors = operadoras.map(op => operadoraColors[op].main);
 
    window.marketShareChart = new Chart(ctx, {
        type: 'pie',
        data: {
            labels: operadoras,
            datasets: [{
                data: operadoras.map(op => marketShareData[selectedYear][op] || 0),
                backgroundColor: backgroundColors,
                borderColor: borderColors,
                borderWidth: 2
            }]
        },
        options: {
            responsive: true,
            plugins: {
                title: {
                    display: true,
                    text: `Participação de Mercado em ${selectedYear}`,
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
                }
            }
        }
    });
 }
 
 function renderHHIChart() {
    const ctx = document.getElementById('hhiChart').getContext('2d');
    new Chart(ctx, {
        type: 'line',
        data: {
            labels: anos,
            datasets: [{
                label: 'HHI',
                data: anos.map(ano => hhiData[ano]),
                borderColor: 'rgb(75, 192, 192)',
                tension: 0.1,
                fill: false
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
    const datasets = operadoras.map(op => ({
        label: op,
        data: anos.map(ano => data[ano][op] || 0),
        backgroundColor: operadoraColors[op].background,
        borderColor: operadoraColors[op].main,
        borderWidth: 1
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
                }
            }
        }
    });
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