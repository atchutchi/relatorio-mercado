// Configuração inicial e constantes
document.addEventListener('DOMContentLoaded', function() {
    console.log('Dados recebidos:', window.appData);
    if(window.appData) {
        renderAllCharts();
        setupEventListeners();
    }

    function mudarAno(ano) {
        // Construir a URL com o novo ano
        const url = new URL(window.location.href);
        url.searchParams.set('ano', ano);
        
        // Mostrar indicador de carregamento
        document.body.style.cursor = 'wait';
        
        // Redirecionar para a nova URL
        window.location.href = url.toString();
    }
    
    // Adicionar listener para o select de ano
    document.addEventListener('DOMContentLoaded', function() {
        const anoSelect = document.getElementById('anoSelect');
        if (anoSelect) {
            anoSelect.addEventListener('change', function(e) {
                mudarAno(e.target.value);
            });
        }
    });

    // Configuração de estilo padrão
    Chart.defaults.font.family = 'Poppins';
    Chart.defaults.color = '#444';
    Chart.defaults.responsive = true;

    // Variáveis globais
    const chartColors = {
        MTN: {
            main: '#fecb00',           
            secondary: '#004f9f',      
            background: 'rgba(254, 203, 0, 0.2)'
        },
        ORANGE: {
            main: '#ff6f00',           
            secondary: '#000000',      
            background: 'rgba(255, 111, 0, 0.2)'
        },
        outros: {
            main: '#75c7c3',          
            background: 'rgba(117, 199, 195, 0.2)'
        }
    };

    // Configuração inicial
    document.addEventListener('DOMContentLoaded', function() {
        // Debug dos dados recebidos
        console.log('Dados completos:', window.appData);
        console.log('Resumo Executivo:', window.appData?.resumo_executivo);
        console.log('Análise Setorial:', window.appData?.analise_setorial);
        
        if(window.appData) {
            renderAllCharts();
            setupEventListeners();
        } else {
            console.warn('Dados não disponíveis para renderização');
        }
    });

    // Função para mudar o ano
    function mudarAno(ano) {
        const url = new URL(window.location.href);
        url.searchParams.set('ano', ano);
        document.body.style.cursor = 'wait';
        window.location.href = url.toString();
    }

    // Setup de event listeners
    function setupEventListeners() {
        const anoSelect = document.getElementById('anoSelect');
        if (anoSelect) {
            anoSelect.addEventListener('change', (e) => mudarAno(e.target.value));
        }
    }

    // Configuração padrão dos gráficos
    Chart.defaults.font.family = 'Poppins';
    Chart.defaults.color = '#444';
    Chart.defaults.responsive = true;

    // Funções de formatação
    function formatNumber(number) {
        return new Intl.NumberFormat('pt-BR').format(number);
    }

    function formatCurrency(value) {
        return new Intl.NumberFormat('fr-FR', {
            style: 'currency',
            currency: 'XOF',
            minimumFractionDigits: 0,
            maximumFractionDigits: 0
        }).format(value);
    }

    // Configurações padrão dos gráficos
    function getDefaultChartOptions(titulo, config = {}) {
        return {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                title: {
                    display: true,
                    text: titulo,
                    font: {
                        family: 'Poppins',
                        size: 16,
                        weight: 'bold'
                    },
                    padding: 20
                },
                legend: {
                    position: 'bottom',
                    labels: {
                        font: {
                            family: 'Poppins',
                            size: 12
                        }
                    }
                },
                tooltip: {
                    backgroundColor: 'rgba(0, 0, 0, 0.8)',
                    titleFont: {
                        family: 'Poppins',
                        size: 13
                    },
                    bodyFont: {
                        family: 'Poppins',
                        size: 12
                    },
                    padding: 12
                }
            },
            ...config
        };
    }

    // Função para renderizar todos os gráficos
    function renderAllCharts() {
        if(!window.appData) {
            console.error('Dados não disponíveis');
            return;
        }        
        renderMarketShareChart();
        renderBandaLargaMovelChart();
        renderIndicadoresFinanceirosChart();
        renderTrafegoVozChart();
        renderTrafegoDadosChart();
        renderEmpregoChart();
    }

    // Adicione a função aqui
    function getDefaultChartOptions(titulo, config = {}) {
        return {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                title: {
                    display: true,
                    text: titulo,
                    font: {
                        family: 'Poppins',
                        size: 16,
                        weight: 'bold'
                    },
                    padding: 20
                },
                legend: {
                    position: 'bottom',
                    labels: {
                        font: {
                            family: 'Poppins',
                            size: 12
                        }
                    }
                },
                tooltip: {
                    backgroundColor: 'rgba(0, 0, 0, 0.8)',
                    titleFont: {
                        family: 'Poppins',
                        size: 13
                    },
                    bodyFont: {
                        family: 'Poppins',
                        size: 12
                    },
                    padding: 12
                }
            },
            ...config
        };
    }
    
    if(window.appData) {
        renderAllCharts();
        setupEventListeners();
    }
});

function renderAssinantesChart() {
    const assinantes = window.appData.mercado_movel?.assinantes;
    if (!assinantes?.mtn_total || !assinantes?.orange_total) {
        console.warn('Dados de assinantes incompletos');
        return;
    }

    const ctx = document.getElementById('assinantesChart')?.getContext('2d');
    if (!ctx) return;

    new Chart(ctx, {
        type: 'pie',
        data: {
            labels: ['MTN', 'Orange'],
            datasets: [{
                data: [assinantes.mtn_total, assinantes.orange_total],
                backgroundColor: [chartColors.MTN.main, chartColors.ORANGE.main],
                borderColor: [chartColors.MTN.secondary, chartColors.ORANGE.secondary],
                borderWidth: 2
            }]
        },
        options: {
            ...getDefaultChartOptions('Distribuição de Assinantes'),
            cutout: '30%',
            plugins: {
                legend: {
                    position: 'bottom',
                    labels: {
                        usePointStyle: true,
                        padding: 20,
                        font: {
                            size: 14
                        }
                    }
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            const label = context.label || '';
                            const value = context.raw;
                            const percentage = ((value / (assinantes.mtn_total + assinantes.orange_total)) * 100).toFixed(1);
                            return `${label}: ${formatNumber(value)} (${percentage}%)`;
                        }
                    }
                }
            }
        }
    });
}

function renderMarketShareChart() {
    const marketShare = window.appData.market_share;
    if (!marketShare) {
        console.warn('Dados de market share não disponíveis');
        return;
    }

    const ctx = document.getElementById('marketShareChart')?.getContext('2d');
    if (!ctx) return;

    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ['Assinantes', 'Receita', 'Tráfego'],
            datasets: [
                {
                    label: 'MTN',
                    data: [
                        marketShare.assinantes_rede_movel?.MTN || 0,
                        marketShare.receita_total?.MTN || 0,
                        marketShare.trafego_dados?.MTN || 0
                    ],
                    backgroundColor: chartColors.MTN.main,
                    borderColor: chartColors.MTN.secondary,
                    borderWidth: 2
                },
                {
                    label: 'Orange',
                    data: [
                        marketShare.assinantes_rede_movel?.ORANGE || 0,
                        marketShare.receita_total?.ORANGE || 0,
                        marketShare.trafego_dados?.ORANGE || 0
                    ],
                    backgroundColor: chartColors.ORANGE.main,
                    borderColor: chartColors.ORANGE.secondary,
                    borderWidth: 2
                }
            ]
        },
        options: {
            ...getDefaultChartOptions('Market Share por Indicador'),
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        callback: value => `${value}%`
                    }
                }
            },
            plugins: {
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            return `${context.dataset.label}: ${context.raw.toFixed(1)}%`;
                        }
                    }
                }
            }
        }
    });
}

function renderBandaLargaMovelChart() {
    const bandaLarga = window.appData.mercado_movel?.banda_larga_movel;
    if (!bandaLarga) {
        console.warn('Dados de banda larga móvel não disponíveis');
        return;
    }

    const ctx = document.getElementById('bandaLargaMovelChart')?.getContext('2d');
    if (!ctx) return;

    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ['3G', '4G'],
            datasets: [
                {
                    label: 'MTN',
                    data: [bandaLarga['3g'].mtn, bandaLarga['4g'].mtn],
                    backgroundColor: chartColors.MTN.main,
                    borderColor: chartColors.MTN.secondary,
                    borderWidth: 2
                },
                {
                    label: 'Orange',
                    data: [bandaLarga['3g'].orange, bandaLarga['4g'].orange],
                    backgroundColor: chartColors.ORANGE.main,
                    borderColor: chartColors.ORANGE.secondary,
                    borderWidth: 2
                }
            ]
        },
        options: {
            ...getDefaultChartOptions('Banda Larga Móvel por Tecnologia'),
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        callback: value => formatNumber(value)
                    }
                }
            },
            plugins: {
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            const label = context.dataset.label || '';
                            const value = context.raw;
                            return `${label}: ${formatNumber(value)} assinantes`;
                        }
                    }
                }
            }
        }
    });
}

function renderTrafegoVozChart() {
    const trafegoVoz = window.appData.trafego?.voz;
    if (!trafegoVoz) {
        console.warn('Dados de tráfego de voz não disponíveis');
        return;
    }

    const ctx = document.getElementById('trafegoVozChart')?.getContext('2d');
    if (!ctx) return;

    // Preparar dados para cada operadora
    const mtnData = {
        onNet: trafegoVoz.mtn?.on_net || 0,
        offNet: trafegoVoz.mtn?.off_net || 0
    };

    const orangeData = {
        onNet: trafegoVoz.orange?.on_net || 0,
        offNet: trafegoVoz.orange?.off_net || 0
    };

    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ['On-net', 'Off-net', 'Internacional'],
            datasets: [
                {
                    label: 'MTN',
                    data: [mtnData.onNet, mtnData.offNet, trafegoVoz.mtn?.internacional || 0],
                    backgroundColor: chartColors.MTN.main,
                    borderColor: chartColors.MTN.secondary,
                    borderWidth: 2
                },
                {
                    label: 'Orange',
                    data: [orangeData.onNet, orangeData.offNet, trafegoVoz.orange?.internacional || 0],
                    backgroundColor: chartColors.ORANGE.main,
                    borderColor: chartColors.ORANGE.secondary,
                    borderWidth: 2
                }
            ]
        },
        options: {
            ...getDefaultChartOptions('Distribuição do Tráfego de Voz'),
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        callback: value => `${formatNumber(value)} min`
                    }
                }
            },
            plugins: {
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            return `${context.dataset.label}: ${formatNumber(context.raw)} minutos`;
                        }
                    }
                }
            }
        }
    });
}

function renderTrafegoDadosChart() {
    const trafegoDados = window.appData.trafego?.dados;
    if (!trafegoDados) {
        console.warn('Dados de tráfego de dados não disponíveis');
        return;
    }

    const ctx = document.getElementById('trafegoDadosChart')?.getContext('2d');
    if (!ctx) return;

    new Chart(ctx, {
        type: 'line',
        data: {
            labels: ['3G', '4G'],
            datasets: [
                {
                    label: 'MTN',
                    data: [
                        trafegoDados.mtn?.['3g'] || 0,
                        trafegoDados.mtn?.['4g'] || 0
                    ],
                    backgroundColor: chartColors.MTN.background,
                    borderColor: chartColors.MTN.main,
                    borderWidth: 3,
                    tension: 0.4,
                    fill: true
                },
                {
                    label: 'Orange',
                    data: [
                        trafegoDados.orange?.['3g'] || 0,
                        trafegoDados.orange?.['4g'] || 0
                    ],
                    backgroundColor: chartColors.ORANGE.background,
                    borderColor: chartColors.ORANGE.main,
                    borderWidth: 3,
                    tension: 0.4,
                    fill: true
                }
            ]
        },
        options: {
            ...getDefaultChartOptions('Tráfego de Dados por Tecnologia'),
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        callback: value => formatDataSize(value)
                    }
                }
            },
            plugins: {
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            return `${context.dataset.label}: ${formatDataSize(context.raw)}`;
                        }
                    }
                }
            }
        }
    });
}

function formatDataSize(bytes) {
    const sizes = ['B', 'KB', 'MB', 'GB', 'TB'];
    if (bytes === 0) return '0 B';
    const i = parseInt(Math.floor(Math.log(bytes) / Math.log(1024)));
    return Math.round(bytes / Math.pow(1024, i), 2) + ' ' + sizes[i];
}

function renderIndicadoresFinanceirosChart() {
    const indicadores = window.appData.indicadores_financeiros?.por_operadora;
    if (!indicadores?.MTN || !indicadores?.ORANGE) {
        console.warn('Dados de indicadores financeiros incompletos');
        return;
    }

    const ctx = document.getElementById('indicadoresFinanceirosChart')?.getContext('2d');
    if (!ctx) return;

    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ['Volume de Negócio', 'Receita Total'],
            datasets: [
                {
                    label: 'MTN',
                    data: [
                        indicadores.MTN.volume_negocio,
                        indicadores.MTN.receita_total
                    ],
                    backgroundColor: chartColors.MTN.main,
                    borderColor: chartColors.MTN.secondary,
                    borderWidth: 2
                },
                {
                    label: 'Orange',
                    data: [
                        indicadores.ORANGE.volume_negocio,
                        indicadores.ORANGE.receita_total
                    ],
                    backgroundColor: chartColors.ORANGE.main,
                    borderColor: chartColors.ORANGE.secondary,
                    borderWidth: 2
                }
            ]
        },
        options: {
            ...getDefaultChartOptions('Indicadores Financeiros por Operadora'),
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        callback: value => formatCurrency(value)
                    }
                }
            },
            plugins: {
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            return `${context.dataset.label}: ${formatCurrency(context.raw)}`;
                        }
                    }
                }
            }
        }
    });
}

function renderEmpregoChart() {
    const emprego = window.appData.emprego?.por_operadora;
    if (!emprego?.MTN || !emprego?.ORANGE) {
        console.warn('Dados de emprego incompletos');
        return;
    }

    const ctx = document.getElementById('empregoChart')?.getContext('2d');
    if (!ctx) return;

    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ['MTN', 'Orange'],
            datasets: [
                {
                    label: 'Homens',
                    data: [
                        emprego.MTN.homens,
                        emprego.ORANGE.homens
                    ],
                    backgroundColor: chartColors.MTN.main,
                    borderColor: chartColors.MTN.secondary,
                    borderWidth: 2
                },
                {
                    label: 'Mulheres',
                    data: [
                        emprego.MTN.mulheres,
                        emprego.ORANGE.mulheres
                    ],
                    backgroundColor: chartColors.ORANGE.main,
                    borderColor: chartColors.ORANGE.secondary,
                    borderWidth: 2
                }
            ]
        },
        options: {
            ...getDefaultChartOptions('Emprego por Operadora e Gênero'),
            plugins: {
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            const total = context.raw;
                            const percentage = ((context.raw / window.appData.emprego.total) * 100).toFixed(1);
                            return `${context.dataset.label}: ${formatNumber(total)} (${percentage}%)`;
                        }
                    }
                }
            }
        }
    });
}

// Funções de Exportação
function downloadPDF() {
    const element = document.querySelector('.container');
    if (!element) return;

    // Configurações do PDF
    const pdfOptions = {
        margin: 10,
        filename: `Relatorio_Mercado_Telecom_${window.appData.ano_atual}.pdf`,
        image: { type: 'jpeg', quality: 0.98 },
        html2canvas: { 
            scale: 2,
            useCORS: true,
            logging: false
        },
        jsPDF: { 
            unit: 'mm', 
            format: 'a4', 
            orientation: 'portrait' 
        }
    };

    // Criar uma cópia do elemento para modificar
    const elementClone = element.cloneNode(true);
    prepareElementForExport(elementClone);

    // Gerar PDF
    html2pdf().set(pdfOptions).from(elementClone).save().catch(error => {
        console.error('Erro ao gerar PDF:', error);
        alert('Ocorreu um erro ao gerar o PDF. Por favor, tente novamente.');
    });
}

function downloadWord() {
    const element = document.querySelector('.container');
    if (!element) return;

    const header = `
        <html xmlns:o='urn:schemas-microsoft-com:office:office' 
              xmlns:w='urn:schemas-microsoft-com:office:word' 
              xmlns='http://www.w3.org/TR/REC-html40'>
        <head>
            <meta charset='utf-8'>
            <title>Relatório do Mercado de Telecomunicações</title>
            <style>
                /* Estilos para o documento Word */
                body { font-family: 'Calibri', sans-serif; }
                .chart-container { page-break-inside: avoid; }
                table { border-collapse: collapse; width: 100%; }
                th, td { border: 1px solid #ddd; padding: 8px; }
                th { background-color: #f4f4f4; }
            </style>
        </head>
        <body>
    `;

    // Criar uma cópia do elemento para modificar
    const elementClone = element.cloneNode(true);
    prepareElementForExport(elementClone);

    // Converter gráficos em imagens
    convertChartsToImages(elementClone).then(() => {
        const blob = new Blob(
            [header + elementClone.innerHTML + "</body></html>"], 
            { type: 'application/msword' }
        );
        
        const link = document.createElement('a');
        link.href = URL.createObjectURL(blob);
        link.download = `Relatorio_Mercado_Telecom_${window.appData.ano_atual}.doc`;
        link.click();
        URL.revokeObjectURL(link.href);
    });
}

// Funções auxiliares para exportação
function prepareElementForExport(element) {
    // Remover botões e elementos interativos
    element.querySelectorAll('.btn-group, .form-select').forEach(el => el.remove());
    
    // Adicionar estilos para impressão
    element.querySelectorAll('.card').forEach(card => {
        card.style.pageBreakInside = 'avoid';
        card.style.marginBottom = '20px';
    });
}

async function convertChartsToImages(element) {
    const charts = element.querySelectorAll('canvas');
    for (const canvas of charts) {
        try {
            const imageUrl = canvas.toDataURL('image/png');
            const img = document.createElement('img');
            img.src = imageUrl;
            img.style.width = '100%';
            img.style.maxWidth = '600px';
            canvas.parentNode.replaceChild(img, canvas);
        } catch (error) {
            console.error('Erro ao converter gráfico:', error);
        }
    }
}

// Função para formatar valores monetários em FCFA
function formatCurrency(value) {
    return new Intl.NumberFormat('fr-FR', {
        style: 'currency',
        currency: 'XOF',
        minimumFractionDigits: 0,
        maximumFractionDigits: 0
    }).format(value);
}