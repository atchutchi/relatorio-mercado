document.addEventListener('DOMContentLoaded', function() {
    populateYearSelect();
    updateChart();
    
    document.getElementById('yearSelect').addEventListener('change', updateChart);
    document.getElementById('indicatorSelect').addEventListener('change', updateChart);
});

function populateYearSelect() {
    const yearSelect = document.getElementById('yearSelect');
    anos.forEach(ano => {
        const option = document.createElement('option');
        option.value = ano;
        option.textContent = ano;
        yearSelect.appendChild(option);
    });
}

function updateChart() {
    const selectedYear = document.getElementById('yearSelect').value;
    const selectedIndicator = document.getElementById('indicatorSelect').value;
    
    const data = comparisonData[selectedYear];
    const chartData = operadoras.map(operadora => data[operadora][selectedIndicator]);
    
    renderChart(chartData);
    renderTable(data, selectedIndicator);
}

function renderChart(data) {
    const ctx = document.getElementById('comparisonChart').getContext('2d');
    if (window.comparisonChart) {
        window.comparisonChart.destroy();
    }
    window.comparisonChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: operadoras,
            datasets: [{
                label: document.getElementById('indicatorSelect').selectedOptions[0].text,
                data: data,
                backgroundColor: ['rgba(75, 192, 192, 0.6)', 'rgba(255, 99, 132, 0.6)', 'rgba(54, 162, 235, 0.6)'],
                borderColor: ['rgb(75, 192, 192)', 'rgb(255, 99, 132)', 'rgb(54, 162, 235)'],
                borderWidth: 1
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

function renderTable(data, indicator) {
    const tableBody = document.querySelector('#comparisonTable tbody');
    let tableHtml = '';
    
    const total = Object.values(data).reduce((sum, op) => sum + op[indicator], 0);
    
    Object.entries(data).forEach(([operadora, valores]) => {
        const valor = valores[indicator];
        const percentagem = (valor / total) * 100;
        tableHtml += `
            <tr>
                <td>${operadora}</td>
                <td>${formatNumber(valor)}</td>
                <td>${formatNumber(percentagem, 2)}%</td>
            </tr>
        `;
    });
    
    tableBody.innerHTML = tableHtml;
}

function formatNumber(number, decimals = 0) {
    return new Intl.NumberFormat('fr-FR', { 
        minimumFractionDigits: decimals,
        maximumFractionDigits: decimals 
    }).format(number);
}