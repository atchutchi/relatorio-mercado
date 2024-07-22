document.addEventListener('DOMContentLoaded', function() {
    const dataElement = document.getElementById('emprego-data');
    const empregoData = JSON.parse(dataElement.getAttribute('data-emprego'));
    
    console.log('Dados recebidos:', empregoData);  // Log para depuração

    // Função para preencher a tabela e o resumo
    function preencherDados() {
        const elementos = ['direto', 'nacionais', 'homem', 'mulher', 'indireto'];
        elementos.forEach(elem => {
            document.getElementById(`mtn-${elem}`).textContent = empregoData.mtn[elem];
            document.getElementById(`orange-${elem}`).textContent = empregoData.orange[elem];
            const total = empregoData.mtn[elem] + empregoData.orange[elem];
            document.getElementById(`total-${elem}`).textContent = total;
            if (document.getElementById(`total-${elem}-table`)) {
                document.getElementById(`total-${elem}-table`).textContent = total;
            }
        });
    }

    preencherDados();

    // Criar o gráfico
    var ctx = document.getElementById('empregoSetorChart').getContext('2d');
    var chart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ['Emprego Direto', 'Nacionais', 'Homem', 'Mulher', 'Emprego Indireto'],
            datasets: [{
                label: 'MTN',
                data: [
                    empregoData.mtn.direto,
                    empregoData.mtn.nacionais,
                    empregoData.mtn.homem,
                    empregoData.mtn.mulher,
                    empregoData.mtn.indireto
                ],
                backgroundColor: 'rgba(255, 204, 0, 0.7)', // Amarelo para MTN
                borderColor: 'rgb(255, 204, 0)',
                borderWidth: 1
            }, {
                label: 'Orange',
                data: [
                    empregoData.orange.direto,
                    empregoData.orange.nacionais,
                    empregoData.orange.homem,
                    empregoData.orange.mulher,
                    empregoData.orange.indireto
                ],
                backgroundColor: 'rgba(255, 140, 0, 0.7)', // Laranja para Orange
                borderColor: 'rgb(255, 140, 0)',
                borderWidth: 1
            }]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true
                }
            },
            responsive: true,
            maintainAspectRatio: false,
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