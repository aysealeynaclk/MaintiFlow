import { createRouter, createWebHistory } from 'vue-router'
import { auth } from '../stores/auth'

import Login from '../views/Login.vue'
import RiskListesi from '../views/RiskListesi.vue'
import Detay from '../views/Detay.vue'
import IsEmirleri from '../views/IsEmirleri.vue'
import Profil from '../views/Profil.vue'
import AdminMakineler from '../views/admin/Makineler.vue'
import AdminStok from '../views/admin/Stok.vue'
import AdminLoglar from '../views/admin/Loglar.vue'
import AdminKullanicilar from '../views/admin/Kullanicilar.vue'

const routes = [
  { path: '/login', name: 'login', component: Login, meta: { public: true } },
  { path: '/', name: 'risk-listesi', component: RiskListesi },
  { path: '/tahmin/:id', name: 'detay', component: Detay, props: true },
  { path: '/is-emirleri', name: 'is-emirleri', component: IsEmirleri },
  { path: '/profil', name: 'profil', component: Profil },
  { path: '/admin/makineler', name: 'admin-makineler', component: AdminMakineler, meta: { admin: true } },
  { path: '/admin/stok', name: 'admin-stok', component: AdminStok, meta: { admin: true } },
  { path: '/admin/loglar', name: 'admin-loglar', component: AdminLoglar, meta: { admin: true } },
  { path: '/admin/kullanicilar', name: 'admin-kullanicilar', component: AdminKullanicilar, meta: { admin: true } },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

router.beforeEach((to) => {
  if (!to.meta.public && !auth.isLoggedIn) {
    return { name: 'login', query: { redirect: to.fullPath } }
  }
  if (to.meta.admin && !auth.isAdmin) {
    return { name: 'risk-listesi' }
  }
  if (to.name === 'login' && auth.isLoggedIn) {
    return { name: 'risk-listesi' }
  }
  return true
})

export default router
