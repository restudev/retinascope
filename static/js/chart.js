var optionsProfileVisit = {
    annotations: {
        position: 'back'
    },
    dataLabels: {
        enabled: false
    },
    chart: {
        type: 'bar',
        height: 300
    },
    fill: {
        opacity: 1
    },
    plotOptions: {},
    series: [{
        name: 'Count: ',
        data: [1805, 370, 999, 139, 295]  // Sample data for 5 DR classes
    }],
    colors: ['#007bff', '#ffc107', '#ff9900', '#dc3545', '#28a745'],  // Blue, Yellow, and other colors
    xaxis: {
        categories: ["No DR", "Mild", "Moderate", "Severe", "Proliferative"],  // 5 DR classes
    }
};

let optionsDataSplit = {
    series: [70, 15, 15], // 70% for Training Set, 15% for Validation Set, 15% for Test Set
    labels: ['Training Set', 'Validation Set', 'Test Set'],
    colors: ['#007bff', '#ffc107', '#28a745'], // Blue, Yellow, and Green (complementary color)
    chart: {
        type: 'donut',
        width: '100%',
        height: '350px'
    },
    legend: {
        position: 'bottom' // Legend position at the bottom
    },
    plotOptions: {
        pie: {
            donut: {
                size: '30%' // Size of the donut hole
            }
        }
    }
};

document.addEventListener("DOMContentLoaded", function() {
    var chartProfileVisit = new ApexCharts(document.querySelector("#chart-profile-visit"), optionsProfileVisit);
    var chartDataSplit = new ApexCharts(document.getElementById('chart-data-split'), optionsDataSplit);

    // Render charts
    chartProfileVisit.render();
    chartDataSplit.render();
});

        
// Data for Accuracy Chart
const accuracyData = {
    labels: Array.from({ length: 50 }, (_, i) => ` ${i + 1}`),
    datasets: [
        {
            label: 'Training Accuracy',
            data: [
                0.4899, 0.6815, 0.7181, 0.7463, 0.7407, 0.7473, 0.7604, 0.7570, 0.7464, 0.7549, 0.7722,
                0.7615, 0.7665, 0.7802, 0.7868, 0.7836, 0.8075, 0.7888, 0.7764, 0.8023, 0.8003, 0.7994, 0.7940,
                0.8003, 0.8184, 0.8005, 0.8154, 0.8093, 0.8235, 0.8225, 0.8039, 0.8153, 0.8251, 0.8188, 0.8229, 0.8320,
                0.8240, 0.8426, 0.8284, 0.8330, 0.8323, 0.8353, 0.8356, 0.8286, 0.8545, 0.8400, 0.8446, 0.8486   
            ],
            borderColor: 'rgba(75, 192, 192, 1)',
            backgroundColor: 'rgba(75, 192, 192, 0.2)',
            fill: true
        },
        {
            label: 'Validation Accuracy',
            data: [
                0.6764, 0.7255, 0.7345, 0.7455, 0.7509, 0.7618, 0.7582, 0.7691, 0.7655, 0.7582, 0.7709, 0.7655,
                0.7618, 0.7691, 0.7764, 0.7691, 0.7727, 0.7691, 0.7782, 0.7800, 0.7782, 0.7782, 0.7818, 0.7764,
                0.7836, 0.7855, 0.7873, 0.7873, 0.7818, 0.7891, 0.7909, 0.7927, 0.7818, 0.7945, 0.7873, 0.7873,
                0.7945, 0.7855, 0.7855, 0.7873, 0.7909, 0.7873, 0.7873, 0.7909, 0.7909, 0.7927, 0.7855, 0.7909    
            ],
            borderColor: 'rgba(255, 99, 132, 1)',
            backgroundColor: 'rgba(255, 99, 132, 0.2)',
            fill: true
        }
    ]
};

// Data for Loss Chart
const lossData = {
    labels: Array.from({ length: 50 }, (_, i) => ` ${i + 1}`),
    datasets: [
        {
            label: 'Training Loss',
            data: [
                1.3033, 0.9115, 0.8216, 0.7245, 0.7166, 0.7007, 0.6626, 0.6777, 0.6690, 0.6514, 0.6070,
                0.6281, 0.6171, 0.6042, 0.5635, 0.5660, 0.5451, 0.5600, 0.5498, 0.5395, 0.5288, 0.5441, 0.5441,
                0.5260, 0.4926, 0.5176, 0.5059, 0.4945, 0.4884, 0.4871, 0.5050, 0.4907, 0.4697, 0.4784, 0.4753, 0.4584,
                0.4605, 0.4359, 0.4679, 0.4363, 0.4321, 0.4477, 0.4360, 0.4420, 0.4087, 0.4269, 0.4185, 0.4267
            ],
            borderColor: 'rgba(54, 162, 235, 1)',
            backgroundColor: 'rgba(54, 162, 235, 0.2)',
            fill: true
        },
        {
            label: 'Validation Loss',
            data: [
                0.9216, 0.8116, 0.7534, 0.7274, 0.7013, 0.6860, 0.6802, 0.6671, 0.6580, 0.6523, 0.6471,
                0.6405, 0.6385, 0.6313, 0.6293, 0.6283, 0.6220, 0.6328, 0.6226, 0.6212, 0.6169, 0.6175, 0.6109,
                0.6107, 0.6061, 0.6083, 0.6046, 0.6063, 0.6082, 0.6025, 0.6071, 0.6046, 0.6088, 0.5999, 0.6030, 0.6030,
                0.6122, 0.6001, 0.6063, 0.6000, 0.6025, 0.5983, 0.6035, 0.6006, 0.6022, 0.6028, 0.6014, 0.6014
          ],
            borderColor: 'rgba(255, 206, 86, 1)',
            backgroundColor: 'rgba(255, 206, 86, 0.2)',
            fill: true
        }
    ]
};

// Data for Evaluation Metrics
const evaluationData = {
    labels: ['Mild', 'Moderate', 'No_DR', 'Proliferate_DR', 'Severe'], // Classes
    datasets: [
        {
            label: 'Precision',
            data: [0.531250, 0.659574, 0.941818, 0.500000, 0.444444], // Precision per class
            backgroundColor: 'rgba(75, 192, 192, 0.2)', // Light green
            borderColor: 'rgba(75, 192, 192, 1)', // Dark green
            borderWidth: 1
        },
        {
            label: 'Recall',
            data: [0.607143, 0.826667, 0.955720, 0.159091, 0.137931], // Recall per class
            backgroundColor: 'rgba(255, 99, 132, 0.2)', // Light red
            borderColor: 'rgba(255, 99, 132, 1)', // Dark red
            borderWidth: 1
        },
        {
            label: 'F1-Score',
            data: [0.566667, 0.733728, 0.948718, 0.241379, 0.210526], // F1-Score per class
            backgroundColor: 'rgba(54, 162, 235, 0.2)', // Light blue
            borderColor: 'rgba(54, 162, 235, 1)', // Dark blue
            borderWidth: 1
        }
    ]
};

// Configuration for the Chart
const config = {
    type: 'bar', // Bar chart
    data: evaluationData,
    options: {
        responsive: true,
        plugins: {
            legend: {
                display: true, // Display legend
                position: 'top' // Legend position
            },
            title: {
                display: true,
                text: 'Precision, Recall, and F1-Score per Class' // Title
            }
        },
        scales: {
            x: {
                stacked: true // Enable stacked bars for better comparison
            },
            y: {
                beginAtZero: true, // Start y-axis at 0
                max: 1 // Maximum value (metrics are in range 0-1)
            }
        }
    }
};

// Render Accuracy Chart
const ctx1 = document.getElementById('accuracyChart').getContext('2d');
new Chart(ctx1, {
    type: 'line',
    data: accuracyData,
    options: {
        responsive: true,
        plugins: {
            legend: {
                position: 'top',
            },
            title: {
                display: true,
                text: 'Training vs Validation Accuracy'
            }
        },
        scales: {
            x: {
                title: {
                    display: true,
                    text: 'Epochs'
                }
            },
            y: {
                title: {
                    display: true,
                    text: 'Accuracy'
                },
                min: 0,     // Ensure minimum y-axis value is 0
                max: 1,     // Ensure maximum y-axis value is 1
            }
        }
    }
});

// Render Loss Chart
const ctx2 = document.getElementById('lossChart').getContext('2d');
new Chart(ctx2, {
    type: 'line',
    data: lossData,
    options: {
        responsive: true,
        plugins: {
            legend: {
                position: 'top',
            },
            title: {
                display: true,
                text: 'Training vs Validation Loss'
            }
        },
        scales: {
            x: {
                title: {
                    display: true,
                    text: 'Epochs'
                }
            },
            y: {
                title: {
                    display: true,
                    text: 'Accuracy'
                },
                min: 0,     // Ensure minimum y-axis value is 0
                max: 1,     // Ensure maximum y-axis value is 1
            }
        }
    }
});

// Render Evaluation Chart
const ctx3 = document.getElementById('evaluationChart').getContext('2d');
new Chart(ctx3, {
    type: 'bar',
    data: evaluationData,
    options: {
        responsive: true,
        plugins: {
            legend: {
                position: 'top',
            },
            title: {
                display: true,
                text: 'Precision, Recall, and F1-Score per Class:'
            }
        }
    }
});
              
