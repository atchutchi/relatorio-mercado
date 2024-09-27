document.addEventListener('DOMContentLoaded', function() {
    if (marketData && marketData.length > 0) {
        renderChart();
        renderMarketSummary();
        renderDataTable();
    } else {
        document.querySelector('.container').innerHTML += '<p class="alert alert-warning">Nenhum dado disponível para exibição.</p>';
    }
});

function renderChart() {
    if (!anos || !assinantesTotal || !receitaTotal || !trafegoDadosTotal || !investimentosTotal) {
        return;
    }
    var ctx = document.getElementById('mainIndicatorsChart').getContext('2d');
    new Chart(ctx, {
        type: 'line',
        data: {
            labels: anos,
            datasets: [{
                label: 'Assinantes',
                data: assinantesTotal,
                borderColor: 'rgb(75, 192, 192)',
                tension: 0.1
            }, {
                label: 'Receita (Bilhões FCFA)',
                data: receitaTotal.map(value => Number(value) / 1000000000),
                borderColor: 'rgb(255, 99, 132)',
                tension: 0.1
            }, {
                label: 'Tráfego de Dados (TB)',
                data: trafegoDadosTotal.map(value => value / 1000000),
                borderColor: 'rgb(54, 162, 235)',
                tension: 0.1
            }, {
                label: 'Investimentos (Bilhões FCFA)',
                data: investimentosTotal.map(value => Number(value) / 1000000000),
                borderColor: 'rgb(255, 206, 86)',
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

function renderMarketSummary() {
    if (!marketData || marketData.length === 0) {
        return;
    }
    const lastYear = marketData[marketData.length - 1];
    const penultimateYear = marketData.length > 1 ? marketData[marketData.length - 2] : null;
    
    let summaryHtml = `
        <p>
            Em ${lastYear.ano}, o mercado de telecomunicações atingiu ${formatNumber(lastYear.assinantes_total)} assinantes,
            com uma receita total de ${formatNumber(lastYear.receita_total)} FCFA.
            O tráfego de dados totalizou ${formatNumber(lastYear.trafego_dados_total)} MB,
            enquanto os investimentos no setor chegaram a ${formatNumber(lastYear.investimentos_total)} FCFA.
        </p>
    `;

    if (penultimateYear) {
        const assinantesCrescimento = ((lastYear.assinantes_total - penultimateYear.assinantes_total) / penultimateYear.assinantes_total) * 100;
        const receitaCrescimento = ((lastYear.receita_total - penultimateYear.receita_total) / penultimateYear.receita_total) * 100;
        const trafegoCrescimento = ((lastYear.trafego_dados_total - penultimateYear.trafego_dados_total) / penultimateYear.trafego_dados_total) * 100;
        const investimentosCrescimento = ((lastYear.investimentos_total - penultimateYear.investimentos_total) / penultimateYear.investimentos_total) * 100;

        summaryHtml += `
            <p>
                Comparado ao ano anterior, observamos um crescimento de 
                ${formatNumber(assinantesCrescimento, 2)}% em assinantes,
                ${formatNumber(receitaCrescimento, 2)}% em receita,
                ${formatNumber(trafegoCrescimento, 2)}% em tráfego de dados e
                ${formatNumber(investimentosCrescimento, 2)}% em investimentos.
            </p>
        `;
    }
    
    document.getElementById('marketSummary').innerHTML = summaryHtml;
}

function renderDataTable() {
    const tableBody = document.querySelector('#annualDataTable tbody');
    let tableHtml = '';
    
    marketData.slice().reverse().forEach(data => {
        tableHtml += `
            <tr>
                <td>${data.ano}</td>
                <td>${formatNumber(data.assinantes_total)}</td>
                <td>${formatNumber(data.receita_total)}</td>
                <td>${formatNumber(data.trafego_dados_total)}</td>
                <td>${formatNumber(data.investimentos_total)}</td>
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