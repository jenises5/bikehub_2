<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import NavBar from '@/components/NavBar.vue'

const route = useRoute()
const showNavBar = computed(() => !route.path.startsWith('/admin'))
</script>

<template>
  <div class="min-h-screen flex flex-col">
    <NavBar v-if="showNavBar" />
    <main class="flex-1">
      <RouterView v-slot="{ Component }">
        <transition name="fade" mode="out-in">
          <component :is="Component" />
        </transition>
      </RouterView>
    </main>
    <footer v-if="showNavBar" class="border-t border-stone-200 bg-cream-deep mt-16">
      <div class="max-w-7xl mx-auto px-6 py-8 flex flex-col md:flex-row items-start md:items-center justify-between gap-4 text-sm text-stone-600">
        <div>
          <p class="font-display text-lg text-stone-900">BikeHub</p>
          <p class="text-xs">Built for Filipino cyclists · CTU-Main BSIS Capstone</p>
        </div>
        <p class="text-xs">© 2026 BikeHub. All rights reserved.</p>
      </div>
    </footer>
  </div>
</template>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.18s ease;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
