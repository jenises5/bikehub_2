<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import NavBar from '@/components/NavBar.vue'

// Get info about the current route (which URL the user is on)
const route = useRoute()

// Some pages (admin) will eventually use a different layout (sidebar instead of navbar).
// We hide the public NavBar on routes starting with '/admin'.
// For Phase 2 nothing matches /admin yet, but we set up the pattern now.
const showNavBar = computed(() => !route.path.startsWith('/admin'))
</script>

<template>
<<<<<<< HEAD
  <RouterView />
=======
  <div class="min-h-screen flex flex-col">

    <!-- Top navigation (hidden on admin pages later) -->
    <NavBar v-if="showNavBar" />

    <!-- The current routed page renders here, with a fade transition -->
    <main class="flex-1">
      <RouterView v-slot="{ Component }">
        <transition name="fade" mode="out-in">
          <component :is="Component" />
        </transition>
      </RouterView>
    </main>

    <!-- Footer (hidden on admin pages later) -->
    <footer
      v-if="showNavBar"
      class="border-t border-stone-200 bg-cream-deep mt-16"
    >
      <div class="max-w-7xl mx-auto px-6 py-8 flex flex-col md:flex-row items-start md:items-center justify-between gap-4 text-sm text-stone-600">
        <div>
          <p class="font-display text-lg text-stone-900">BikeHub</p>
          <p class="text-xs">Built for Filipino cyclists · CTU-Main BSIS Capstone</p>
        </div>
        <p class="text-xs">© 2026 BikeHub. All rights reserved.</p>
      </div>
    </footer>

  </div>
>>>>>>> 48da94096a2a516f3758e317689b63040e8a024f
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