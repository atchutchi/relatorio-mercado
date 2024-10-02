let marketEvolutionChart = null;
let operatorContributionChart = null;

document.addEventListener('DOMContentLoaded', function() {
    initializeSectorPanorama();
});

function initializeSectorPanorama() {
    renderMarketOverview();
    populateIndicatorSelect();
    populateYearSelect();
    renderMarketEvolutionChart();
    renderOperatorContributionChart();

    document.getElementById('indicatorSelect').addEventListener('change', renderMarketEvolutionChart);
    document.getElementById('yearSelect').addEventListener('change', renderOperatorContributionChart);
}

function renderMarketOverview() {
    const overviewDiv = document.getElementById('marketOverview');
    const latestYear = anos[anos.length - 1];
    const latestData = panoramaData[latestYear];

    let overviewHtml = `<h3>Visão Geral do Mercado em ${latestYear}</h3>`;

    const keyIndicators = ['assinantes_rede_movel', 'receita_total', 'trafego_dados', 'investimentos'];

    keyIndicators.forEach(indicator => {
        const totalValue = latestData[indicator].total;
        overviewHtml += `
            <div class="indicator-highlight">
                <span class="indicator-title">${formatIndicatorName(indicator)}:</span>
                <span class="indicator-value">${formatNumber(totalValue)}</span>
            </div>
        `;
    });

    overviewDiv.innerHTML = overviewHtml;
}

function populateIndicatorSelect() {
    const indicatorSelect = document.getElementById('indicatorSelect');
    indicators.forEach(indicator => {
        const option = document.createElement('option');
        option.value = indicator;
        option.textContent = formatIndicatorName(indicator);
        indicatorSelect.appendChild(option);
    });
}

function populateYearSelect() {
    const yearSelect = document.getElementById('yearSelect');
    anos.forEach(ano => {
        const option = document.createElement('option');
        option.value = ano;
        option.textContent = ano;
        yearSelect.appendChild(option);
    });
    yearSelect.value = anos[anos.length - 1];
}

function renderMarketEvolutionChart() {
    const selectedIndicator = document.getElementById('indicatorSelect').value;
    const ctx = document.getElementById('marketEvolutionChart').getContext('2d');

    const datasets = operadoras.map((operadora, index) => ({
        label: operadora,
        data: anos.map(ano => panoramaData[ano][selectedIndicator].operadoras[operadora]),
        backgroundColor: getColor(index, 0.6),
        borderColor: getColor(index),
        borderWidth: 1
    }));

    if (marketEvolutionChart) {
        marketEvolutionChart.destroy();
    }

    marketEvolutionChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: anos,
            datasets: datasets
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: true,
                    stacked: true
                }
            }
        }
    });
}

function renderOperatorContributionChart() {
    const selectedYear = document.getElementById('yearSelect').value;
    const ctx = document.getElementById('operatorContributionChart').getContext('2d');

    const datasets = indicators.map((indicator, index) => ({
        label: formatIndicatorName(indicator),
        data: operadoras.map(operadora => panoramaData[selectedYear][indicator].operadoras[operadora]),
        backgroundColor: getColor(index, 0.6),
        borderColor: getColor(index),
        borderWidth: 1
    }));

    if (operatorContributionChart) {
        operatorContributionChart.destroy();
    }

    operatorContributionChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: operadoras,
            datasets: datasets
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: true,
                    stacked: true
                },
                x: {
                    stacked: true
                }
            }
        }
    });
}

function formatIndicatorName(name) {
    return name.split('_').map(word => word.charAt(0).toUpperCase() + word.slice(1)).join(' ');
}

function formatNumber(number) {
    return new Intl.NumberFormat('pt-BR').format(number);
}

function getColor(index, alpha = 1) {
    const colors = [
        `rgba(75, 192, 192, ${alpha})`,
        `rgba(255, 99, 132, ${alpha})`,
        `rgba(54, 162, 235, ${alpha})`,
        `rgba(255, 206, 86, ${alpha})`,
        `rgba(153, 102, 255, ${alpha})`,
        `rgba(255, 159, 64, ${alpha})`
    ];
    return colors[index % colors.length];
}