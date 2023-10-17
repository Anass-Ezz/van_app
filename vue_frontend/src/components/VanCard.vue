<template>
    <div class="van_card" :style='{"background-color":van_data.rec_state ? "rgba(79, 163, 89, 1)" : "grey"}'>
        <RouterLink :to="{ path: `/Van/${this.van_data.id}`}" style="font-size: 30px; color: rgba(44, 44, 44, 0.8);">{{ this.van_data.name }}</RouterLink>
        <p>{{ this.van_data.device_id }}</p>
        <div class="feed_data">
            <div class="flow">
                <h5>Flow</h5>
                <p>{{ this.van_data.flow }} <span style="color: rgba(0, 0, 0, 0.8);">L/min</span></p>
            </div>
            <div class="quantity">
                <h5>Quantity</h5>
                <p>{{ this.van_data.quantity }} <span style="color: rgba(0, 0, 0, 0.8);">m<sup>3</sup></span></p>
            </div>
            <div class="battery">
                <h5>Battery</h5>
                <p>{{ this.van_data.battery }} <span style="color: rgba(0, 0, 0, 0.8);">V</span></p>
            </div>
        </div>
        <div class="form-check form-switch" style="display: flex; justify-content: space-around;">
            <input class="form-check-input" style="transform: scale(2)" @change="handleChange" type="checkbox" v-model="com_state" :checked="com_state" role="switch" id="flexSwitchCheckDefault">
        </div>
    </div>
</template>

<script>
import axios from 'axios'
export default {
	name: 'VanCard',
	data(){
		return {
			com_state:this.van_data.com_state
		}
	},
    props:{
        van_data : Object
    },
    methods:{
        handleChange(){
            console.log(this.com_state)
            axios.post("http://127.0.0.1:5000/post_new_state",{"id":this.van_data.id, "state":this.com_state})
        }
    }
}
</script>

<style scoped>
    .van_card{
        background-color: #F0F0F0;
        color: white;
        width: 300px;
        height: 300px;
        border-radius:20px ;
        text-align: center;
        display: grid;
        grid-template-rows: 2fr 1fr 3fr 2fr;
        align-items: center;
    }
    .feed_data{
        display: flex;
        flex-direction: row;
        justify-content: space-around;
    }
</style>

