<template>
	<div class="wrapper">
        <div class="last_mesurment">
            <h1>Last mesurment</h1>
            <h5>Temperature</h5>
            <img src="@/assets/temperature_icon.png" style="width: 100px;">
            <h2>30<span style="font-size: 40px;">°C</span> </h2>
            <p>9:30pm</p>
        </div>
        <div class="chart_wrapper">
            <div style="display: flex; justify-content: space-between; padding: 0px 30px; padding-top: 10px; align-items: center;">
                <h4><img src="@/assets/temperature_icon.png" width="50px">Last day mesurments</h4>
                <h5>Temperature</h5>
            </div>
            <div class="chart"> 
                <canvas id="temp_chart" style="padding: 0px; margin: 0px;"></canvas>
            </div>
        </div>
	</div>
</template>

<script>
import Chart from 'chart.js/auto' 
export default {
	name: 'FlowValues',
	data(){
		return {
            van_id : null
		}
	},
    props:{
        temperature_values:Object
    },
    mounted(){
        var data = {
            labels: ["13:30", "16:00", "16:30", "15:00"],
            datasets: [
            {
                label: "Humidity",
                data: [29.5, 30.3, 30.1, 28.2],
                backgroundColor: "rgba(167, 0, 0, 0.5)",
                borderColor: "#ef4e52",
                borderWidth: 3,
                fill: true,
            },
            ]
        }
        const ctx = document.getElementById('temp_chart');
        var temp_chart = new Chart(ctx, {
            type: 'line',
            data: data,
            options: {
                borderRadius:40,
                responsive: true,
                lineTension: .4,
                maintainAspectRatio: false,
                plugins:{
                    legend: {
                        display: false
                    },
                },
          
            },
        });
        window.setInterval(()=>{
            if (this.temperature_values){
                data.datasets[0].data = this.temperature_values.values
                data.labels = this.temperature_values.time
                temp_chart.update()
            }
		}, 500)
    }
}
</script>

<style scoped>
       .wrapper{
        display: flex;
        width: 100%;
        height: 300px;
    }
	.chart{
        display: grid;
        padding: 10px;
        height: 400px;
    }
    .chart_wrapper{
        background-color: #D9D9D9;
        border-radius: 20px;
        height: 460px;
    }
    .last_mesurment{
        display: flex;
        flex-direction: column;
        background-color: #D9D9D9;
        align-items: center;
        justify-content: space-around;
        border-radius: 20px;
        padding: 10px;
        height: 100%;
    }
    .last_mesurment h2{
        font-size: 80px;
    }
    .last_mesurment p{
        font-size: 20px;
        background-color: #E8E8E8;
        padding: 10px 20px;
        border-radius: 10px;
    }
    span{
        color: rgb(44, 161, 161);
    }
</style>

