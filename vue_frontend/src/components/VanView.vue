<template>
	<div class="wrapper">
		<div class="van_info" style="display: flex; gap: 30px; align-items: start;">
				<RouterLink :to="{ path: `/VanList/${this.van_data.parcel_id}`}" style="display: flex; gap: 20px;">
					<i class="fas fa-3x fa-arrow-left" style="color: black;" ></i>
				</RouterLink>
				<div>
					<h2>{{this.van_data.name}}</h2>
					<p>{{this.van_data.device_id}}</p>
				</div>
		</div>
		<div class="actions" style="display: flex; gap: 30px; justify-content: end; align-items: center;">
			<button class="btn btn-info" data-mdb-toggle="modal" data-mdb-target="#edit_modal">Edit Sector <i class="fas ms-2 fa-pen"></i></button>
			<button class="btn btn-danger" data-mdb-toggle="modal" data-mdb-target="#delete_modal">Delete Sector <i class="far ms-2 fa-trash-can "></i></button>
			<div class="form-check form-switch" style="display: flex; justify-content: end;">
				<input class="form-check-input" style="transform: scale(2)" @change="handleChange" type="checkbox" v-model="van_data.com_state" :checked="com_state" role="switch" id="flexSwitchCheckDefault">
			</div>
		</div>
		<!-- edit Modal -->
		<div class="edit_modal modal fade" id="edit_modal" data-mdb-keyboard="true" tabindex="-1" aria-labelledby="staticBackdropLabel" aria-hidden="true">
				<div class="modal-dialog">
					<div class="modal-content">
					<div class="modal-header">
						<h5 class="modal-title" id="staticBackdropLabel">Edit Van</h5>
						<button type="button" class="btn-close" data-mdb-dismiss="modal" aria-label="Close"></button>
					</div>
					<div class="modal-body">
						<div class="form-group">
							<label for="name">Parcel name</label>
							<input type="text" required v-model="this.van_data.name" id="name" class="form-control" >
						</div>
						<div class="form-group">
							<label for="location">Parcel location</label>
							<input type="text" required v-model="this.van_data.device_id" id="location" class="form-control">
						</div>
					</div>
					<div class="modal-footer">
						<button type="button" class="btn btn-secondary" data-mdb-dismiss="modal">Close</button>
						<button type="button" @click="handleEditVan" data-mdb-dismiss="modal" class="btn btn-primary">Edit</button>
					</div>
					</div> 
				</div>
			</div>
			<!-- edit Modal -->
			<!-- delete Modal -->
			<div class="delete_modal modal fade" id="delete_modal" data-mdb-keyboard="true" tabindex="-1" aria-labelledby="staticBackdropLabel" aria-hidden="true">
				<div class="modal-dialog">
					<div class="modal-content">
					<div class="modal-body">
						Are you sure you want to delete {{ this.van_data.name }}
					</div>
					<div class="modal-footer">
						<button type="button" class="btn btn-secondary" data-mdb-dismiss="modal">Close</button>
						<button type="button" @click="handleDeleteVan" data-mdb-dismiss="modal" class="btn btn-danger">Delete</button>
					</div>
					</div>
				</div>
			</div>
			<!-- delete Modal -->
		<div class="tabs">
			<div class="tab" :class="selected_tab=='Temperature' ? 'active' : ''" @click="handleTab('Temperature')">Temperature</div>
			<div class="tab" :class="selected_tab=='Humidity' ? 'active' : ''" @click="handleTab('Humidity')">Humidity</div>
			<div class="tab" :class="selected_tab=='Conductivity' ? 'active' : ''" @click="handleTab('Conductivity')">Conductivity</div>
			<div class="tab" :class="selected_tab=='Flow' ? 'active' : ''" @click="handleTab('Flow')">Flow</div>
		</div>
		<div class="tab_content">
			<div  :class="selected_tab=='Temperature' ? 'active_content' : 'hidden_content'">
				<TemperatureValues/>
			</div>
			<div  :class="selected_tab=='Humidity' ? 'active_content' : 'hidden_content'">
				<HumidityValues/>
			</div>
			<div  :class="selected_tab=='Conductivity' ? 'active_content' : 'hidden_content'">
				<ConductivityValues/>
			</div>
			<div  :class="selected_tab=='Flow' ? 'active_content' : 'hidden_content'">
				<FlowValues :flow_values = "flow_values"/>
			</div>
		</div>
	</div>
</template>

<script>
import FlowValues from './van_values/FlowValues.vue'
import HumidityValues from './van_values/HumidityValues.vue'
import TemperatureValues from './van_values/TemperatureValues.vue'
import ConductivityValues from './van_values/ConductivityValues.vue'
import axios from 'axios'
export default {
	name: 'VanView',
	data(){
		return {
			van_id:null,
			van_data:{},
            selected_tab : "Flow",
			flow_values:{},
			temperature_values:{},
			humidity_values:{},
			conductivity_values:{},
		}
	},
	components:{
		FlowValues,
		HumidityValues,
		TemperatureValues,
		ConductivityValues
	},
    created(){
		this.van_id = this.$route.params.van_id
    },
	mounted(){
		axios.get(`http://127.0.0.1:5000/get_van_data?id=${this.van_id}`).then((res)=>{
			this.flow_values=res.data.flow_values
			this.van_data=res.data.van
			// this.temperature_alues=res.data,
			// this.humidity_alues=res.data,
			// this.conductivity_alues=res.data,
		})
		window.setInterval(()=>{
			axios.get(`http://127.0.0.1:5000/get_van_data?id=${this.van_id}`).then((res)=>{
				this.flow_values=res.data.flow_values
			})
		}, 1000)
	},
	methods:{
		handleTab(tab){
			this.selected_tab = tab
		},
		handleChange(){
            axios.post("http://127.0.0.1:5000/post_new_state",{"id":this.van_data.id, "state":this.van_data.com_state})
        },
		handleEditVan(){
            axios.post("http://127.0.0.1:5000/edit_van", this.van_data)
        },
        handleDeleteVan(){
            axios.post("http://127.0.0.1:5000/delete_van", {"id":this.van_data.id})
			this.$router.push(`/VanList/${this.van_data.parcel_id}`)
        },
	}
}
</script>

<style scoped>
	.wrapper{
		border-radius: 30px;
		display: grid;
		grid-template-columns: 1fr 2fr;
		grid-template-rows: 1fr 1fr 5fr;
		gap: 10px;
		justify-content: space-around;
		background-color: #F0F0F0;
		padding: 30px;
		align-items: start;
	}
	.tabs{
		grid-column: 1/3;
		grid-row: 2/3;
		display: flex;
		background-color: #D9D9D9;
		justify-content: space-around;
		gap: 50px;
		align-items: center;
		border-radius: 20px;
		/* width: fit-content; */
		padding: 0px 25px;
		margin: 0 auto;
		height: 100px;
		width: 100%;
		
	}
	.tab{
		/* background-color: #E8E8E8; */
		padding: 10px 20px;
		border-radius: 10px;
		width: 200px;
		text-align: center;
		margin: 20px 0px;
		font-size: 20px;
	}
	.tab:hover{
		background-color: #a0c09f;
		color: white;
		cursor: pointer;
	}
	.tab_content{
		width: 100%;
		grid-column: 1/3;
	}
	.active_content{
		display:grid;
	}
	.hidden_content{
		
		display: none;
	}
	.active{
		background-color: #a0c09f;
		color: white;
	}

</style>

