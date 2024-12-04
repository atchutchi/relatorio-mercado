let comparisonChart = null;

document.addEventListener('DOMContentLoaded', function() {
   initializeComparison();
});

function initializeComparison() {
   populateYearSelect();
   populateIndicatorSelect();
   updateChart();
   
   document.getElementById('yearSelect').addEventListener('change', updateChart);
   document.getElementById('indicatorSelect').addEventListener('change', updateChart);
}

function populateYearSelect() {
   const yearSelect = document.getElementById('yearSelect');
   anos.forEach(ano => {
       const option = document.createElement('option');
       option.value = ano;
       option.textContent = ano;
       yearSelect.appendChild(option);
   });
}

function populateIndicatorSelect() {
   const indicatorSelect = document.getElementById('indicatorSelect');
   const firstYearData = comparisonData[anos[0]][operadoras[0]];
   
   for (const [key, value] of Object.entries(firstYearData)) {
       const option = document.createElement('option');
       option.value = key;
       option.textContent = formatIndicatorName(key);
       indicatorSelect.appendChild(option);
   }
}

function updateChart() {
   const selectedYear = document.getElementById('yearSelect').value;
   const selectedIndicator = document.getElementById('indicatorSelect').value;
   
   if (!comparisonData[selectedYear]) {
       console.error(`Dados não disponíveis para o ano ${selectedYear}`);
       return;
   }
   
   const data = comparisonData[selectedYear];
   const chartData = operadoras.map(operadora => data[operadora][selectedIndicator]);
   
   renderChart(chartData, selectedIndicator);
   renderTable(data, selectedIndicator);
   renderAnalysis(data, selectedIndicator);
}

function renderChart(data, indicator) {
   const ctx = document.getElementById('comparisonChart').getContext('2d');
   
   if (comparisonChart) {
       comparisonChart.destroy();
   }
   
   comparisonChart = new Chart(ctx, {
       type: 'bar',
       data: {
           labels: operadoras,
           datasets: [{
               label: formatIndicatorName(indicator),
               data: data,
               backgroundColor: ['rgba(255, 206, 86, 0.6)', 'rgba(255, 159, 64, 0.6)'],
               borderColor: ['rgb(255, 206, 86)', 'rgb(255, 159, 64)'],
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

function renderAnalysis(data, indicator) {
   const analysisDiv = document.getElementById('analysisText');
   const indicatorName = formatIndicatorName(indicator);
   const year = document.getElementById('yearSelect').value;
   
   let analysisText = `<h3>Análise Comparativa - ${indicatorName} (${year})</h3>`;
   
   const [op1, op2] = operadoras;
   const valor1 = data[op1][indicator];
   const valor2 = data[op2][indicator];
   
   if (valor1 > valor2) {
       analysisText += `<p>${op1} se destacou em ${indicatorName.toLowerCase()} com ${formatNumber(valor1)}, superando ${op2} que registrou ${formatNumber(valor2)}.</p>`;
   } else if (valor2 > valor1) {
       analysisText += `<p>${op2} liderou em ${indicatorName.toLowerCase()} com ${formatNumber(valor2)}, à frente de ${op1} que obteve ${formatNumber(valor1)}.</p>`;
   } else {
       analysisText += `<p>${op1} e ${op2} apresentaram resultados idênticos em ${indicatorName.toLowerCase()} com ${formatNumber(valor1)}.</p>`;
   }
   
   const diferenca = Math.abs(valor1 - valor2);
   const percentualDiferenca = (diferenca / Math.min(valor1, valor2)) * 100;
   
   analysisText += `<p>A diferença entre as operadoras foi de ${formatNumber(diferenca)}, representando uma variação de ${formatNumber(percentualDiferenca, 2)}%.</p>`;
   
   analysisDiv.innerHTML = analysisText;
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