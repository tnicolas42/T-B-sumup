import Vue from 'vue'
import VueRouter from 'vue-router'
import Home from '../views/Home.vue'
import ProduitsSem from '../views/ProduitsSem.vue'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/produits_sem',
    name: 'Produits par semaine',
    component: ProduitsSem
  },
  {
    path: '/stats_date',
    name: 'Stats',
    component: () => import('../views/StatsDate.vue')
  },
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router
