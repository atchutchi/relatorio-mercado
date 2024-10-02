document.addEventListener('DOMContentLoaded', function() {
    populateYearSelect();
    renderMarketShareChart(anos[anos.length - 1]);
    renderHHIChart();
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
    if (window.marketShareChart) {
        window.marketShareChart.destroy();
    }
    window.marketShareChart = new Chart(ctx, {
        type: 'pie',
        data: {
            labels: operadoras,
            datasets: [{
                data: operadoras.map(op => marketShareData[selectedYear][op]),
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
    const ctx = document.getElementById('hhiChart').getContext('2d');
    new Chart(ctx, {
        type: 'line',
        data: {
            labels: anos,
            datasets: [{
                label: 'HHI',
                data: anos.map(ano => hhiData[ano]),
                borderColor: 'rgb(75, 192, 192)',
                tension: 0.1
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: 'HHI'
                    }
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
    
    analysisDiv.innerHTML = analysis;
}

function formatNumber(number, decimals = 0) {
    return new Intl.NumberFormat('pt-BR', { 
        minimumFractionDigits: decimals,
        maximumFractionDigits: decimals 
    }).format(number);
}