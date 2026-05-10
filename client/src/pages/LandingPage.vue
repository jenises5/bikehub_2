<script setup>
import { onMounted, ref } from 'vue'
import { RouterLink } from 'vue-router'
import api from '@/api'
import ProductCard from '@/components/ProductCard.vue'

const featured = ref([])
const loading = ref(true)
const error = ref(null)

const categories = [
  { key: 'mountain_bike', label: 'Mountain', desc: 'Trail-ready hardtails and full-suspension builds.' },
  { key: 'road_bike',     label: 'Road',     desc: 'Drop-bar bikes built for tarmac and speed.' },
  { key: 'fixed_gear',    label: 'Fixed Gear', desc: 'Track-style frames for the city.' },
  { key: 'gravel',        label: 'Gravel',   desc: 'Versatile, rough-road capable rigs.' },
]

onMounted(async () => {
  loading.value = true
  try {
    const { data } = await api.get('/products/?limit=6')
    featured.value = (data || []).slice(0, 6)
  } catch (err) {
    error.value = 'Could not load featured products.'
  } finally {
    loading.value = false
  }
})
</script>

<template>
  <div class="fade-in">

    <!-- HERO -->
    <section class="max-w-7xl mx-auto px-6 pt-16 pb-20 md:pt-24 md:pb-28 grid md:grid-cols-12 gap-10 items-center">
      <div class="md:col-span-7">
        <p class="eyebrow mb-5">An intelligent bike marketplace · Cebu, PH</p>
        <h1 class="font-display text-5xl md:text-7xl leading-[0.95] tracking-tight text-stone-900 mb-6">
          The right bike,<br/>
          <span class="italic font-normal text-clay-700">found for you.</span>
        </h1>
        <p class="text-lg text-stone-600 max-w-xl mb-8 leading-relaxed">
          Tell us your budget, height, and how you ride. Our five-factor scoring engine ranks builds against your needs — and explains every recommendation.
        </p>
        <div class="flex flex-wrap gap-3">
          <RouterLink to="/builder" class="btn-primary !px-6 !py-3 !text-base">
            Build my bike →
          </RouterLink>
          <RouterLink to="/catalog" class="btn-secondary !px-6 !py-3 !text-base">
            Browse catalog
          </RouterLink>
        </div>
      </div>

      <div class="md:col-span-5">
        <div class="aspect-square bg-cream-deep rounded-2xl flex items-center justify-center border border-stone-200">
          <svg viewBox="0 0 200 200" class="w-3/4 h-3/4 text-stone-400" fill="none"
               stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
            <circle cx="50" cy="140" r="40" />
            <circle cx="150" cy="140" r="40" />
            <path d="M50 140 L90 70 L150 70 L150 140" />
            <path d="M90 70 L80 50 L65 50" />
            <path d="M120 70 L135 40" />
          </svg>
        </div>
      </div>
    </section>

    <!-- HOW IT WORKS -->
    <section class="border-y border-stone-200 bg-cream-deep">
      <div class="max-w-7xl mx-auto px-6 py-20 grid md:grid-cols-12 gap-10">
        <div class="md:col-span-4">
          <p class="eyebrow mb-3">How it works</p>
          <h2 class="font-display text-4xl tracking-tight">Guided, not generic.</h2>
          <p class="mt-4 text-stone-600">Three steps and you have a build that fits your budget, your body, and your riding.</p>
        </div>
        <div class="md:col-span-8 grid sm:grid-cols-3 gap-8">
          <div>
            <p class="font-display text-5xl text-clay-700">01</p>
            <h3 class="text-base font-medium mt-3 mb-2">Tell us about you</h3>
            <p class="text-sm text-stone-600 leading-relaxed">Your budget, height in centimeters, and how you ride.</p>
          </div>
          <div>
            <p class="font-display text-5xl text-clay-700">02</p>
            <h3 class="text-base font-medium mt-3 mb-2">We score every match</h3>
            <p class="text-sm text-stone-600 leading-relaxed">Five factors: budget, size, style, reviews, brand tier.</p>
          </div>
          <div>
            <p class="font-display text-5xl text-clay-700">03</p>
            <h3 class="text-base font-medium mt-3 mb-2">Pick your tier</h3>
            <p class="text-sm text-stone-600 leading-relaxed">Best Match, Best Brand, or Budget Pick. Add to cart. Done.</p>
          </div>
        </div>
      </div>
    </section>

    <!-- FEATURED -->
    <section class="max-w-7xl mx-auto px-6 py-20">
      <div class="flex items-end justify-between mb-8 flex-wrap gap-4">
        <div>
          <p class="eyebrow mb-2">Featured builds</p>
          <h2 class="font-display text-4xl tracking-tight">In stock and ready to roll.</h2>
        </div>
        <RouterLink to="/catalog" class="text-sm font-medium text-clay-700 hover:underline">
          View full catalog →
        </RouterLink>
      </div>

      <div v-if="loading" class="flex justify-center py-12">
        <span class="spinner"></span>
      </div>
      <div v-else-if="error" class="text-sm text-stone-500 py-12 text-center">{{ error }}</div>
      <div v-else-if="featured.length === 0" class="text-sm text-stone-500 py-12 text-center">
        No products available yet.
      </div>
      <div v-else class="grid grid-cols-2 lg:grid-cols-3 gap-5">
        <ProductCard v-for="product in featured" :key="product.id" :product="product" />
      </div>
    </section>

    <!-- CATEGORIES -->
    <section class="max-w-7xl mx-auto px-6 pb-20">
      <p class="eyebrow mb-2">Shop by category</p>
      <h2 class="font-display text-4xl tracking-tight mb-8">Find your kind of riding.</h2>
      <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
        <RouterLink
          v-for="cat in categories"
          :key="cat.key"
          :to="`/catalog?category=${cat.key}`"
          class="group p-6 bg-white border border-stone-200 rounded-lg hover:border-clay-600 hover:bg-clay-50 transition-all"
        >
          <h3 class="font-display text-2xl text-stone-900 group-hover:text-clay-700 transition-colors">
            {{ cat.label }}
          </h3>
          <p class="text-sm text-stone-600 mt-2 leading-relaxed">{{ cat.desc }}</p>
        </RouterLink>
      </div>
    </section>

  </div>
</template>