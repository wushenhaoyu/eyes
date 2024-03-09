import { createRouter, createWebHistory } from 'vue-router'
import index from '../views/index.vue'
import login from '../views/login.vue'
import patient1View from '../views/patient1View.vue'
import patient2View from '@/views/patient2View.vue'

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
        {
          path:'/patient1',
          component:patient1View
        },
        {
          path:'/patient2',
          component:patient2View
        }

      ]
    }
  ]
})

export default router
