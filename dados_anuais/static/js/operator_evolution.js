document.addEventListener('DOMContentLoaded', function() {
    renderCharts();
    // A tabela de crescimento agora é renderizada no template
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
 
 function renderCharts() {
    // Usa a variável operadora definida no template
    const currentOperadora = operadora;
    const color = operadoraColors[currentOperadora] || operadoraColors.MTN; // Fallback para MTN
 
    renderAssinantesChart(color);
    renderReceitaInvestimentosChart(color);
    renderTrafegoChart(color);
    renderChamadasChart(color);
 }
 
 function renderAssinantesChart(color) {
    const ctx = document.getElementById('assinantesChart').getContext('2d');
    new Chart(ctx, {
        type: 'line',
        data: {
            labels: anos,
            datasets: [
                {
                    label: 'Rede Móvel',
                    data: evolutionData.assinantes_rede_movel,
                    borderColor: color.main,
                    backgroundColor: color.background,
                    tension: 0.1,
                    fill: true
                },
                {
                    label: 'Pós-pago',
                    data: evolutionData.assinantes_pos_pago,
                    borderColor: 'rgba(75, 192, 192)',
                    backgroundColor: 'rgba(75, 192, 192, 0.2)',
                    tension: 0.1,
                    fill: true
                },
                {
                    label: 'Pré-pago',
                    data: evolutionData.assinantes_pre_pago,
                    borderColor: 'rgba(54, 162, 235)',
                    backgroundColor: 'rgba(54, 162, 235, 0.2)',
                    tension: 0.1,
                    fill: true
                }
            ]
        },
        options: getChartOptions('Evolução de Assinantes')
    });
 }
 
 function renderReceitaInvestimentosChart(color) {
    const ctx = document.getElementById('receitaInvestimentosChart').getContext('2d');
    new Chart(ctx, {
        type: 'line',
        data: {
            labels: anos,
            datasets: [
                {
                    label: 'Receita Total',
                    data: evolutionData.receita_total,
                    borderColor: color.main,
                    backgroundColor: color.background,
                    tension: 0.1,
                    fill: true
                },
                {
                    label: 'Investimentos',
                    data: evolutionData.investimentos,
                    borderColor: 'rgba(75, 192, 192)',
                    backgroundColor: 'rgba(75, 192, 192, 0.2)',
                    tension: 0.1,
                    fill: true
                }
            ]
        },
        options: getChartOptions('Receita e Investimentos')
    });
 }
 
 function renderTrafegoChart(color) {
    const ctx = document.getElementById('trafegoChart').getContext('2d');
    new Chart(ctx, {
        type: 'line',
        data: {
            labels: anos,
            datasets: [
                {
                    label: 'Voz',
                    data: evolutionData.trafego_voz_originado,
                    borderColor: color.main,
                    backgroundColor: color.background,
                    tension: 0.1,
                    fill: true
                },
                {
                    label: 'SMS',
                    data: evolutionData.trafego_sms,
                    borderColor: 'rgba(75, 192, 192)',
                    backgroundColor: 'rgba(75, 192, 192, 0.2)',
                    tension: 0.1,
                    fill: true
                },
                {
                    label: 'Dados',
                    data: evolutionData.trafego_dados,
                    borderColor: 'rgba(54, 162, 235)',
                    backgroundColor: 'rgba(54, 162, 235, 0.2)',
                    tension: 0.1,
                    fill: true
                }
            ]
        },
        options: getChartOptions('Evolução de Tráfego')
    });
 }
 
 function renderChamadasChart(color) {
    const ctx = document.getElementById('chamadasChart').getContext('2d');
    new Chart(ctx, {
        type: 'line',
        data: {
            labels: anos,
            datasets: [
                {
                    label: 'Originadas',
                    data: evolutionData.chamadas_originadas,
                    borderColor: color.main,
                    backgroundColor: color.background,
                    tension: 0.1,
                    fill: true
                },
                {
                    label: 'Terminadas',
                    data: evolutionData.chamadas_terminadas,
                    borderColor: 'rgba(75, 192, 192)',
                    backgroundColor: 'rgba(75, 192, 192, 0.2)',
                    tension: 0.1,
                    fill: true
                }
            ]
        },
        options: getChartOptions('Evolução de Chamadas')
    });
 }
 
 function getChartOptions(title) {
    return {
        responsive: true,
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
                },
                callbacks: {
                    label: function(context) {
                        let label = context.dataset.label || '';
                        let value = context.parsed.y;
                        if (label) {
                            label += ': ';
                        }
                        
                        if (label.includes('Receita') || label.includes('Investimentos')) {
                            return label + formatCurrency(value);
                        } else {
                            return label + formatNumber(value);
                        }
                    }
                }
            }
        },
        scales: {
            y: {
                beginAtZero: true,
                grid: {
                    color: 'rgba(0, 0, 0, 0.1)'
                }
            },
            x: {
                grid: {
                    color: 'rgba(0, 0, 0, 0.1)'
                }
            }
        }
    };
 }

 // Funções auxiliares para formatação
 function formatNumber(number, decimals = 0) {
    return new Intl.NumberFormat('pt-BR', { 
        minimumFractionDigits: decimals,
        maximumFractionDigits: decimals 
    }).format(number);
 }
 
 function formatCurrency(value) {
    return new Intl.NumberFormat('pt-BR', { 
        minimumFractionDigits: 2,
        maximumFractionDigits: 2 
    }).format(value) + ' FCFA';
 }