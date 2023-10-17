<template>
	<div class="nav_bar">
		<RouterLink :to="{ path: '/'}" class="logo" >
			<img src="@/assets/logo.webp" alt="">
		</RouterLink>
		<div class="account">
			
			<div class="profile_photo" >
				<img width="60px" src="@/assets/profile_photo.webp" >
			</div>

			<h4 class="profile_name">Anas BELKADI</h4>
			<div class="dots">
				<img width="40px" src="@/assets/dots.webp" >
			</div>
		</div>
	</div>
</template>

<script>
export default {
	name: 'NavBar',
}
</script>

<style>
	.nav_bar{
		display: flex;
		justify-content: space-between;
		height: 100px;
		align-items: center;
		/* background-color: rgb(243, 243, 243); */
		padding: 0px 30px ;
		padding-top: 5px;
	}
	.account{
		display: flex;
		justify-content: space-between;
		align-items: center;
		gap: 20px;
	}
	.profile_photo img{
		width: 60px;
		height: 60px;
		object-fit: cover;
		border-radius: 100%;
	}
	.logo img{
		width: 150px;
	}


</style>

