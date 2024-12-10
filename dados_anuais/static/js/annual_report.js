// Variáveis e configurações globais
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

// Configurações do Chart.js
Chart.defaults.font.family = 'Poppins';
Chart.defaults.color = '#444';
Chart.defaults.responsive = true;

document.addEventListener('DOMContentLoaded', function() {
    console.log('Dados recebidos:', window.appData);
    if(window.appData) {
        renderAllCharts();
        setupEventListeners();
    }

    // Event listener for Confirm button
    const confirmAnoButton = document.getElementById('confirmAnoButton');
    confirmAnoButton.addEventListener('click', function() {
        const anoSelect = document.getElementById('anoSelect');
        mudarAno(anoSelect.value);
    });
});

// Function to change the year and reload the page with selected year
function mudarAno(ano) {
    if (!ano) return;
    
    const currentUrl = new URL(window.location.href);
    currentUrl.searchParams.set('ano', ano);
    document.body.style.cursor = 'wait';
    window.location.href = currentUrl.toString();
}

// Funções de utilidade
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

function formatDataSize(bytes) {
    const sizes = ['B', 'KB', 'MB', 'GB', 'TB'];
    if (bytes === 0) return '0 B';
    const i = parseInt(Math.floor(Math.log(bytes) / Math.log(1024)));
    return Math.round(bytes / Math.pow(1024, i), 2) + ' ' + sizes[i];
}

// Opções padrão dos gráficos
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

// Função principal de renderização
function renderAllCharts() {
    if(!window.appData) {
        console.error('Dados não disponíveis');
        return;
    }

    // Limpar gráficos existentes
    Chart.helpers.each(Chart.instances, (instance) => {
        instance.destroy();
    });

    // Renderizar todos os gráficos
    renderMarketShareChart();
    renderBandaLargaMovelChart();
    renderIndicadoresFinanceirosChart();
    renderTrafegoVozChart();
    renderTrafegoDadosChart();
    renderEmpregoChart();
}

// Market Share Chart
function renderMarketShareChart() {
    const marketShare = window.appData.market_share;
    if (!marketShare) {
        console.warn('Dados de market share não disponíveis');
        return;
    }

    const ctx = document.getElementById('marketShareChart')?.getContext('2d');
    if (!ctx) {
        console.warn('Contexto do gráfico de market share não encontrado');
        return;
    }

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

// Banda Larga Móvel Chart
function renderBandaLargaMovelChart() {
    const bandaLarga = window.appData.mercado_movel?.banda_larga_movel;
    if (!bandaLarga) {
        console.warn('Dados de banda larga móvel não disponíveis');
        return;
    }

    const ctx = document.getElementById('bandaLargaMovelChart')?.getContext('2d');
    if (!ctx) {
        console.warn('Contexto do gráfico de banda larga não encontrado');
        return;
    }

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

// Indicadores Financeiros Chart
function renderIndicadoresFinanceirosChart() {
    const indicadores = window.appData.indicadores_financeiros?.por_operadora;
    if (!indicadores?.MTN || !indicadores?.ORANGE) {
        console.warn('Dados de indicadores financeiros incompletos');
        return;
    }

    const ctx = document.getElementById('indicadoresFinanceirosChart')?.getContext('2d');
    if (!ctx) {
        console.warn('Contexto do gráfico de indicadores financeiros não encontrado');
        return;
    }

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

// Tráfego de Voz Chart
function renderTrafegoVozChart() {
    const trafegoVoz = window.appData.trafego?.voz;
    if (!trafegoVoz || !trafegoVoz.por_operadora) {
        console.warn('Dados de tráfego de voz não disponíveis');
        return;
    }

    const ctx = document.getElementById('trafegoVozChart')?.getContext('2d');
    if (!ctx) {
        console.warn('Contexto do gráfico de tráfego de voz não encontrado');
        return;
    }

    const mtnData = trafegoVoz.por_operadora.MTN || {};
    const orangeData = trafegoVoz.por_operadora.ORANGE || {};

    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ['On-net', 'Off-net', 'Internacional'],
            datasets: [
                {
                    label: 'MTN',
                    data: [
                        mtnData.on_net || 0,
                        mtnData.off_net || 0,
                        mtnData.internacional || 0
                    ],
                    backgroundColor: chartColors.MTN.main,
                    borderColor: chartColors.MTN.secondary,
                    borderWidth: 2
                },
                {
                    label: 'Orange',
                    data: [
                        orangeData.on_net || 0,
                        orangeData.off_net || 0,
                        orangeData.internacional || 0
                    ],
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

// Tráfego de Dados Chart
function renderTrafegoDadosChart() {
    const trafegoDados = window.appData.trafego?.dados;
    if (!trafegoDados || !trafegoDados.por_operadora) {
        console.warn('Dados de tráfego de dados não disponíveis');
        return;
    }

    const ctx = document.getElementById('trafegoDadosChart')?.getContext('2d');
    if (!ctx) {
        console.warn('Contexto do gráfico de tráfego de dados não encontrado');
        return;
    }

    const mtnData = trafegoDados.por_operadora.MTN || {};
    const orangeData = trafegoDados.por_operadora.ORANGE || {};

    new Chart(ctx, {
        type: 'line',
        data: {
            labels: ['3G', '4G'],
            datasets: [
                {
                    label: 'MTN',
                    data: [mtnData['3g'] || 0, mtnData['4g'] || 0],
                    backgroundColor: chartColors.MTN.background,
                    borderColor: chartColors.MTN.main,
                    borderWidth: 3,
                    tension: 0.4,
                    fill: true
                },
                {
                    label: 'Orange',
                    data: [orangeData['3g'] || 0, orangeData['4g'] || 0],
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

// Emprego Chart
function renderEmpregoChart() {
    const emprego = window.appData.emprego?.por_operadora;
    if (!emprego?.MTN || !emprego?.ORANGE) {
        console.warn('Dados de emprego incompletos');
        return;
    }

    const ctx = document.getElementById('empregoChart')?.getContext('2d');
    if (!ctx) {
        console.warn('Contexto do gráfico de emprego não encontrado');
        return;
    }

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
                            const total = context.raw;
                            const percentage = ((total / window.appData.emprego.total) * 100).toFixed(1);
                            return `${context.dataset.label}: ${formatNumber(total)} (${percentage}%)`;
                        }
                    }
                }
            }
        }
    });
}

// Funções de Exportação
async function downloadPDF() {
    try {
        console.log('Iniciando download do PDF');
        const element = document.querySelector('.container');
        if (!element) {
            console.error('Elemento container não encontrado');
            return;
        }

        // Mostrar loading e feedback visual
        document.body.style.cursor = 'wait';
        const loadingDiv = document.createElement('div');
        loadingDiv.style.position = 'fixed';
        loadingDiv.style.top = '50%';
        loadingDiv.style.left = '50%';
        loadingDiv.style.transform = 'translate(-50%, -50%)';
        loadingDiv.style.background = 'rgba(0,0,0,0.8)';
        loadingDiv.style.color = 'white';
        loadingDiv.style.padding = '20px';
        loadingDiv.style.borderRadius = '10px';
        loadingDiv.innerHTML = 'Gerando PDF...';
        document.body.appendChild(loadingDiv);

        // Clonar elemento
        const elementClone = element.cloneNode(true);
        
        // Remover elementos desnecessários
        elementClone.querySelectorAll('.btn-group, .form-select, button, select').forEach(el => el.remove());

        // Converter Canvas para imagens
        console.log('Convertendo gráficos para imagens');
        const canvases = elementClone.querySelectorAll('canvas');
        for (const canvas of canvases) {
            try {
                console.log('Processando canvas:', canvas);
                const container = canvas.parentElement;
                const img = document.createElement('img');
                img.src = canvas.toDataURL('image/png');
                img.style.width = '100%';
                img.style.maxWidth = '800px';
                container.replaceChild(img, canvas);
            } catch (err) {
                console.error('Erro ao converter canvas:', err);
            }
        }

        // Configurações do PDF
        const opt = {
            margin: [10, 10, 10, 10],
            filename: `Relatorio_Mercado_Telecom_${window.appData?.ano_atual || new Date().getFullYear()}.pdf`,
            image: { type: 'jpeg', quality: 1 },
            html2canvas: { 
                scale: 2,
                useCORS: true,
                logging: true,
                allowTaint: true,
                foreignObjectRendering: true,
                scrollX: 0,
                scrollY: 0,
                windowWidth: document.documentElement.offsetWidth,
                windowHeight: document.documentElement.offsetHeight
            },
            jsPDF: { 
                unit: 'mm', 
                format: 'a4', 
                orientation: 'portrait',
                compress: true,
                putOnlyUsedFonts: true
            },
            pagebreak: { mode: ['avoid-all', 'css', 'legacy'] }
        };

        // Configurar estilos para impressão
        const styleSheet = document.createElement('style');
        styleSheet.textContent = `
            @media print {
                body { font-size: 12pt; }
                .card { page-break-inside: avoid; margin-bottom: 20px; }
                table { page-break-inside: avoid; }
                .chart-container { page-break-inside: avoid; }
                h1, h2, h3 { page-break-after: avoid; }
                img { max-width: 100% !important; }
            }
        `;
        elementClone.appendChild(styleSheet);

        console.log('Configurações PDF:', opt);

        // Gerar PDF
        try {
            const pdf = await html2pdf().set(opt).from(elementClone).save();
            console.log('PDF gerado com sucesso');
        } catch (error) {
            console.error('Erro na geração do PDF:', error);
            throw error;
        }

    } catch (error) {
        console.error('Erro ao gerar PDF:', error);
        alert('Ocorreu um erro ao gerar o PDF. Por favor, tente novamente.');
    } finally {
        document.body.style.cursor = 'default';
        document.querySelectorAll('[data-loading]').forEach(el => el.remove());
    }
}

function downloadWord() {
    try {
        const element = document.querySelector('.container');
        if (!element) {
            console.error('Elemento container não encontrado');
            return;
        }

        // Mostrar loading
        document.body.style.cursor = 'wait';

        // Criar cabeçalho do documento
        const header = `
            <html xmlns:o='urn:schemas-microsoft-com:office:office' 
                  xmlns:w='urn:schemas-microsoft-com:office:word' 
                  xmlns='http://www.w3.org/TR/REC-html40'>
            <head>
                <meta charset='utf-8'>
                <title>Relatório do Mercado de Telecomunicações</title>
                <style>
                    body { font-family: 'Calibri', sans-serif; }
                    .chart-container { page-break-inside: avoid; }
                    table { border-collapse: collapse; width: 100%; }
                    th, td { border: 1px solid #ddd; padding: 8px; }
                    th { background-color: #f4f4f4; }
                </style>
            </head>
            <body>
        `;

        // Criar clone e preparar para exportação
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
            link.download = `Relatorio_Mercado_Telecom_${window.appData?.ano_atual || new Date().getFullYear()}.doc`;
            link.click();
            URL.revokeObjectURL(link.href);
            
            document.body.style.cursor = 'default';
        });
    } catch (error) {
        console.error('Erro ao gerar documento Word:', error);
        alert('Ocorreu um erro ao gerar o documento Word. Por favor, tente novamente.');
        document.body.style.cursor = 'default';
    }
}

// Funções auxiliares para exportação
async function prepareElementForExport(element) {
    // Remover elementos interativos
    element.querySelectorAll('.btn-group, .form-select').forEach(el => el.remove());
    
    // Configurar estilos de impressão
    element.querySelectorAll('.card').forEach(card => {
        card.style.pageBreakInside = 'avoid';
        card.style.marginBottom = '20px';
    });

    // Aguardar um momento para os gráficos renderizarem
    await new Promise(resolve => setTimeout(resolve, 500));
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

// Setup de eventos
function setupEventListeners() {
    const anoSelect = document.getElementById('anoSelect');
    if (anoSelect) {
        anoSelect.addEventListener('change', e => mudarAno(e.target.value));
    }
}
