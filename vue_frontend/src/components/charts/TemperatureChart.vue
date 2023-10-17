<template>
    <div class="wrapper" >
        <h3 >Temperature</h3>
        <h1 style="font-size: 76px;">{{ this.current_temp }}°C</h1>
        <div>
            <canvas id="temp_chart"></canvas>
        </div>
    </div>
  </template>
  
  <script>
    import Chart from 'chart.js/auto' 
    import axios from 'axios'
    export default {
        name: 'TemperatureChart',
        data(){
            return {
                current_temp: 30,
            }
        },
        mounted(){
            console.log(this.temperature) 
            var data = {
                labels: ["ds", "dsse", "oiz", "zep"],
                datasets: [
                    {
                        label: "Temperature",
                        data: [79, 82, 27, 67],
                        backgroundColor: "rgba(108, 221, 193, 1)",
                        borderColor: "#36495d",
                        borderWidth: 0,
                    },
                ]
            }
            const ctx = document.getElementById('temp_chart');
            var TempChart = new Chart(ctx, {
                type: 'bar',
                data: data,
                options: {
                    borderRadius:40,
                    responsive: true,
                    scales: {
                        
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
                            left:20,
                            up:20,
                            right:20
                        }
                    }
                },
            });
            window.setInterval(()=>{
                axios.get("https://api.open-meteo.com/v1/forecast?latitude=32.210972&longitude=-7.929902&current_weather=true&hourly=temperature_2m,relativehumidity_2m").then((res)=>{
                    let current_time = res.data.current_weather.time
                    let time_index = res.data.hourly.time.indexOf(current_time)
                    data.labels = res.data.hourly.time.slice(time_index+1, time_index+10)
                    data.datasets[0].data = res.data.hourly.temperature_2m.slice(time_index+1, time_index+10)
                    this.current_temp = res.data.current_weather.temperature
                    TempChart.update()
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
        /* background-color: rgba(108, 221, 193, 0.3); */
        background-color: rgba(66, 220, 182, 0.3);
    }
</style>