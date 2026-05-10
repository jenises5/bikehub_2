<script setup>
import { computed, ref, onMounted, onUnmounted } from 'vue'
import { RouterLink, useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useCartStore } from '@/stores/cart'

const auth      = useAuthStore()
const cartStore = useCartStore()
const router    = useRouter()
const route     = useRoute()

const userMenuOpen = ref(false)
const menuRef      = ref(null)

const cartCount = computed(() => cartStore.count)
const initial   = computed(() => (auth.user?.name?.[0] || 'U').toUpperCase())

function handleLogout() {
  auth.logout()
  userMenuOpen.value = false
  router.push('/')
}

// Close dropdown when clicking outside
function onClickOutside(e) {
  if (menuRef.value && !menuRef.value.contains(e.target)) {
    userMenuOpen.value = false
  }
}
onMounted(()  => document.addEventListener('mousedown', onClickOutside))
onUnmounted(() => document.removeEventListener('mousedown', onClickOutside))
</script>

<template>
  <header class="sticky top-0 z-40 border-b border-stone-200/80 bg-cream/90 backdrop-blur-lg">
    <div class="max-w-7xl mx-auto px-6 h-16 flex items-center justify-between gap-6">

      <!-- Logo -->
      <RouterLink to="/" class="flex items-center gap-2.5 shrink-0 group">
        <span class="w-8 h-8 rounded-lg bg-clay-700 text-cream flex items-center justify-center font-display text-lg leading-none shadow-sm group-hover:bg-clay-800 transition-colors">
          B
        </span>
        <span class="font-display text-xl tracking-tight text-stone-900">
          Bike<span class="text-clay-700">Hub</span>
        </span>
      </RouterLink>

      <!-- Primary nav -->
      <nav class="hidden md:flex items-center gap-1 flex-1 justify-center">
        <RouterLink
          v-for="link in [
            { to: '/catalog', label: 'Catalog' },
            { to: '/builder', label: 'Auto-Builder' },
          ]"
          :key="link.to"
          :to="link.to"
          class="relative px-4 py-2 text-sm font-medium text-stone-600 hover:text-stone-900 transition-colors rounded-md hover:bg-stone-100/70 group"
          active-class="!text-clay-700"
        >
          {{ link.label }}
          <span
            class="absolute bottom-0 left-1/2 -translate-x-1/2 h-0.5 w-0 bg-clay-600 rounded-full transition-all group-[.router-link-active]:w-4"
          ></span>
        </RouterLink>

        <RouterLink
          v-if="auth.isLoggedIn"
          to="/orders"
          class="relative px-4 py-2 text-sm font-medium text-stone-600 hover:text-stone-900 transition-colors rounded-md hover:bg-stone-100/70 group"
          active-class="!text-clay-700"
        >
          My Orders
          <span class="absolute bottom-0 left-1/2 -translate-x-1/2 h-0.5 w-0 bg-clay-600 rounded-full transition-all group-[.router-link-active]:w-4"></span>
        </RouterLink>
      </nav>

      <!-- Right side -->
      <div class="flex items-center gap-1 shrink-0">

        <!-- Cart -->
        <RouterLink
          to="/cart"
          class="relative p-2 rounded-lg text-stone-500 hover:text-clay-700 hover:bg-stone-100/70 transition-all"
          title="Cart"
        >
          <svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
            <path stroke-linecap="round" stroke-linejoin="round"
              d="M2.25 3h1.386c.51 0 .955.343 1.087.835l.383 1.437M7.5 14.25a3 3 0 00-3 3h15.75m-12.75-3h11.218c1.121-1.9.083-8.906-1.041-9.083H7.5m0 0l-.383-1.437M7.5 14.25L5.106 5.272M15 19.5a1.5 1.5 0 11-3 0 1.5 1.5 0 013 0zm6 0a1.5 1.5 0 11-3 0 1.5 1.5 0 013 0z"
            />
          </svg>
          <transition name="pop">
            <span
              v-if="cartCount > 0"
              class="absolute -top-0.5 -right-0.5 min-w-[1.1rem] h-[1.1rem] px-0.5 bg-clay-700 text-cream text-[10px] font-semibold rounded-full flex items-center justify-center leading-none"
            >
              {{ cartCount > 99 ? '99+' : cartCount }}
            </span>
          </transition>
        </RouterLink>

        <!-- Divider -->
        <span class="w-px h-5 bg-stone-200 mx-1"></span>

        <!-- Logged in -->
        <div v-if="auth.isLoggedIn" class="relative" ref="menuRef">
          <button
            @click="userMenuOpen = !userMenuOpen"
            class="flex items-center gap-2 pl-1.5 pr-3 py-1 rounded-full border border-transparent hover:border-stone-200 hover:bg-stone-50 transition-all"
          >
            <span class="w-7 h-7 rounded-full bg-clay-700 text-cream text-xs font-semibold flex items-center justify-center ring-2 ring-clay-200">
              {{ initial }}
            </span>
            <span class="hidden sm:inline text-sm font-medium text-stone-700 max-w-[120px] truncate">
              {{ auth.user?.name || 'Account' }}
            </span>
            <svg
              xmlns="http://www.w3.org/2000/svg"
              class="w-3.5 h-3.5 text-stone-400 transition-transform"
              :class="userMenuOpen ? 'rotate-180' : ''"
              viewBox="0 0 20 20" fill="currentColor"
            >
              <path fill-rule="evenodd" d="M5.23 7.21a.75.75 0 011.06.02L10 11.168l3.71-3.938a.75.75 0 111.08 1.04l-4.25 4.5a.75.75 0 01-1.08 0l-4.25-4.5a.75.75 0 01.02-1.06z" clip-rule="evenodd" />
            </svg>
          </button>

          <!-- Dropdown -->
          <transition name="dropdown">
            <div
              v-if="userMenuOpen"
              class="absolute right-0 top-full mt-2 w-56 bg-white border border-stone-200 rounded-xl shadow-lg py-2 overflow-hidden"
            >
              <!-- User info header -->
              <div class="px-4 py-2.5 border-b border-stone-100 mb-1">
                <p class="text-xs font-semibold text-stone-900 truncate">{{ auth.user?.name }}</p>
                <p class="text-xs text-stone-400 truncate">{{ auth.user?.email }}</p>
              </div>

              <RouterLink
                v-if="auth.isAdmin"
                to="/admin"
                @click="userMenuOpen = false"
                class="flex items-center gap-2.5 px-4 py-2 text-sm text-stone-700 hover:bg-stone-50 transition-colors"
              >
                <svg class="w-4 h-4 text-stone-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M9.594 3.94c.09-.542.56-.94 1.11-.94h2.593c.55 0 1.02.398 1.11.94l.213 1.281c.063.374.313.686.645.87.074.04.147.083.22.127.324.196.72.257 1.075.124l1.217-.456a1.125 1.125 0 011.37.49l1.296 2.247a1.125 1.125 0 01-.26 1.431l-1.003.827c-.293.24-.438.613-.431.992a6.759 6.759 0 010 .255c-.007.378.138.75.43.99l1.005.828c.424.35.534.954.26 1.43l-1.298 2.247a1.125 1.125 0 01-1.369.491l-1.217-.456c-.355-.133-.75-.072-1.076.124a6.57 6.57 0 01-.22.128c-.331.183-.581.495-.644.869l-.213 1.28c-.09.543-.56.941-1.11.941h-2.594c-.55 0-1.02-.398-1.11-.94l-.213-1.281c-.062-.374-.312-.686-.644-.87a6.52 6.52 0 01-.22-.127c-.325-.196-.72-.257-1.076-.124l-1.217.456a1.125 1.125 0 01-1.369-.49l-1.297-2.247a1.125 1.125 0 01.26-1.431l1.004-.827c.292-.24.437-.613.43-.992a6.932 6.932 0 010-.255c.007-.378-.138-.75-.43-.99l-1.004-.828a1.125 1.125 0 01-.26-1.43l1.297-2.247a1.125 1.125 0 011.37-.491l1.216.456c.356.133.751.072 1.076-.124.072-.044.146-.087.22-.128.332-.183.582-.495.644-.869l.214-1.281z" />
                  <path stroke-linecap="round" stroke-linejoin="round" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                </svg>
                Admin Dashboard
              </RouterLink>

              <RouterLink
                to="/orders"
                @click="userMenuOpen = false"
                class="flex items-center gap-2.5 px-4 py-2 text-sm text-stone-700 hover:bg-stone-50 transition-colors"
              >
                <svg class="w-4 h-4 text-stone-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
                </svg>
                My Orders
              </RouterLink>

              <RouterLink
                to="/cart"
                @click="userMenuOpen = false"
                class="flex items-center gap-2.5 px-4 py-2 text-sm text-stone-700 hover:bg-stone-50 transition-colors"
              >
                <svg class="w-4 h-4 text-stone-400" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M2.25 3h1.386c.51 0 .955.343 1.087.835l.383 1.437M7.5 14.25a3 3 0 00-3 3h15.75m-12.75-3h11.218c1.121-1.9.083-8.906-1.041-9.083H7.5m0 0l-.383-1.437M7.5 14.25L5.106 5.272M15 19.5a1.5 1.5 0 11-3 0 1.5 1.5 0 013 0zm6 0a1.5 1.5 0 11-3 0 1.5 1.5 0 013 0z" />
                </svg>
                Cart
                <span v-if="cartCount > 0" class="ml-auto badge bg-clay-100 text-clay-800 !py-0">{{ cartCount }}</span>
              </RouterLink>

              <div class="border-t border-stone-100 mt-1 pt-1">
                <button
                  @click="handleLogout"
                  class="flex items-center gap-2.5 w-full px-4 py-2 text-sm text-red-600 hover:bg-red-50 transition-colors"
                >
                  <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.5">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M15.75 9V5.25A2.25 2.25 0 0013.5 3h-6a2.25 2.25 0 00-2.25 2.25v13.5A2.25 2.25 0 007.5 21h6a2.25 2.25 0 002.25-2.25V15M12 9l-3 3m0 0l3 3m-3-3h12.75" />
                  </svg>
                  Log out
                </button>
              </div>
            </div>
          </transition>
        </div>

        <!-- Logged out -->
        <template v-else>
          <RouterLink to="/login" class="btn-ghost !px-3.5 !py-1.5 !text-sm">Log in</RouterLink>
          <RouterLink to="/register" class="btn-primary !px-3.5 !py-1.5 !text-sm">Sign up</RouterLink>
        </template>
      </div>
    </div>
  </header>
</template>

<style scoped>
.dropdown-enter-active { transition: all 0.15s ease-out; }
.dropdown-leave-active { transition: all 0.1s ease-in; }
.dropdown-enter-from  { opacity: 0; transform: translateY(-6px) scale(0.98); }
.dropdown-leave-to    { opacity: 0; transform: translateY(-4px) scale(0.98); }

.pop-enter-active { transition: all 0.2s cubic-bezier(0.34, 1.56, 0.64, 1); }
.pop-leave-active { transition: all 0.1s ease-in; }
.pop-enter-from   { opacity: 0; transform: scale(0.5); }
.pop-leave-to     { opacity: 0; transform: scale(0.5); }
</style>