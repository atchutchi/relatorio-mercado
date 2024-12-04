let marketEvolutionChart = null;
let operatorContributionChart = null;

document.addEventListener('DOMContentLoaded', initializeSectorPanorama);

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

   let overviewHtml = `
       <div class="overview-grid">
           <div class="indicator-card" style="border-left: 4px solid ${operadoraColors.MTN.main}">
               <h4>Assinantes</h4>
               <span class="value">${formatNumber(latestData.assinantes_rede_movel.total)}</span>
           </div>
           <div class="indicator-card" style="border-left: 4px solid ${operadoraColors.ORANGE.main}">
               <h4>Receita</h4>
               <span class="value">${formatNumber(latestData.receita_total.total)} FCFA</span>
           </div>
           <div class="indicator-card" style="border-left: 4px solid ${operadoraColors.MTN.main}">
               <h4>Tráfego de Dados</h4>
               <span class="value">${formatNumber(latestData.trafego_dados.total)} MB</span>
           </div>
           <div class="indicator-card" style="border-left: 4px solid ${operadoraColors.ORANGE.main}">
               <h4>Investimentos</h4>
               <span class="value">${formatNumber(latestData.investimentos.total)} FCFA</span>
           </div>
       </div>
   `;
   
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

   const datasets = operadoras.map(operadora => ({
       label: operadora,
       data: anos.map(ano => panoramaData[ano][selectedIndicator].operadoras[operadora]),
       borderColor: operadoraColors[operadora].main,
       backgroundColor: operadoraColors[operadora].background,
       borderWidth: 2,
       tension: 0.1,
       fill: true
   }));

   if (marketEvolutionChart) {
       marketEvolutionChart.destroy();
   }

   marketEvolutionChart = new Chart(ctx, {
       type: 'line',
       data: { labels: anos, datasets },
       options: {
           responsive: true,
           plugins: {
               title: {
                   display: true,
                   text: `Evolução - ${formatIndicatorName(selectedIndicator)}`,
                   font: { family: 'Poppins', size: 16 }
               },
               legend: {
                   labels: { font: { family: 'Poppins' } }
               },
               tooltip: {
                   backgroundColor: 'rgba(0, 0, 0, 0.8)',
                   titleFont: { family: 'Poppins', size: 14 },
                   bodyFont: { family: 'Poppins', size: 13 }
               }
           },
           scales: {
               y: {
                   beginAtZero: true,
                   grid: { color: 'rgba(0, 0, 0, 0.1)' }
               }
           }
       }
   });
}

function renderOperatorContributionChart() {
   const selectedYear = document.getElementById('yearSelect').value;
   const ctx = document.getElementById('operatorContributionChart').getContext('2d');

   const datasets = indicators.map(indicator => ({
       label: formatIndicatorName(indicator),
       data: operadoras.map(op => panoramaData[selectedYear][indicator].operadoras[op]),
       backgroundColor: operadoras.map(op => operadoraColors[op].background),
       borderColor: operadoras.map(op => operadoraColors[op].main),
       borderWidth: 2
   }));

   if (operatorContributionChart) {
       operatorContributionChart.destroy();
   }

   operatorContributionChart = new Chart(ctx, {
       type: 'bar',
       data: { labels: operadoras, datasets },
       options: {
           responsive: true,
           scales: {
               y: { stacked: true },
               x: { stacked: true }
           },
           plugins: {
               title: {
                   display: true,
                   text: `Contribuição por Operadora - ${selectedYear}`,
                   font: { family: 'Poppins', size: 16 }
               },
               legend: {
                   labels: { font: { family: 'Poppins' } }
               },
               tooltip: {
                   backgroundColor: 'rgba(0, 0, 0, 0.8)',
                   titleFont: { family: 'Poppins', size: 14 },
                   bodyFont: { family: 'Poppins', size: 13 }
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