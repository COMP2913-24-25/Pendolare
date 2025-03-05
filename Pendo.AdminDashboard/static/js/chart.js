document.addEventListener('DOMContentLoaded', (event) => {
    const ctx = document.getElementById('weeklyIncomeChart').getContext('2d');
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ['1st week', '2nd week', '3rd week', '4th week', '5th week', '6th week'],
            datasets: [{
                label: 'Revenue in £',
                data: [4345, 1233, 7899, 4567, 2346, 6786],
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