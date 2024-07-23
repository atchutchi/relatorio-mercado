// Espera que o DOM esteja completamente carregado antes de executar o código
document.addEventListener('DOMContentLoaded', function() {
    // Log dos dados recebidos do backend para depuração
    console.log('Dados recebidos:', empregoData);

    // Função para exibir mensagens de erro
    function showError(message) {
        const errorDiv = document.getElementById('error-message');
        errorDiv.textContent = message;
        errorDiv.style.display = 'block';
    }

    // Função para preencher a tabela com os dados de emprego
    function preencherTabela() {
        // Define os campos que serão preenchidos
        const campos = ['direto', 'nacionais', 'homem', 'mulher', 'indireto'];
        // Obtém as operadoras dos dados recebidos
        const operadoras = Object.keys(empregoData);

        console.log('Operadoras encontradas:', operadoras);

        // Itera sobre cada operadora
        operadoras.forEach(operadora => {
            console.log(`Dados para ${operadora}:`, empregoData[operadora]);
            
            // Preenche os dados para cada campo da operadora
            campos.forEach(campo => {
                let valor = empregoData[operadora][campo] || 0;
                console.log(`${operadora} - ${campo}: ${valor}`);
                // Preenche a célula da tabela com o valor
                document.getElementById(`${operadora}-${campo}`).textContent = valor;
            });
        });

        // Calcula e preenche os totais
        campos.forEach(campo => {
            let total = operadoras.reduce((sum, operadora) => sum + (empregoData[operadora][campo] || 0), 0);
            console.log(`Total - ${campo}: ${total}`);
            document.getElementById(`total-${campo}`).textContent = total;
        });
    }

    // Verifica se há dados de emprego disponíveis
    if (!empregoData || (Object.keys(empregoData).length === 0)) {
        showError('Nenhum dado de emprego disponível.');
        return;
    }

    // Preenche a tabela com os dados
    preencherTabela();

    // Cria o gráfico de barras
    var ctx = document.getElementById('empregoSetorChart').getContext('2d');
    var chart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ['Emprego Direto', 'Nacionais', 'Homem', 'Mulher', 'Emprego Indireto'],
            datasets: Object.keys(empregoData).map(operadora => ({
                label: operadora.toUpperCase(),
                data: [
                    empregoData[operadora].direto,
                    empregoData[operadora].nacionais,
                    empregoData[operadora].homem,
                    empregoData[operadora].mulher,
                    empregoData[operadora].indireto
                ],
                backgroundColor: operadora.toLowerCase() === 'mtn' ? 'rgba(255, 204, 0, 0.7)' : 'rgba(255, 140, 0, 0.7)',
                borderColor: operadora.toLowerCase() === 'mtn' ? 'rgb(255, 204, 0)' : 'rgb(255, 140, 0)',
                borderWidth: 1
            }))
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true
                }
            },
            responsive: true,
            plugins: {
                legend: {
                    position: 'top',
                },
                title: {
                    display: true,
                    text: 'Emprego no Setor das TIC'
                }
            }
        }
    });
});