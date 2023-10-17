import { createRouter, createWebHistory } from 'vue-router'
import ParcelList from '../components/ParcelList.vue'
import VanList from '../components/VanList.vue'
import VanView from '../components/VanView.vue'


const router = createRouter({
    history: createWebHistory(),
    routes:[
        {
            path : "/",
            name:"ParcelList",
            component:ParcelList
        },
        {
            path : "/VanList/:parcel_id",
            name: "VanList",
            component: VanList,
        },
        {
            path : "/Van/:van_id",
            name: "Van",
            component: VanView
        },
    ]
        
})

export default router