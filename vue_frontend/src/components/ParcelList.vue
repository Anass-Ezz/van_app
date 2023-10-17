<template>
	<div class="wrapper">
		<div class="parcel_list">
			<RouterLink  v-for="parcel in parcels" :key="parcel.id" :to="{ path: `/VanList/${ parcel.id }`}" class="parcel_card">
				<h4 class="parcel_id">{{ parcel.location }}</h4>		
				<h6 class="parcel_location">ID {{ parcel.id }}</h6>		
				<h1 class="parcel_name">{{ parcel.name }}</h1>		
				<div class="info_wrapper">
					<img class="on" src="@/assets/on.gif" >
					<p class="on_vans">{{ parcel.states.on }}</p>
					<img class="off" src="@/assets/off.png" >
					<p class="off_vans">{{ parcel.states.off }}</p>
					<h5 class="quantity">{{ parcel.surface }} <span style="font-weight: lighter;" v-if="parcel.surface<=1">Hectare</span><span v-else style="font-weight: lighter;">Hectares</span></h5>
				</div>		
			</RouterLink>
			<!-- Button trigger modal -->
			<div class="add_parcel_card" data-mdb-toggle="modal" data-mdb-target="#staticBackdrop">
				<div class="add">
					<img src="@/assets/add.png" >
					<h4>Add Parcel</h4>
				</div>
			</div>
			<!-- Modal -->
			<div
			class="modal fade"
			id="staticBackdrop"
			data-mdb-keyboard="true"
			tabindex="-1"
			aria-labelledby="staticBackdropLabel"
			aria-hidden="true"
			>
			<div class="modal-dialog">
				<div class="modal-content">
				<div class="modal-header">
					<h5 class="modal-title" id="staticBackdropLabel">Add Parcel</h5>
					<button type="button" class="btn-close" data-mdb-dismiss="modal" aria-label="Close"></button>
				</div>
				<div class="modal-body">
					<div class="form-group">
						<label for="name">Parcel name</label>
						<input type="text" required v-model="this.add_parcel_data.name" id="name" class="form-control" >
					</div>
					<div class="form-group">
						<label for="location">Parcel location</label>
						<input type="text" required v-model="this.add_parcel_data.location" id="location" class="form-control">
					</div>
					<div class="form-group">
						<label for="suface">Parcel surface</label>
						<input type="number" required min="0" v-model="this.add_parcel_data.surface" id="surface" class="form-control">
					</div>
				</div>
				<div class="modal-footer">
					<button type="button" class="btn btn-secondary" data-mdb-dismiss="modal">Close</button>
					<button type="button" @click="handleAddParcel" data-mdb-dismiss="modal" class="btn btn-primary">Add</button>
				</div>
				</div>
			</div>
			</div>
		</div>
	</div>
</template>

<script>
import axios from 'axios'
export default {
	name: 'ParcelList',
	data(){
		return {
			parcels: [],
			add_parcel_data : {
				name:"ds",
				location:"ds",
				surface:"3"
			}
		}
	},
	mounted(){
		axios.get("http://127.0.0.1:5000/get_parcel_list").then((res)=>{
			this.parcels = res.data
		})
		setInterval(()=> {
			axios.get("http://127.0.0.1:5000/get_parcel_list").then((res)=>{
				this.parcels = res.data
			})
		}, 500);
	},
	methods:{
		handleAddParcel(){
			axios.post("http://127.0.0.1:5000/add_parcel", this.add_parcel_data).then((res)=>{
				console.log(res)
			})
		}
	}
}
</script>

<style scoped>
	.wrapper{
		display: grid;
		margin-bottom: 30px;
	}
	.parcel_list{
		display: flex;
		/* justify-content:space-between; */
		gap: 50px;
		flex-wrap: wrap;
	}
	.parcel_card{
		background-color: #dfdfdf;
		width: 300px;
		height: 500px;
		border-radius:20px ;
		text-align: center;
		display: grid;
		grid-template-rows: 1fr 1fr 4fr 2fr;
		align-items: center;
	}
	.parcel_id{
		color: black;
	}
	.parcel_location{
		color: grey;
	}
	.parcel_name{
		color: rgb(28, 110, 83);


	}
	.info_wrapper{
		display: grid;
		grid-template-rows: 1fr 1fr;
		grid-template-columns: 1fr 1fr 1fr 1fr;
		/* gap: 30px; */
		align-items: center;
		justify-content: space-evenly;
	}
	.info_wrapper p{
		margin: 0 auto;
		margin-left: 0px;
		font-size: 20px;
		color: rgb(82, 82, 82);
	}
	.on{
		width: 50px;
		margin-left: 30px;
	}
	.off{
		width: 25px;
		margin-left: 30px;
	}
	h5{
		grid-column: 1/5;
		color: rgb(59, 139, 139);
	}
	.add_parcel_card{
		/* background-color: rgba(0, 255, 0, .2); */
		width: 300px;
		height: 500px;
		border-radius:20px ;
		border: dashed green 2px;
		text-align: center;
		display: flex;
		flex-direction: column;
		justify-content: center;
	}
	.add img{
		width: 70px;
		color: rgba(0, 255, 0, .2);
	}
	.add h4{
		color: rgb(64, 133, 92);
	}

</style>

