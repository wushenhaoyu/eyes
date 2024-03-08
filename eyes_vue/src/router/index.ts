import { createRouter, createWebHistory } from 'vue-router'
import index from '../views/index.vue'
import login from '../views/login.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path:'/',
      component:login,
      children:[
      ]
    },
    {
      path:'/index',
      component:index,
      children:[
        
      ]
    }
  ]
})

export default router
