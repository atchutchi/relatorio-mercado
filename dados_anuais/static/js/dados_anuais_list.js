document.addEventListener('DOMContentLoaded', function() {
    // Function to create a chart
    function createChart(elementId, label, data, type = 'line', color = 'rgb(75, 192, 192)') {
        const ctx = document.getElementById(elementId).getContext('2d');
        new Chart(ctx, {
            type: type,
            data: {
                labels: dadosGraficos.anos,
                datasets: [{
                    label: label,
                    data: data,
                    borderColor: color,
                    backgroundColor: type === 'bar' ? color : undefined,
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

    // Create charts for key indicators
    createChart('assinantesChart', 'Assinantes Rede Móvel', dadosGraficos.assinantes_rede_movel);
    createChart('volumeNegocioChart', 'Volume de Negócio (FCFA)', dadosGraficos.volume_negocio, 'bar', 'rgba(255, 99, 132, 0.8)');

    // Additional charts
    const additionalCharts = [
        { id: 'assinantesBandaLargaChart', label: 'Assinantes Banda Larga Móvel', data: dadosGraficos.assinantes_banda_larga_movel },
        { id: 'investimentosChart', label: 'Investimentos (FCFA)', data: dadosGraficos.investimentos, type: 'bar', color: 'rgba(54, 162, 235, 0.8)' },
        { id: 'trafegoVozChart', label: 'Tráfego de Voz (minutos)', data: dadosGraficos.trafego_voz_originado },
        { id: 'trafegoSMSChart', label: 'Tráfego de SMS', data: dadosGraficos.trafego_sms }
    ];

    // Create additional chart elements and render charts
    const chartsContainer = document.createElement('div');
    chartsContainer.className = 'row mt-4';
    additionalCharts.forEach(chart => {
        const col = document.createElement('div');
        col.className = 'col-md-6 mb-4';
        col.innerHTML = `
            <div class="card">
                <div class="card-body">
                    <h2 class="card-title">${chart.label}</h2>
                    <canvas id="${chart.id}"></canvas>
                </div>
            </div>
        `;
        chartsContainer.appendChild(col);
    });
    document.querySelector('.content-wrapper .container').appendChild(chartsContainer);

    // Render additional charts
    additionalCharts.forEach(chart => {
        createChart(chart.id, chart.label, chart.data, chart.type, chart.color);
    });

    // Function to format large numbers
    function formatNumber(num) {
        if (num >= 1000000000) {
            return (num / 1000000000).toFixed(1) + 'B';
        }
        if (num >= 1000000) {
            return (num / 1000000).toFixed(1) + 'M';
        }
        if (num >= 1000) {
            return (num / 1000).toFixed(1) + 'K';
        }
        return num;
    }

    // Create summary cards for the latest year
    const latestYear = dadosGraficos.anos[dadosGraficos.anos.length - 1];
    const summaryContainer = document.createElement('div');
    summaryContainer.className = 'row mt-4';
    const summaryData = [
        { label: 'Assinantes Rede Móvel', value: dadosGraficos.assinantes_rede_movel.slice(-1)[0] },
        { label: 'Volume de Negócio', value: dadosGraficos.volume_negocio.slice(-1)[0], isCurrency: true },
        { label: 'Assinantes Banda Larga', value: dadosGraficos.assinantes_banda_larga_movel.slice(-1)[0] },
        { label: 'Investimentos', value: dadosGraficos.investimentos.slice(-1)[0], isCurrency: true }
    ];

    summaryData.forEach(item => {
        const col = document.createElement('div');
        col.className = 'col-md-3 mb-4';
        col.innerHTML = `
            <div class="card">
                <div class="card-body">
                    <h5 class="card-title">${item.label}</h5>
                    <p class="card-text h4">
                        ${item.isCurrency ? 'FCFA ' : ''}${formatNumber(item.value)}
                    </p>
                    <p class="card-text text-muted">Ano: ${latestYear}</p>
                </div>
            </div>
        `;
        summaryContainer.appendChild(col);
    });

    document.querySelector('.content-wrapper .container').insertBefore(summaryContainer, document.querySelector('.content-wrapper .container').firstChild);
});