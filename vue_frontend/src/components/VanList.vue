<template>
	<div class="wrapper">
		<div class="parcel">
			<RouterLink to="/" style="display: flex; gap: 20px;">
				<i class="fas fa-3x fa-arrow-left" style="color: white;"></i>
				<h1 style="color: white;">{{this.parcel.name}}</h1>
			</RouterLink>
			<p style="color: white;">{{this.parcel.location}} • {{this.parcel.surface}} Hectare</p>
			<!-- Button trigger modal -->
			<div class="actions" style="display: flex; gap: 10px; justify-content: end;">
				<button class="btn btn-success" data-mdb-toggle="modal" data-mdb-target="#add_van_modal">Add Sector <i class="fas ms-2 fa-circle-plus"></i></button>
				<button class="btn btn-info" data-mdb-toggle="modal" data-mdb-target="#edit_modal">Edit Parcel <i class="fas ms-2 fa-pen"></i></button>
				<button class="btn btn-danger" data-mdb-toggle="modal" data-mdb-target="#delete_modal">Delete parcel <i class="far ms-2 fa-trash-can "></i></button>
			</div>
			<!-- add van Modal -->
			<div class="edit_modal modal fade" id="add_van_modal" data-mdb-keyboard="true" tabindex="-1" aria-labelledby="staticBackdropLabel" aria-hidden="true">
				<div class="modal-dialog">
					<div class="modal-content">
					<div class="modal-header">
						<h5 class="modal-title" id="staticBackdropLabel">Add Sector</h5>
						<button type="button" class="btn-close" data-mdb-dismiss="modal" aria-label="Close"></button>
					</div>
					<div class="modal-body">
						<div class="form-group">
							<label for="name">Sector name</label>
							<input type="text" required v-model="this.add_van_data.name" id="name" class="form-control" >
						</div>
						<div class="form-group">
							<label for="location">Device ID (TTN)</label>
							<input type="text" required v-model="this.add_van_data.device_id" id="location" class="form-control">
						</div>
					</div>
					<div class="modal-footer">
						<button type="button" class="btn btn-secondary" data-mdb-dismiss="modal">Close</button>
						<button type="button" @click="handleAddVan" data-mdb-dismiss="modal" class="btn btn-primary">Add</button>
					</div>
					</div>
				</div>
			</div>
			<!-- add van Modal -->
			<!-- edit Modal -->
			<div class="edit_modal modal fade" id="edit_modal" data-mdb-keyboard="true" tabindex="-1" aria-labelledby="staticBackdropLabel" aria-hidden="true">
				<div class="modal-dialog">
					<div class="modal-content">
					<div class="modal-header">
						<h5 class="modal-title" id="staticBackdropLabel">Edit Parcel</h5>
						<button type="button" class="btn-close" data-mdb-dismiss="modal" aria-label="Close"></button>
					</div>
					<div class="modal-body">
						<div class="form-group">
							<label for="name">Parcel name</label>
							<input type="text" required v-model="this.parcel.name" id="name" class="form-control" >
						</div>
						<div class="form-group">
							<label for="location">Parcel location</label>
							<input type="text" required v-model="this.parcel.location" id="location" class="form-control">
						</div>
						<div class="form-group">
							<label for="suface">Parcel surface</label>
							<input type="number" required min="0" v-model="this.parcel.surface" id="surface" class="form-control">
						</div>
					</div>
					<div class="modal-footer">
						<button type="button" class="btn btn-secondary" data-mdb-dismiss="modal">Close</button>
						<button type="button" @click="handleEditParcel" data-mdb-dismiss="modal" class="btn btn-primary">Edit</button>
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
						Are you sure you want to delete {{ this.parcel.name }}
					</div>
					<div class="modal-footer">
						<button type="button" class="btn btn-secondary" data-mdb-dismiss="modal">Close</button>
						<button type="button" @click="handleDeleteParcel" data-mdb-dismiss="modal" class="btn btn-danger">Delete</button>
					</div>
					</div>
				</div>
			</div>
			<!-- delete Modal -->
		</div>
		<div class="van_list">
			<VanCard v-for="van in vans" :key="van.id" :van_data="van"/>
			<div class="add_van_card" data-mdb-toggle="modal" data-mdb-target="#add_van_modal">
				<div class="add">
					<img src="@/assets/add.png" >
					<h4>Add Sector</h4>
				</div>
			</div>
		</div>
	</div>
</template>

<script>
import axios from 'axios'
import VanCard from './VanCard.vue'
export default {
	name: 'VanList',
	components:{
		VanCard
	},
	data(){
		return {
			parcel_id : null,
			parcel:{},
			vans :[],
			add_van_data : {
				name:"",
				davice_id:"",
			}
		}
	},
	created(){
		this.parcel_id = this.$route.params.parcel_id
	},
	mounted(){
		axios.get(`http://127.0.0.1:5000/get_van_list?id=${this.parcel_id}`).then((res)=>{
			this.parcel = res.data.parcel
			this.vans = res.data.vans
		})
		if (this.parcel_id){
			window.setInterval(()=>{
				axios.get(`http://127.0.0.1:5000/get_van_list?id=${this.parcel_id}`).then((res)=>{
					this.vans = res.data.vans
				})
			}, 1000)
		}
	},
	methods:{
        handleEditParcel(){
            axios.post("http://127.0.0.1:5000/edit_parcel",{"parcel":this.parcel})
        },
        handleDeleteParcel(){
            axios.post("http://127.0.0.1:5000/delete_parcel",{"id":this.parcel.id})
			this.$router.push('/')
        },
        handleAddVan(){
            axios.post("http://127.0.0.1:5000/add_van",{"parcel_id":this.parcel_id, "van":this.add_van_data})
        }
    }
}
</script>

<style scoped>
	.wrapper{
		display: grid;
		margin-bottom: 30px;

	}
	.parcel{
		display: grid;
		grid-template-columns: 3fr 1fr 3fr;
		align-items:center;
		padding:5px 20px;
		margin-bottom: 30px;
		justify-items: space-between;
		background-color: #5d838d;
		border-radius: 40px;
	}
	.actions{
		align-items: left;
	}
	.parcel p, .parcel h1{
		margin-bottom: 0px;
	}
	.van_list{
		display: flex;
		gap: 45px;
		flex-wrap: wrap;
		justify-content: center;
		padding: 20px 20px;
		background-color: #dedede;
		border-radius: 30px;
	}
	.add_van_card{
		/* background-color: rgba(0, 255, 0, .2); */
		width: 300px;
		height: 300px;
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

