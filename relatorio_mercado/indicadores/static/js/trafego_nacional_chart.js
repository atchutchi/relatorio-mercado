document.addEventListener('DOMContentLoaded', function() {
    console.log('Dados recebidos:', trafegoData);

    if (!trafegoData || !trafegoData.labels || trafegoData.labels.length === 0) {
        console.error('Dados de tráfego inválidos ou vazios');
        return;
    }

    // Função para criar tabelas
    function createTable(tableId, data, columns) {
        const table = document.getElementById(tableId);
        let html = '<thead><tr><th>Trimestre</th>';
        columns.forEach(col => {
            html += `<th>${col}</th>`;
        });
        html += '</tr></thead><tbody>';

        data.labels.forEach((label, index) => {
            html += `<tr><td>${label}</td>`;
            columns.forEach(col => {
                html += `<td>${data[col][index].toLocaleString()}</td>`;
            });
            html += '</tr>';
        });
        html += '</tbody>';
        table.innerHTML = html;
    }

    // Criar tabelas
    createTable('chamadasOriginadasTable', trafegoData.originadas, ['on_net', 'off_net', 'saida_internacional', 'total']);
    createTable('chamadasTerminadasTable', trafegoData.terminadas, ['off_net_entrada', 'entrada_internacional', 'total']);
    createTable('roamingTable', trafegoData.roaming, ['in', 'out', 'total']);

    // Função para criar gráficos
    function createChart(chartId, data, title) {
        const ctx = document.getElementById(chartId).getContext('2d');
        new Chart(ctx, {
            type: 'line',
            data: {
                labels: trafegoData.labels,
                datasets: Object.keys(data).map(key => ({
                    label: key,
                    data: data[key],
                    borderColor: getRandomColor(),
                    fill: false
                }))
            },
            options: {
                responsive: true,
                title: {
                    display: true,
                    text: title
                }
            }
        });
    }

    // Criar gráficos
    createChart('chamadasOriginadasChart', trafegoData.originadas, 'Chamadas Originadas');
    createChart('chamadasTerminadasChart', trafegoData.terminadas, 'Chamadas Terminadas');
    createChart('roamingChart', trafegoData.roaming, 'Minutos em Roaming');

    // Repartição do Tráfego de Voz
    const lastIndex = trafegoData.labels.length - 1;
    const reparticaoData = [
        trafegoData.originadas.on_net[lastIndex],
        trafegoData.originadas.off_net[lastIndex],
        trafegoData.terminadas.off_net_entrada[lastIndex],
        trafegoData.originadas.saida_internacional[lastIndex],
        trafegoData.terminadas.entrada_internacional[lastIndex]
    ];
    const total = reparticaoData.reduce((a, b) => a + b, 0);
    const reparticaoLabels = ['On-net', 'Off-net (Saída)', 'Off-net (Entrada)', 'Saída Internacional', 'Entrada Internacional'];

    // Criar tabela de repartição
    let reparticaoHtml = '<thead><tr><th>Tipo de Tráfego</th><th>Minutos</th><th>Percentagem</th></tr></thead><tbody>';
    reparticaoData.forEach((value, index) => {
        const percentage = ((value / total) * 100).toFixed(2);
        reparticaoHtml += `<tr><td>${reparticaoLabels[index]}</td><td>${value.toLocaleString()}</td><td>${percentage}%</td></tr>`;
    });
    reparticaoHtml += `<tr><td>Total</td><td>${total.toLocaleString()}</td><td>100%</td></tr></tbody>`;
    document.getElementById('reparticaoTrafegoTable').innerHTML = reparticaoHtml;

    // Criar gráfico de pizza para repartição
    const ctxReparticao = document.getElementById('reparticaoTrafegoChart').getContext('2d');
    new Chart(ctxReparticao, {
        type: 'pie',
        data: {
            labels: reparticaoLabels,
            datasets: [{
                data: reparticaoData,
                backgroundColor: reparticaoLabels.map(() => getRandomColor())
            }]
        },
        options: {
            responsive: true,
            title: {
                display: true,
                text: 'Repartição do Tráfego de Voz'
            }
        }
    });

    // Função auxiliar para gerar cores aleatórias
    function getRandomColor() {
        const letters = '0123456789ABCDEF';
        let color = '#';
        for (let i = 0; i < 6; i++) {
            color += letters[Math.floor(Math.random() * 16)];
        }
        return color;
    }
});