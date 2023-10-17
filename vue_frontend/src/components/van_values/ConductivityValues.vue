<template>
	<div class="wrapper">
        <div class="last_mesurment">
            <h1>Last mesurment</h1>
            <h5>Conductivity</h5>
            <img src="@/assets/conductivity_icon.png" style="width: 100px;">
            <h2>30<span style="font-size: 40px;">%</span></h2>
            <p>9:30pm</p>
        </div>
        <div class="chart_wrapper">
            <div style="display: flex; justify-content: space-between; padding: 0px 30px; padding-top: 10px; align-items: center;">
                <h4><img src="@/assets/conductivity_icon.png" width="50px">Last day mesurments</h4>
                <h5>Conductivity</h5>
            </div>
            <div class="chart"> 
                <canvas id="cond_chart" style="padding: 0px; margin: 0px;"></canvas>
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
        conductivity_values:Object
    },
    mounted(){
        var data = {
            labels: ["13:30", "16:00", "16:30", "15:00"],
            datasets: [
            {
                label: "Humidity",
                data: [1.25, 1.28, 1.30, 1.27],
                backgroundColor: "rgba(0, 152, 166, 0.5)",
                borderColor: "#4eefeb",
                borderWidth: 3,
                fill: true,
            },
            ]
        }
        const ctx = document.getElementById('cond_chart');
        var cond_chart = new Chart(ctx, {
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
                // layout: {
                //     padding: {
                //         // left:20,
                //         up:20,
                //         // right:20
                //     }
                // }
            },
        });
        window.setInterval(()=>{
            if (this.conductivity_values){
                data.datasets[0].data = this.conductivity_values.values
                data.labels = this.conductivity_values.time
                cond_chart.update()
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

