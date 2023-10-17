<template>
    <div class="wrapper" >
        <h3 >Humidity</h3>
        <h1 style="font-size: 76px;">{{ this.current_hum }}%</h1>
        <div >
            <canvas id="hum_chart"></canvas>
        </div>
    </div>
  </template>
  
<script>
    import Chart from 'chart.js/auto' 
    import axios from 'axios'   
    export default {
        name: 'HumidityChart',
        data(){
            return {
                current_hum: 30,
            }
        },
        mounted(){
            var data = {
                labels: ["ds", "dsse", "oiz", "zep"],
                datasets: [
                {
                    label: "Humidity",
                    data: [79, 82, 27, 67],
                    backgroundColor: "rgba(54,73,93,.5)",
                    borderColor: "#36495d",
                    borderWidth: 3,
                    // fill: true,
                },
                ]
            }
            const ctx = document.getElementById('hum_chart');
            var HumChart = new Chart(ctx, {
                type: 'line',
                data: data,
                options: {

                    borderRadius:40,
                    responsive: true,
                    lineTension: .4,
                
                    scales: {
                        yAxes: [{
                            gridLines: {
                                drawBorder: false,
                                display:false,
                            },
                        }],
                        x: {
                            display:false,
                            
                        },
                        y: {
                            display:false,
                            
                        }
                    },
                    maintainAspectRatio: false,
                    plugins:{
                        legend: {
                            display: false
                        },
                    },
                    layout: {
                        padding: {
                            // left:20,
                            up:20,
                            // right:20
                        }
                    }
                },
            });
            window.setInterval(()=>{
                axios.get("https://api.open-meteo.com/v1/forecast?latitude=32.210972&longitude=-7.929902&current_weather=true&hourly=temperature_2m,relativehumidity_2m").then((res)=>{
                    let current_time = res.data.current_weather.time
                    let time_index = res.data.hourly.time.indexOf(current_time)
                    data.labels = res.data.hourly.time.slice(time_index+1, time_index+10)
                    data.datasets[0].data = res.data.hourly.relativehumidity_2m.slice(time_index+1, time_index+10)
                    this.current_hum = res.data.hourly.relativehumidity_2m[time_index]
                    HumChart.update()
                })
                
            }, 500)

        }
    }
</script>

<style scoped>
    .wrapper{
        border-radius: 20px; 
        text-align: center; 
        display: flex; 
        justify-content: end;
        flex-direction: column;  
        background-color: rgba(65, 120, 221, 0.3);
    }
</style>