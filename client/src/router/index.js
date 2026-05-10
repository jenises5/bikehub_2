import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

import LandingPage       from '@/pages/LandingPage.vue'
import CatalogPage       from '@/pages/CatalogPage.vue'
import LoginPage         from '@/pages/LoginPage.vue'
import RegisterPage      from '@/pages/RegisterPage.vue'
import ProductDetailPage from '@/pages/ProductDetailPage.vue'
import CartPage          from '@/pages/CartPage.vue'
import CheckoutPage      from '@/pages/CheckoutPage.vue'
import OrdersPage        from '@/pages/OrdersPage.vue'
import AutoBuilderPage   from '@/pages/AutoBuilderPage.vue'

const routes = [
  { path: '/',            name: 'home',     component: LandingPage },
  { path: '/catalog',     name: 'catalog',  component: CatalogPage },
  { path: '/catalog/:id', name: 'product',  component: ProductDetailPage },
  { path: '/cart',        name: 'cart',     component: CartPage },
  { path: '/builder',     name: 'builder',  component: AutoBuilderPage },
  { path: '/checkout',    name: 'checkout', component: CheckoutPage,      meta: { requiresAuth: true } },
  { path: '/orders',      name: 'orders',   component: OrdersPage,        meta: { requiresAuth: true } },
  { path: '/orders/:id',  name: 'order',    component: () => import('@/pages/OrderDetailPage.vue'), meta: { requiresAuth: true } },
  { path: '/login',       name: 'login',    component: LoginPage },
  { path: '/register',    name: 'register', component: RegisterPage },
  { path: '/:pathMatch(.*)*', redirect: '/' },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior() { return { top: 0 } },
})

router.beforeEach((to, _, next) => {
  const auth = useAuthStore()
  if (to.meta.requiresAdmin) {
    if (!auth.isLoggedIn) return next({ name: 'login', query: { redirect: to.fullPath } })
    if (!auth.isAdmin)    return next({ name: 'home' })
  }
  if (to.meta.requiresAuth && !auth.isLoggedIn) {
    return next({ name: 'login', query: { redirect: to.fullPath } })
  }
  next()
})

export default router