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
