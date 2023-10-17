<template>
  <div class="global_wrapper">
    <div class="nav_bar_wrapper">
      <NavBar/>
    </div>
    <div class="body">
      <div class="content">
        <router-view/>
      </div>
      <!-- <div class="weather_wrapper"> -->
        <div class="weather">
          <WeatherSideBar/>
        </div>
      <!-- </div> -->
    </div>

  </div>
</template>

<script>
import NavBar from './components/NavBar.vue'
import WeatherSideBar from './components/WeatherSideBar.vue'
export default {
  name: 'App',
  components: {
    NavBar,
    WeatherSideBar,
  }
}
</script>

<style>
  .global_wrapper{
   padding: 0px; 
   /* width :100vw; */
  }
  .content{
    border: solid black 0px;
  }
  .nav_bar_wrapper{
    position: sticky;
    top: 0px;
    padding-bottom: 40px;
    background-color: white;
    z-index: 1;
  }
  .body{
    display: grid;
    grid-template-columns: 10fr 3fr;
    gap: 30px;
    position: relative;
    justify-content: space-between;
    padding-left: 20px;
  }
  /* .weather_wrapper{
    border: solid black 1px;
    position: relative;
    width: 700px;
  } */
  .weather{
    position: fixed;
    right: 30px;
    width: 400px;
    justify-content: space-around;
  }
</style>
