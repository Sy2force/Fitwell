document.addEventListener('DOMContentLoaded', () => {
    // Check if Chart.js is loaded
    if (typeof Chart === 'undefined') {
        console.error('Chart.js is not loaded');
        return;
    }

    // Configuration commune
    Chart.defaults.color = '#6b7280';
    Chart.defaults.borderColor = 'rgba(255, 255, 255, 0.05)';
    Chart.defaults.font.family = '"JetBrains Mono", monospace';
    
    // Retrieve data from JSON script tags
    const datesElement = document.getElementById('chart-dates-data');
    const weightElement = document.getElementById('chart-weight-data');
    const sleepElement = document.getElementById('chart-sleep-data');
    const moodElement = document.getElementById('chart-mood-data');

    if (!datesElement || !weightElement || !sleepElement || !moodElement) {
        return;
    }

    const dates = JSON.parse(datesElement.textContent);
    const weightData = JSON.parse(weightElement.textContent);
    const sleepData = JSON.parse(sleepElement.textContent);
    const moodData = JSON.parse(moodElement.textContent);
    
    // Retrieve translations from config or use defaults
    const config = window.dashboardConfig || {
        labelWeight: "Poids (kg)",
        labelSleep: "Sommeil (h)",
        labelMood: "Humeur (1-10)"
    };

    // Weight Chart
    const weightCanvas = document.getElementById('weightChart');
    if (weightCanvas) {
        const ctxWeight = weightCanvas.getContext('2d');
        const gradientWeight = ctxWeight.createLinearGradient(0, 0, 0, 400);
        gradientWeight.addColorStop(0, 'rgba(234, 179, 8, 0.2)'); // Energy color
        gradientWeight.addColorStop(1, 'rgba(234, 179, 8, 0)');

        new Chart(weightCanvas, {
            type: 'line',
            data: {
                labels: dates,
                datasets: [{
                    label: config.labelWeight,
                    data: weightData,
                    borderColor: '#eab308', // energy color
                    backgroundColor: gradientWeight,
                    borderWidth: 2,
                    pointBackgroundColor: '#000',
                    pointBorderColor: '#eab308',
                    pointBorderWidth: 2,
                    tension: 0.4,
                    fill: true
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: { 
                    legend: { display: false },
                    tooltip: {
                        backgroundColor: 'rgba(15, 15, 22, 0.9)',
                        titleColor: '#fff',
                        bodyColor: '#eab308',
                        borderColor: 'rgba(255, 255, 255, 0.1)',
                        borderWidth: 1,
                        padding: 10,
                        displayColors: false,
                    }
                },
                scales: { 
                    x: { grid: { display: false } },
                    y: { grid: { color: 'rgba(255,255,255,0.05)' } } 
                }
            }
        });
    }

    // Sleep & Mood Chart
    const sleepMoodCanvas = document.getElementById('sleepMoodChart');
    if (sleepMoodCanvas) {
        new Chart(sleepMoodCanvas, {
            type: 'bar',
            data: {
                labels: dates,
                datasets: [
                    {
                        label: config.labelSleep,
                        data: sleepData,
                        backgroundColor: 'rgba(0, 243, 255, 0.5)', // primary cyan
                        hoverBackgroundColor: 'rgba(0, 243, 255, 0.8)',
                        borderRadius: 2,
                        order: 2
                    },
                    {
                        type: 'line',
                        label: config.labelMood,
                        data: moodData,
                        borderColor: '#7000ff', // secondary purple
                        borderWidth: 2,
                        pointBackgroundColor: '#000',
                        pointBorderColor: '#7000ff',
                        pointBorderWidth: 2,
                        tension: 0.4,
                        yAxisID: 'y1',
                        order: 1
                    }
                ]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: { 
                        labels: { font: { size: 10, family: '"JetBrains Mono", monospace' }, color: '#9ca3af' },
                        position: 'top',
                        align: 'end'
                    },
                    tooltip: {
                        backgroundColor: 'rgba(15, 15, 22, 0.9)',
                        titleColor: '#fff',
                        borderColor: 'rgba(255, 255, 255, 0.1)',
                        borderWidth: 1,
                        padding: 10,
                    }
                },
                scales: {
                    x: { grid: { display: false } },
                    y: { 
                        beginAtZero: true, 
                        max: 12, 
                        grid: { color: 'rgba(255,255,255,0.05)' },
                        ticks: { color: '#6b7280' }
                    },
                    y1: { 
                        beginAtZero: true, 
                        max: 10, 
                        position: 'right', 
                        grid: { display: false },
                        ticks: { color: '#6b7280' }
                    }
                }
            }
        });
    }
});
