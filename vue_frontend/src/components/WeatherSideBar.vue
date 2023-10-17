<template>
    <div class="wrapper">
        <TemperatureChart/>
        <HumidityChart/>
    </div>
  </template>
  
  <script>
    import TemperatureChart from './charts/TemperatureChart.vue';
    import HumidityChart from './charts/HumidityChart.vue';
    export default {
        name: 'App',
        components:{
            TemperatureChart,
            HumidityChart
        },
      
       
        
    }
  </script>
  
  <style scoped>
    .wrapper{
        display: flex;
        flex-direction: column;
        gap: 30px;
        
    }
    .wrapper div{
        height: calc((100vh - 170px - 30px)/2);
        /* border-radius: 20px; */
    }
  </style>
  