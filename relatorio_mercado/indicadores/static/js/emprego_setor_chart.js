document.addEventListener('DOMContentLoaded', function() {
    // Dados do emprego (você precisará passar esses dados do backend)
    const empregoData = {{ emprego_data|safe }};

    // Preencher a tabela
    document.getElementById('mtn-direto').textContent = empregoData.mtn.direto;
    document.getElementById('orange-direto').textContent = empregoData.orange.direto;
    document.getElementById('total-direto').textContent = empregoData.mtn.direto + empregoData.orange.direto;

    document.getElementById('mtn-nacionais').textContent = empregoData.mtn.nacionais;
    document.getElementById('orange-nacionais').textContent = empregoData.orange.nacionais;
    document.getElementById('total-nacionais').textContent = empregoData.mtn.nacionais + empregoData.orange.nacionais;

    document.getElementById('mtn-homem').textContent = empregoData.mtn.homem;
    document.getElementById('orange-homem').textContent = empregoData.orange.homem;
    document.getElementById('total-homem').textContent = empregoData.mtn.homem + empregoData.orange.homem;

    document.getElementById('mtn-mulher').textContent = empregoData.mtn.mulher;
    document.getElementById('orange-mulher').textContent = empregoData.orange.mulher;
    document.getElementById('total-mulher').textContent = empregoData.mtn.mulher + empregoData.orange.mulher;

    document.getElementById('mtn-indireto').textContent = empregoData.mtn.indireto;
    document.getElementById('orange-indireto').textContent = empregoData.orange.indireto;
    document.getElementById('total-indireto').textContent = empregoData.mtn.indireto + empregoData.orange.indireto;

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
                backgroundColor: 'rgba(255, 206, 86, 0.2)',
                borderColor: 'rgba(255, 206, 86, 1)',
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
                backgroundColor: 'rgba(75, 192, 192, 0.2)',
                borderColor: 'rgba(75, 192, 192, 1)',
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