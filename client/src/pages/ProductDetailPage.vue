<script setup>
import { onMounted, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import api, { fileUrl } from '@/api'
import BrandTierBadge from '@/components/BrandTierBadge.vue'
import { useCartStore } from '@/stores/cart'

const route  = useRoute()
const router = useRouter()
const cart   = useCartStore()

const product  = ref(null)
const loading  = ref(true)
const error    = ref(null)
const qty      = ref(1)
const added    = ref(false)
const imgIdx   = ref(0)

onMounted(async () => {
  try {
    const { data } = await api.get(`/products/${route.params.id}`)
    product.value = data
  } catch {
    error.value = 'Product not found.'
  } finally {
    loading.value = false
  }
})

function addToCart() {
  cart.add(product.value, qty.value)
  added.value = true
  setTimeout(() => added.value = false, 2000)
}

const fmt = (n) => '₱' + Number(n).toLocaleString()
</script>

<template>
  <div class="fade-in max-w-7xl mx-auto px-6 py-12">
    <button @click="router.back()" class="text-sm text-stone-500 hover:text-stone-800 mb-8 flex items-center gap-1">
      ← Back
    </button>

    <div v-if="loading" class="flex justify-center py-24"><span class="spinner"></span></div>
    <div v-else-if="error" class="text-center py-24 text-stone-500">{{ error }}</div>

    <div v-else-if="product" class="grid md:grid-cols-2 gap-12">
      <!-- Images -->
      <div>
        <div class="aspect-square bg-cream-deep rounded-xl border border-stone-200 overflow-hidden mb-3">
          <img
            v-if="product.images?.[imgIdx]"
            :src="fileUrl(product.images[imgIdx])"
            :alt="product.name"
            class="w-full h-full object-cover"
          />
          <div v-else class="w-full h-full flex items-center justify-center text-stone-300">
            <svg viewBox="0 0 100 100" class="w-24 h-24" fill="none" stroke="currentColor" stroke-width="1.5">
              <circle cx="25" cy="70" r="20"/><circle cx="75" cy="70" r="20"/>
              <path d="M25 70L45 35L75 70"/><path d="M45 35L40 20H30"/>
            </svg>
          </div>
        </div>
        <div v-if="product.images?.length > 1" class="flex gap-2">
          <button
            v-for="(img, i) in product.images" :key="i"
            @click="imgIdx = i"
            :class="['w-16 h-16 rounded border-2 overflow-hidden transition-all',
              i === imgIdx ? 'border-clay-600' : 'border-stone-200']"
          >
            <img :src="fileUrl(img)" class="w-full h-full object-cover" />
          </button>
        </div>
      </div>

      <!-- Info -->
      <div>
        <div class="flex items-start gap-3 mb-2">
          <BrandTierBadge :tier="product.brand_tier" />
          <span class="badge bg-stone-100 text-stone-600">{{ product.category?.replace('_',' ') }}</span>
        </div>
        <h1 class="font-display text-4xl tracking-tight mb-1">{{ product.name }}</h1>
        <p class="text-stone-500 text-sm mb-4">{{ product.brand }}</p>
        <p class="font-display text-3xl text-clay-700 mb-6">{{ fmt(product.price) }}</p>

        <p v-if="product.description" class="text-stone-600 leading-relaxed mb-6">{{ product.description }}</p>

        <!-- Specs -->
        <div v-if="product.specs && Object.keys(product.specs).length" class="mb-8">
          <h3 class="text-xs font-medium uppercase tracking-widest text-stone-500 mb-3">Specifications</h3>
          <dl class="divide-y divide-stone-100">
            <div v-for="(val, key) in product.specs" :key="key" class="flex justify-between py-2 text-sm">
              <dt class="text-stone-500 capitalize">{{ key.replace(/_/g,' ') }}</dt>
              <dd class="font-medium text-stone-800">{{ val }}</dd>
            </div>
          </dl>
        </div>

        <!-- Stock -->
        <p v-if="product.stock === 0" class="text-sm text-red-600 font-medium mb-4">Out of stock</p>
        <p v-else class="text-sm text-stone-500 mb-4">{{ product.stock }} in stock</p>

        <!-- Qty + Add -->
        <div class="flex gap-3 items-center">
          <div class="flex items-center border border-stone-300 rounded overflow-hidden">
            <button @click="qty = Math.max(1, qty-1)" class="px-3 py-2 text-stone-600 hover:bg-stone-100">−</button>
            <span class="px-4 py-2 text-sm font-medium">{{ qty }}</span>
            <button @click="qty++" class="px-3 py-2 text-stone-600 hover:bg-stone-100">+</button>
          </div>
          <button
            @click="addToCart"
            :disabled="product.stock === 0"
            class="btn-primary flex-1 !py-2.5"
          >
            {{ added ? '✓ Added to cart' : 'Add to cart' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>