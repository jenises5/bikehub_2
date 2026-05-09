<script setup>
const team = [
  {
    name: "Mark Daniel Castillo",
    role: "Project Manager",
    bio: "Keeps the team on track and the roadmap clear. Makes sure BikeHub ships on time and on spec.",
  },
  {
    name: "Dave Hoyohoy",
    role: "Hacker",
    bio: "Backend wizard. Built the scoring engine, API, and database architecture that powers BikeHub.",
  },
  {
    name: "Jenises Mariquit",
    role: "Hipster",
    bio: "Designed the BikeHub experience from the ground up. Obsessed with clean UI and pixel-perfect details.",
  },
  {
    name: "Ivan Fernandez",
    role: "Hipster",
    bio: "Brought the vision to life through design thinking and user-centered decisions across every page.",
  },
];

const stats = [
  { value: "2024", label: "Founded" },
  { value: "39+", label: "Products" },
  { value: "16", label: "Brands" },
  { value: "Cebu", label: "Based In" },
];
</script>

<template>
  <div
    class="min-h-screen bg-neutral-950 text-neutral-100 font-body antialiased"
  >
    <!-- NAV -->
    <nav
      class="sticky top-0 z-50 backdrop-blur-md bg-neutral-950/80 border-b border-neutral-800"
    >
      <div
        class="max-w-7xl mx-auto px-6 py-4 flex items-center justify-between"
      >
        <div class="flex items-center gap-12">
          <router-link to="/" class="font-display text-2xl tracking-tight">
            BIKE<span class="text-lime-400">HUB</span>
          </router-link>
          <div
            class="hidden md:flex items-center gap-8 font-mono text-xs uppercase tracking-widest text-neutral-400"
          >
            <router-link
              to="/shop"
              class="hover:text-lime-400 transition-colors"
              >Shop</router-link
            >
            <router-link
              to="/builder"
              class="hover:text-lime-400 transition-colors"
              >Builder</router-link
            >
            <router-link to="/about" class="text-lime-400">About</router-link>
            <router-link
              to="/support"
              class="hover:text-lime-400 transition-colors"
              >Support</router-link
            >
          </div>
        </div>
        <div class="flex items-center gap-6">
          <router-link
            to="/login"
            class="hidden md:inline font-mono text-xs uppercase tracking-widest text-neutral-400 hover:text-lime-400 transition-colors"
            >Login</router-link
          >
          <router-link
            to="/cart"
            class="text-neutral-400 hover:text-lime-400 transition-colors"
          >
            <svg
              class="w-5 h-5"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              stroke-width="2"
            >
              <circle cx="9" cy="21" r="1" />
              <circle cx="20" cy="21" r="1" />
              <path
                d="M1 1h4l2.7 13.4a2 2 0 0 0 2 1.6h9.7a2 2 0 0 0 2-1.6L23 6H6"
              />
            </svg>
          </router-link>
        </div>
      </div>
    </nav>

    <!-- HERO -->
    <section class="border-b border-neutral-800">
      <div
        class="max-w-7xl mx-auto px-6 py-24 grid md:grid-cols-2 gap-12 items-center"
      >
        <div>
          <div
            class="font-mono text-xs uppercase tracking-widest text-neutral-500 mb-4"
          >
            // ABOUT US
          </div>
          <h1 class="font-display text-6xl md:text-8xl leading-[0.9] mb-6">
            Built for<br /><span class="text-lime-400">riders.</span>
          </h1>
          <p class="text-lg text-neutral-400 leading-relaxed max-w-md">
            BikeHub is the final project of EdgeTech, a group of 4 students from
            Cebu. We got tired of seeing overpriced, poorly-specced bikes and
            decided to build something better — a platform where riders
            configure exactly what they need, at fair prices.
          </p>
        </div>
        <div
          class="grid grid-cols-2 gap-px bg-neutral-800 border border-neutral-800"
        >
          <div
            v-for="stat in stats"
            :key="stat.label"
            class="bg-neutral-950 p-8"
          >
            <div class="font-display text-5xl text-lime-400 mb-2">
              {{ stat.value }}
            </div>
            <div
              class="font-mono text-xs uppercase tracking-widest text-neutral-500"
            >
              {{ stat.label }}
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- MISSION -->
    <section class="border-b border-neutral-800">
      <div class="max-w-7xl mx-auto px-6 py-20 grid md:grid-cols-3 gap-12">
        <div>
          <div
            class="font-mono text-xs uppercase tracking-widest text-lime-400 mb-4"
          >
            01
          </div>
          <h3 class="font-display text-2xl mb-3">Transparency</h3>
          <p class="text-neutral-400 text-sm leading-relaxed">
            Every product is scored on brand quality, compatibility, and value.
            No hidden markups, no paid placements.
          </p>
        </div>
        <div>
          <div
            class="font-mono text-xs uppercase tracking-widest text-lime-400 mb-4"
          >
            02
          </div>
          <h3 class="font-display text-2xl mb-3">Compatibility First</h3>
          <p class="text-neutral-400 text-sm leading-relaxed">
            Our builder scores components in real time. You'll never
            accidentally order incompatible parts.
          </p>
        </div>
        <div>
          <div
            class="font-mono text-xs uppercase tracking-widest text-lime-400 mb-4"
          >
            03
          </div>
          <h3 class="font-display text-2xl mb-3">Local Roots</h3>
          <p class="text-neutral-400 text-sm leading-relaxed">
            Based in Cebu, Philippines. We understand local riding conditions
            and stock components suited for our roads and trails.
          </p>
        </div>
      </div>
    </section>

    <!-- TEAM -->
    <section class="border-b border-neutral-800">
      <div class="max-w-7xl mx-auto px-6 py-20">
        <div
          class="font-mono text-xs uppercase tracking-widest text-neutral-500 mb-3"
        >
          // THE TEAM
        </div>
        <h2 class="font-display text-4xl md:text-5xl mb-12">
          People behind<br />the build.
        </h2>
        <div class="grid md:grid-cols-4 gap-6">
          <div
            v-for="member in team"
            :key="member.name"
            class="bg-neutral-900 border border-neutral-800 p-6 hover:border-lime-400 transition-colors"
          >
            <div
              class="w-12 h-12 bg-lime-400 mb-4 flex items-center justify-center"
            >
              <span class="font-display text-2xl text-neutral-950">{{
                member.name[0]
              }}</span>
            </div>
            <h3 class="font-display text-xl mb-1">{{ member.name }}</h3>
            <div
              class="font-mono text-xs uppercase tracking-widest text-lime-400 mb-3"
            >
              {{ member.role }}
            </div>
            <p class="text-sm text-neutral-400 leading-relaxed">
              {{ member.bio }}
            </p>
          </div>
        </div>
      </div>
    </section>

    <!-- CTA -->
    <section class="border-b border-neutral-800">
      <div class="max-w-7xl mx-auto px-6 py-24 text-center">
        <h2 class="font-display text-5xl md:text-7xl mb-6">Ready to ride?</h2>
        <p class="text-neutral-400 mb-10 max-w-md mx-auto">
          Browse our catalog or let the builder find your perfect match.
        </p>
        <div class="flex flex-wrap justify-center gap-4">
          <router-link
            to="/builder"
            class="inline-flex items-center gap-3 bg-lime-400 hover:bg-lime-300 text-neutral-950 font-mono text-sm uppercase tracking-widest px-8 py-4 transition-colors"
          >
            Start Your Build →
          </router-link>
          <router-link
            to="/shop"
            class="inline-flex items-center gap-3 border border-neutral-700 hover:border-lime-400 hover:text-lime-400 text-neutral-300 font-mono text-sm uppercase tracking-widest px-8 py-4 transition-colors"
          >
            Browse Shop
          </router-link>
        </div>
      </div>
    </section>

    <!-- FOOTER -->
    <footer class="border-t border-neutral-800">
      <div
        class="max-w-7xl mx-auto px-6 py-8 flex flex-col md:flex-row justify-between gap-4 font-mono text-xs text-neutral-500 uppercase tracking-widest"
      >
        <div>© © 2026 BIKEHUB · EDGETECH · CEBU, PH</div>
        <router-link to="/" class="hover:text-lime-400 transition-colors"
          >← Back to Home</router-link
        >
      </div>
    </footer>
  </div>
</template>

<style scoped>
.font-display {
  font-family: "Bebas Neue", "Arial Narrow", sans-serif;
  letter-spacing: 0.01em;
}
.font-mono {
  font-family: "JetBrains Mono", "Courier New", monospace;
}
.font-body {
  font-family:
    "Manrope",
    system-ui,
    -apple-system,
    sans-serif;
}
</style>
