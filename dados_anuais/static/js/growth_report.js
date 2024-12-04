let growthChart = null;

document.addEventListener('DOMContentLoaded', function() {
   initializeGrowthReport();
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
   
   renderGrowthChart(data, selectedIndicator, selectedOperadora);
   renderGrowthTable(data, selectedOperadora);
   renderGrowthHighlights(data, selectedOperadora);
}

function renderGrowthChart(data, indicator, operadora) {
   const ctx = document.getElementById('growthChart').getContext('2d');
   
   if (growthChart) {
       growthChart.destroy();
   }
   
   const operadoraColor = operadoraColors[operadora];
   
   growthChart = new Chart(ctx, {
       type: 'line',
       data: {
           labels: anos.slice(1),
           datasets: [{
               label: `Taxa de Crescimento - ${formatIndicatorName(indicator)}`,
               data: data,
               borderColor: operadoraColor.main,
               backgroundColor: operadoraColor.background,
               tension: 0.1,
               fill: true
           }]
       },
       options: {
           responsive: true,
           scales: {
               y: {
                   beginAtZero: true,
                   title: {
                       display: true,
                       text: 'Taxa de Crescimento (%)',
                       font: {
                           family: 'Poppins'
                       }
                   }
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

function renderGrowthTable(data, operadora) {
   const tableBody = document.querySelector('#growthTable tbody');
   let tableHtml = '';
   
   anos.slice(1).forEach((ano, index) => {
       const growthRate = data[index];
       const color = growthRate >= 0 ? operadoraColors[operadora].main : '#dc3545';
       
       tableHtml += `
           <tr>
               <td>${ano}</td>
               <td style="color: ${color}; font-weight: 500;">${formatNumber(growthRate, 2)}%</td>
           </tr>
       `;
   });
   
   tableBody.innerHTML = tableHtml;
}

function renderGrowthHighlights(data, operadora) {
   const highlightsDiv = document.getElementById('growthHighlights');
   const maxGrowth = Math.max(...data);
   const minGrowth = Math.min(...data);
   const averageGrowth = data.reduce((a, b) => a + b, 0) / data.length;
   
   let highlightsHtml = `
       <p>Maior crescimento: <span style="color: ${operadoraColors[operadora].main}; font-weight: 500;">
           ${formatNumber(maxGrowth, 2)}%</span> (${anos[data.indexOf(maxGrowth) + 1]})</p>
       <p>Maior declínio: <span style="color: #dc3545; font-weight: 500;">
           ${formatNumber(minGrowth, 2)}%</span> (${anos[data.indexOf(minGrowth) + 1]})</p>
       <p>Crescimento médio: <span style="color: ${averageGrowth >= 0 ? operadoraColors[operadora].main : '#dc3545'}; font-weight: 500;">
           ${formatNumber(averageGrowth, 2)}%</span></p>
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