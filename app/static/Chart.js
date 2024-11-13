<canvas id="lessonsChart"></canvas>
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<script>
    var ctx = document.getElementById('lessonsChart').getContext('2d');
    var lessonsChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ['Planning', 'Execution', 'Closing'],
            datasets: [{
                label: 'Lessons Learned per Project Phase',
                data: [10, 20, 5],
            }]
        }
    });
</script>
