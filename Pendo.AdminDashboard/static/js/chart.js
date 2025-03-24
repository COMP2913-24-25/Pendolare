document.addEventListener('DOMContentLoaded', (event) => {
    console.log('Chart.js loaded.');
    const ctx = document.getElementById('weeklyIncomeChart').getContext('2d');
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: window.chartLabels,
            datasets: [{
                label: 'Revenue in £',
                data: [450, 500, 600, 700, 800, 463, 234],
                borderWidth: 1
            }]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
});