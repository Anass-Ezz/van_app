<template>
	<div class="wrapper">
        <div class="last_mesurment">
            <h1>Last mesurment</h1>
            <h5>Flow rate</h5>
            <img class="icon" src="@/assets/flow_icon.png" style="width: 100px;">
            <h2>{{ this.last_mesurment.value }}<span style="font-size: 40px;">L/min</span></h2>
            <p>{{ this.last_mesurment.time }}</p>
        </div>
        <div class="chart_wrapper">
            <div style="display: flex; justify-content: space-between; padding: 0px 30px; padding-top: 10px; align-items: center;">
                <h4><img src="@/assets/flow_icon.png" width="50px">Last day mesurments</h4>
                <h5>Flow rate</h5>
            </div>
            <div class="chart"> 
                <canvas id="flw_chart" style="padding: 0px; margin: 0px;"></canvas>
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
            last_mesurment : {}
		}
	},
    props:{
        flow_values:Object
    },
    mounted(){
        console.log(this.flow_values)
        var data = {
            labels: ["ds", "dsse", "oiz", "zep"],
            datasets: [
            {
                label: "Humidity",
                data: [79, 82, 27, 67],
                backgroundColor: "rgba(23,163,93,.5)",
                borderColor: "#2B682A",
                borderWidth: 3,
                fill: true,
            },
            ]
        }
        const ctx = document.getElementById('flw_chart');
        var flw_chart = new Chart(ctx, {
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
                scales:{
                    x: {
                        display: false
                    }
                }
            },
        });
        window.setInterval(()=>{
            if (this.flow_values){
                data.datasets[0].data = this.flow_values.values
                data.labels = this.flow_values.time
                flw_chart.update()
                this.last_mesurment = {time:this.flow_values.time.slice(-1)[0], value:this.flow_values.values.slice(-1)[0]}
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
    /* .icon{
        width: 100px;
    } */
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

