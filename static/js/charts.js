function initializeChart() {
    const chart = document.getElementById("doughnut");
    if (!chart) return;

    // Get the data from the chartData object
    const data = {
        labels: chartData.labels,
        datasets: [{
            label: "# of Events",
            data: chartData.data.map(value => parseInt(value) || 0), // Convert to numbers and handle null/undefined
            backgroundColor: [
                "#b31a4d", // Workshop
                "#4a920f", // Theatre
                "#582bac", // Concert
                "#e48e2c"  // Sport
            ],
            offset: 10,
            hoverOffset: 8,
            hoverBorderColor: "#9a999b",
            borderWidth: 1
        }]
    };

    // Destroy existing chart if it exists
    if (window.eventChart) {
        window.eventChart.destroy();
    }

    // Create new chart
    window.eventChart = new Chart(chart, {
        type: "doughnut",
        data: data,
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: true,
                    position: 'bottom',
                    labels: {
                        color: "#8b8a96",
                        font: {
                            size: 12,
                            weight: 600
                        },
                        padding: 20
                    }
                }
            },
            layout: {
                padding: {
                    top: 20,
                    bottom: 20
                }
            },
            cutout: '60%'
        }
    });

    // Resize chart on window resize
    window.addEventListener('resize', function() {
        if (window.eventChart) {
            window.eventChart.resize();
        }
    });
}

function populateEventList() {
    const eventList = document.querySelector(".chart ul");
    if (!eventList) return;

    // Clear existing list items
    eventList.innerHTML = '';

    // Add new list items
    chartData.labels.forEach((label, i) => {
        const value = parseInt(chartData.data[i]) || 0;
        const eachEvent = document.createElement("li");
        eachEvent.innerHTML = `${label}: <span class="percentage">${value}%</span>`;
        eventList.appendChild(eachEvent);
    });
}

// Initialize chart when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    // Wait a bit to ensure the canvas is ready
    setTimeout(() => {
        initializeChart();
        populateEventList();
    }, 100);
}); 