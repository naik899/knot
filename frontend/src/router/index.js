import { createRouter, createWebHistory } from 'vue-router'
import DashboardView from '../views/DashboardView.vue'
import QueryView from '../views/QueryView.vue'
import FTOView from '../views/FTOView.vue'
import CorporateView from '../views/CorporateView.vue'
import LandscapeView from '../views/LandscapeView.vue'
import PatentsView from '../views/PatentsView.vue'
import ValidityView from '../views/ValidityView.vue'

const routes = [
  { path: '/', name: 'dashboard', component: DashboardView },
  { path: '/query', name: 'query', component: QueryView },
  { path: '/fto', name: 'fto', component: FTOView },
  { path: '/corporate', name: 'corporate', component: CorporateView },
  { path: '/landscape', name: 'landscape', component: LandscapeView },
  { path: '/patents', name: 'patents', component: PatentsView },
  { path: '/validity', name: 'validity', component: ValidityView },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router
