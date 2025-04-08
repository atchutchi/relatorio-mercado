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

// Cores alternativas para operadoras adicionais
const fallbackColors = [
    { main: '#4285F4', secondary: '#0F9D58', background: 'rgba(66, 133, 244, 0.2)' }, // Azul Google
    { main: '#DB4437', secondary: '#4285F4', background: 'rgba(219, 68, 55, 0.2)' },  // Vermelho Google
    { main: '#0F9D58', secondary: '#DB4437', background: 'rgba(15, 157, 88, 0.2)' },  // Verde Google
    { main: '#F4B400', secondary: '#0F9D58', background: 'rgba(244, 180, 0, 0.2)' },  // Amarelo Google
    { main: '#673AB7', secondary: '#3F51B5', background: 'rgba(103, 58, 183, 0.2)' }, // Roxo
    { main: '#3F51B5', secondary: '#673AB7', background: 'rgba(63, 81, 181, 0.2)' },  // Indigo
    { main: '#009688', secondary: '#4CAF50', background: 'rgba(0, 150, 136, 0.2)' },  // Teal
    { main: '#4CAF50', secondary: '#009688', background: 'rgba(76, 175, 80, 0.2)' }   // Verde
];

// Configurações do Chart.js
Chart.defaults.font.family = 'Poppins';
Chart.defaults.color = '#444';
Chart.defaults.responsive = true;

document.addEventListener('DOMContentLoaded', function() {
    console.log('Dados recebidos:', window.appData);
    if(window.appData) {
        // Configurar cores dinâmicas para operadoras
        setupOperadoraColors();
        renderAllCharts();
        setupEventListeners();
    }

    // Event listener for Confirm button
    const confirmAnoButton = document.getElementById('confirmAnoButton');
    if (confirmAnoButton) {
        confirmAnoButton.addEventListener('click', function() {
            const anoSelect = document.getElementById('anoSelect');
            mudarAno(anoSelect.value);
        });
    }
});

// Configura cores dinâmicas para todas as operadoras encontradas nos dados
function setupOperadoraColors() {
    try {
        if (!window.appData) {
            console.warn('Dados não disponíveis para configurar cores de operadoras');
            return;
        }
        
        // Tenta obter operadoras de várias fontes possíveis
        let operadoras = new Set();
        
        // Market share (assinantes)
        if (window.appData.market_share?.assinantes_rede_movel) {
            Object.keys(window.appData.market_share.assinantes_rede_movel)
                .filter(op => op !== 'TOTAL')
                .forEach(op => operadoras.add(op));
        }
        
        // Indicadores financeiros
        if (window.appData.indicadores_financeiros?.receita_total) {
            Object.keys(window.appData.indicadores_financeiros.receita_total)
                .filter(op => op !== 'TOTAL')
                .forEach(op => operadoras.add(op));
        }
        
        // Tráfego
        if (window.appData.trafego?.trafego_dados) {
            Object.keys(window.appData.trafego.trafego_dados)
                .filter(op => op !== 'TOTAL')
                .forEach(op => operadoras.add(op));
        }
        
        // Emprego
        if (window.appData.emprego?.total) {
            Object.keys(window.appData.emprego.total)
                .filter(op => op !== 'TOTAL')
                .forEach(op => operadoras.add(op));
        }
        
        // Se não encontrou operadoras, tenta definir as padrões (MTN e ORANGE)
        if (operadoras.size === 0) {
            console.warn('Nenhuma operadora encontrada nos dados, usando operadoras padrão');
            operadoras.add('MTN');
            operadoras.add('ORANGE');
        }
        
        // Adiciona cores para operadoras que não possuem configuração
        let colorIndex = 0;
        operadoras.forEach(operadora => {
            if (!chartColors[operadora]) {
                chartColors[operadora] = fallbackColors[colorIndex % fallbackColors.length];
                colorIndex++;
            }
        });
        
        console.log('Cores configuradas para operadoras:', operadoras);
    } catch (error) {
        console.error('Erro ao configurar cores para operadoras:', error);
    }
}

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

    try {
        // Limpar gráficos existentes
        Chart.helpers.each(Chart.instances, (instance) => {
            instance.destroy();
        });

        // Renderizar todos os gráficos - com tratamento de erros para cada um
        try {
            renderMarketShareChart();
        } catch (error) {
            console.error('Erro ao renderizar gráfico de market share:', error);
        }

        try {
            renderBandaLargaMovelChart();
        } catch (error) {
            console.error('Erro ao renderizar gráfico de banda larga móvel:', error);
        }

        try {
            renderIndicadoresFinanceirosChart();
        } catch (error) {
            console.error('Erro ao renderizar gráfico de indicadores financeiros:', error);
        }

        try {
            renderTrafegoVozChart();
        } catch (error) {
            console.error('Erro ao renderizar gráfico de tráfego de voz:', error);
        }

        try {
            renderTrafegoDadosChart();
        } catch (error) {
            console.error('Erro ao renderizar gráfico de tráfego de dados:', error);
        }

        try {
            renderEmpregoChart();
        } catch (error) {
            console.error('Erro ao renderizar gráfico de emprego:', error);
        }
    } catch (error) {
        console.error('Erro ao renderizar gráficos:', error);
    }
}

// Market Share Chart
function renderMarketShareChart() {
    const marketShare = window.appData.market_share;
    if (!marketShare || !marketShare.assinantes_rede_movel) {
        console.warn('Dados de market share não disponíveis ou incompletos');
        return;
    }

    const ctx = document.getElementById('marketShareChart')?.getContext('2d');
    if (!ctx) {
        console.warn('Contexto do gráfico de market share não encontrado');
        return;
    }

    // Obter todas as operadoras (excluindo TOTAL)
    const operadoras = Object.keys(marketShare.assinantes_rede_movel || {})
                       .filter(op => op !== 'TOTAL');
                       
    if (operadoras.length === 0) {
        console.warn('Nenhuma operadora encontrada nos dados de market share');
        return;
    }

    // Indicadores a serem mostrados
    const indicadores = ['assinantes_rede_movel', 'receita_total', 'trafego_dados'];
    const labels = ['Assinantes', 'Receita', 'Tráfego'];

    // Criar datasets dinâmicos para cada operadora
    const datasets = operadoras.map(operadora => {
        return {
            label: operadora,
            data: indicadores.map(indicador => {
                return marketShare[indicador]?.[operadora] || 0;
            }),
            backgroundColor: chartColors[operadora]?.main || chartColors.outros.main,
            borderColor: chartColors[operadora]?.secondary || chartColors.outros.main,
            borderWidth: 2
        };
    });

    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: datasets
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
    const bandaLarga = window.appData.mercado?.banda_larga_movel;
    if (!bandaLarga || !bandaLarga['3g'] || !bandaLarga['4g']) {
        console.warn('Dados de banda larga móvel não disponíveis ou incompletos');
        return;
    }

    const ctx = document.getElementById('bandaLargaMovelChart')?.getContext('2d');
    if (!ctx) {
        console.warn('Contexto do gráfico de banda larga não encontrado');
        return;
    }

    // Obter todas as operadoras da estrutura de dados
    const operadoras3g = Object.keys(bandaLarga['3g'].por_operadora || {})
                        .filter(op => op !== 'TOTAL');
    const operadoras4g = Object.keys(bandaLarga['4g'].por_operadora || {})
                        .filter(op => op !== 'TOTAL');
                        
    // Unir os conjuntos de operadoras
    const operadoras = [...new Set([...operadoras3g, ...operadoras4g])];
    
    if (operadoras.length === 0) {
        console.warn('Nenhuma operadora encontrada nos dados de banda larga móvel');
        return;
    }

    // Criar datasets dinâmicos para cada operadora
    const datasets = operadoras.map(operadora => {
        return {
            label: operadora,
            data: [
                bandaLarga['3g'].por_operadora?.[operadora] || 0,
                bandaLarga['4g'].por_operadora?.[operadora] || 0
            ],
            backgroundColor: chartColors[operadora]?.main || chartColors.outros.main,
            borderColor: chartColors[operadora]?.secondary || chartColors.outros.main,
            borderWidth: 2
        };
    });

    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ['3G', '4G'],
            datasets: datasets
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
    const indicadores = window.appData.indicadores_financeiros;
    if (!indicadores) {
        console.warn('Dados de indicadores financeiros não disponíveis');
        return;
    }

    const ctx = document.getElementById('indicadoresFinanceirosChart')?.getContext('2d');
    if (!ctx) {
        console.warn('Contexto do gráfico de indicadores financeiros não encontrado');
        return;
    }

    // Verificar se temos os campos necessários
    if (!indicadores.volume_negocio && !indicadores.receita_total) {
        console.warn('Campos necessários de indicadores financeiros não disponíveis:', Object.keys(indicadores));
        return;
    }

    // Obter operadoras (excluindo TOTAL)
    const operadoras = Object.keys(indicadores.volume_negocio || indicadores.receita_total || {})
                        .filter(op => op !== 'TOTAL');
    
    if (operadoras.length === 0) {
        console.warn('Nenhuma operadora encontrada nos dados de indicadores financeiros');
        return;
    }
    
    // Indicadores financeiros a mostrar
    const indicadoresFinanceiros = ['volume_negocio', 'receita_total', 'investimentos'];
    const labels = ['Volume de Negócio', 'Receita Total', 'Investimentos'];
    
    // Criar datasets para cada operadora
    const datasets = operadoras.map(operadora => {
        return {
            label: operadora,
            data: indicadoresFinanceiros.map(indicador => 
                indicadores[indicador]?.[operadora] || 0
            ),
            backgroundColor: chartColors[operadora]?.main || chartColors.outros.main,
            borderColor: chartColors[operadora]?.secondary || chartColors.outros.main,
            borderWidth: 2
        };
    });

    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: datasets
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
    const trafego = window.appData.trafego;
    if (!trafego) {
        console.warn('Dados de tráfego não disponíveis');
        return;
    }

    const ctx = document.getElementById('trafegoVozChart')?.getContext('2d');
    if (!ctx) {
        console.warn('Contexto do gráfico de tráfego de voz não encontrado');
        return;
    }

    // Verificar se temos dados para os campos específicos
    if (!trafego.trafego_voz_on_net || !trafego.trafego_voz_off_net || !trafego.trafego_voz_internacional) {
        console.warn('Dados específicos de tráfego de voz não disponíveis');
        return;
    }

    // Obter operadoras (excluindo TOTAL)
    const operadoras = Object.keys(trafego.trafego_voz_on_net || {})
                        .filter(op => op !== 'TOTAL');
    
    if (operadoras.length === 0) {
        console.warn('Nenhuma operadora encontrada para tráfego de voz');
        return;
    }

    // Criar datasets para cada operadora
    const datasets = operadoras.map(operadora => {
        return {
            label: operadora,
            data: [
                trafego.trafego_voz_on_net[operadora] || 0,
                trafego.trafego_voz_off_net[operadora] || 0,
                trafego.trafego_voz_internacional[operadora] || 0
            ],
            backgroundColor: chartColors[operadora]?.main || chartColors.outros.main,
            borderColor: chartColors[operadora]?.secondary || chartColors.outros.main,
            borderWidth: 2
        };
    });

    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ['On-net', 'Off-net', 'Internacional'],
            datasets: datasets
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
    const trafego = window.appData.trafego;
    if (!trafego || !trafego.trafego_dados) {
        console.warn('Dados de tráfego não disponíveis ou incompletos');
        return;
    }

    const ctx = document.getElementById('trafegoDadosChart')?.getContext('2d');
    if (!ctx) {
        console.warn('Contexto do gráfico de tráfego de dados não encontrado');
        return;
    }

    // Obter todas as operadoras (excluindo TOTAL)
    const operadoras = Object.keys(trafego.trafego_dados || {})
                        .filter(op => op !== 'TOTAL');
    
    if (operadoras.length === 0) {
        console.warn('Nenhuma operadora encontrada para tráfego de dados');
        return;
    }
    
    // Criar datasets dinâmicos para cada operadora
    const datasets = operadoras.map((operadora, index) => {
        return {
            label: operadora,
            data: [trafego.trafego_dados[operadora] || 0],
            backgroundColor: chartColors[operadora]?.background || chartColors.outros.background,
            borderColor: chartColors[operadora]?.main || chartColors.outros.main,
            borderWidth: 3,
            tension: 0.4,
            fill: true
        };
    });

    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ['Tráfego de Dados'],
            datasets: datasets
        },
        options: {
            ...getDefaultChartOptions('Tráfego de Dados por Operadora'),
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
    const emprego = window.appData.emprego;
    if (!emprego) {
        console.warn('Dados de emprego não disponíveis');
        return;
    }

    const ctx = document.getElementById('empregoChart')?.getContext('2d');
    if (!ctx) {
        console.warn('Contexto do gráfico de emprego não encontrado');
        return;
    }

    // Verificar se temos os campos necessários
    if (!emprego.emprego_total || !emprego.emprego_homens || !emprego.emprego_mulheres) {
        console.warn('Campos necessários de emprego não disponíveis:', Object.keys(emprego));
        return;
    }

    // Obter todas as operadoras (excluindo TOTAL)
    const operadoras = Object.keys(emprego.emprego_total || {})
                      .filter(op => op !== 'TOTAL');
    
    if (operadoras.length === 0) {
        console.warn('Nenhuma operadora encontrada nos dados de emprego');
        return;
    }
    
    // Preparar dados para o gráfico
    const labels = operadoras;
    
    // Criar datasets para funcionários homens e mulheres
    const datasets = [
        {
            label: 'Homens',
            data: operadoras.map(op => emprego.emprego_homens[op] || 0),
            backgroundColor: chartColors[operadoras[0]]?.main || chartColors.outros.main,
            borderColor: chartColors[operadoras[0]]?.secondary || chartColors.outros.main,
            borderWidth: 2
        },
        {
            label: 'Mulheres',
            data: operadoras.map(op => emprego.emprego_mulheres[op] || 0),
            backgroundColor: chartColors[operadoras[1] || operadoras[0]]?.main || chartColors.outros.main,
            borderColor: chartColors[operadoras[1] || operadoras[0]]?.secondary || chartColors.outros.main,
            borderWidth: 2
        }
    ];

    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: datasets
        },
        options: {
            ...getDefaultChartOptions('Emprego por Operadora'),
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
                            const totalEmpregos = emprego.emprego_total.TOTAL || 0;
                            const percentage = totalEmpregos > 0 ? ((total / totalEmpregos) * 100).toFixed(1) : 0;
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
