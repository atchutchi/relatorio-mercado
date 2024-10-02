let growthChart = null;

document.addEventListener('DOMContentLoaded', function() {
    initializeGrowthReport();
});

function initializeGrowthReport() {
    populateOperadoraSelect();
    populateIndicatorSelect();
    updateGrowthReport();
    
    document.getElementById('operadoraSelect').addEventListener('change', updateGrowthReport);
    document.getElementById('indicatorSelect').addEventListener('change', updateGrowthReport);
}

function populateOperadoraSelect() {
    const operadoraSelect = document.getElementById('operadoraSelect');
    operadoras.forEach(operadora => {
        const option = document.createElement('option');
        option.value = operadora;
        option.textContent = operadora;
        operadoraSelect.appendChild(option);
    });
}

function populateIndicatorSelect() {
    const indicatorSelect = document.getElementById('indicatorSelect');
    const indicators = Object.keys(growthData[operadoras[0]][anos[1]]);
    
    indicators.forEach(indicator => {
        const option = document.createElement('option');
        option.value = indicator;
        option.textContent = formatIndicatorName(indicator);
        indicatorSelect.appendChild(option);
    });
}

function updateGrowthReport() {
    const selectedOperadora = document.getElementById('operadoraSelect').value;
    const selectedIndicator = document.getElementById('indicatorSelect').value;
    
    const data = anos.slice(1).map(ano => growthData[selectedOperadora][ano][selectedIndicator]);
    
    renderGrowthChart(data, selectedIndicator);
    renderGrowthTable(data);
    renderGrowthHighlights(data);
}

function renderGrowthChart(data, indicator) {
    const ctx = document.getElementById('growthChart').getContext('2d');
    
    if (growthChart) {
        growthChart.destroy();
    }
    
    growthChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: anos.slice(1),
            datasets: [{
                label: `Taxa de Crescimento - ${formatIndicatorName(indicator)}`,
                data: data,
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
                        text: 'Taxa de Crescimento (%)'
                    }
                }
            }
        }
    });
}

function renderGrowthTable(data) {
    const tableBody = document.querySelector('#growthTable tbody');
    let tableHtml = '';
    
    anos.slice(1).forEach((ano, index) => {
        const growthRate = data[index];
        tableHtml += `
            <tr>
                <td>${ano}</td>
                <td class="${growthRate >= 0 ? 'positive-growth' : 'negative-growth'}">${formatNumber(growthRate, 2)}%</td>
            </tr>
        `;
    });
    
    tableBody.innerHTML = tableHtml;
}

function renderGrowthHighlights(data) {
    const highlightsDiv = document.getElementById('growthHighlights');
    const maxGrowth = Math.max(...data);
    const minGrowth = Math.min(...data);
    const averageGrowth = data.reduce((a, b) => a + b, 0) / data.length;
    
    let highlightsHtml = `
        <p>Maior crescimento: <span class="positive-growth">${formatNumber(maxGrowth, 2)}%</span> (${anos[data.indexOf(maxGrowth) + 1]})</p>
        <p>Maior declínio: <span class="negative-growth">${formatNumber(minGrowth, 2)}%</span> (${anos[data.indexOf(minGrowth) + 1]})</p>
        <p>Crescimento médio: <span class="${averageGrowth >= 0 ? 'positive-growth' : 'negative-growth'}">${formatNumber(averageGrowth, 2)}%</span></p>
    `;
    
    highlightsDiv.innerHTML = highlightsHtml;
}

function formatNumber(number, decimals = 0) {
    return new Intl.NumberFormat('pt-BR', { 
        minimumFractionDigits: decimals,
        maximumFractionDigits: decimals 
    }).format(number);
}

function formatIndicatorName(name) {
    return name.split('_').map(word => word.charAt(0).toUpperCase() + word.slice(1)).join(' ');
}