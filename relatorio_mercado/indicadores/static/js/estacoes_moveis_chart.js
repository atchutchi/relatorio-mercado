document.addEventListener('DOMContentLoaded', function() {
    const estacoesMoveisRaw = document.getElementById('estacoesMoveisTotalChart').dataset.estacoes;
    
    try {
        const estacoesMoveis = JSON.parse(estacoesMoveisRaw);

        // Gráfico de linha para o total de estações móveis
        var ctxTotal = document.getElementById('estacoesMoveisTotalChart').getContext('2d');
        new Chart(ctxTotal, {
            type: 'line',
            data: {
                labels: estacoesMoveis.labels,
                datasets: [{
                    label: 'Total de Estações Móveis',
                    data: estacoesMoveis.total,
                    borderColor: 'rgb(75, 192, 192)',
                    tension: 0.1
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    title: {
                        display: true,
                        text: 'Evolução do Total de Estações Móveis'
                    }
                }
            }
        });

        // Gráfico de barras empilhadas para distribuição por operador
        var ctxOperador = document.getElementById('estacoesMoveisPorOperadorChart').getContext('2d');
        new Chart(ctxOperador, {
            type: 'bar',
            data: {
                labels: estacoesMoveis.labels,
                datasets: [{
                    label: 'MTN',
                    data: estacoesMoveis.mtn,
                    backgroundColor: 'rgba(255, 204, 0, 0.7)', // Amarelo para MTN
                    borderColor: 'rgb(255, 204, 0)',
                    borderWidth: 1
                }, {
                    label: 'Orange',
                    data: estacoesMoveis.orange,
                    backgroundColor: 'rgba(255, 140, 0, 0.7)', // Laranja para Orange
                    borderColor: 'rgb(255, 140, 0)',
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    x: {
                        stacked: true,
                    },
                    y: {
                        stacked: true
                    }
                },
                plugins: {
                    title: {
                        display: true,
                        text: 'Distribuição de Estações Móveis por Operador'
                    }
                }
            }
        });

        // Preencher a tabela de crescimento trimestral
        const tableBody = document.getElementById('crescimentoTrimestralBody');
        for (let i = 1; i < estacoesMoveis.labels.length; i++) {
            for (const operador of ['MTN', 'Orange']) {
                const row = document.createElement('tr');
                const dados = operador === 'MTN' ? estacoesMoveis.mtn : estacoesMoveis.orange;
                
                const evolucaoAbsoluta = dados[i] - dados[i-1];
                const crescimentoPercentual = ((dados[i] - dados[i-1]) / dados[i-1] * 100).toFixed(1);

                row.innerHTML = `
                    <td>${operador}</td>
                    <td>${estacoesMoveis.labels[i]}</td>
                    <td>${dados[i].toLocaleString()}</td>
                    <td>${evolucaoAbsoluta.toLocaleString()}</td>
                    <td>${crescimentoPercentual}%</td>
                `;
                tableBody.appendChild(row);
            }
        }
    } catch (e) {
        console.error('Error parsing JSON:', e);
    }
});