import { createRouter, createWebHistory } from 'vue-router'
import Laboratory from '../components/Laboratory.vue'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Laboratory
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router 