<?php
$con=mysqlI_connect("localhost","root","","oil_price_chart");
mysqli_query($con,"SET NAMES utf8");
$result=mysqli_query($con,"SELECT * FROM `oil_price_chart` ORDER BY date");
$num = mysqli_num_rows($result);
if ($result) {
        $dates = array();
        $prices = array();
        while ($row = mysqli_fetch_assoc($result)) {
            $dates[]  = $row["date"];
            $prices[] = $row["price"];
        }
    }
mysqli_free_result($result);
mysqli_close($con);

$output=exec('python oil_price_chart.py');

?>
<html>
    <head>
        <meta charset="UTF-8" />
    </head>
    <body>
        <canvas id="myChart" width="300" height="200"></canvas>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/2.7.2/Chart.min.js"></script>
        </script>
        <script>
            var ctx = document.getElementById('myChart');
            var myChart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: <?=json_encode($dates);?>,
                datasets: [{
                        label: '柴油歷年價格',
                        data: <?=json_encode($prices);?>,
                        }]
            }
            });
        </script>
    </body>
</html>
