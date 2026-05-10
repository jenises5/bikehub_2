<script setup>
import { onMounted, ref, computed, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import api from '@/api'
import ProductCard from '@/components/ProductCard.vue'

const route  = useRoute()
const router = useRouter()

const products   = ref([])
const loading    = ref(true)
const error      = ref(null)
const search     = ref(route.query.search || '')
const category   = ref(route.query.category || '')
const sortBy     = ref(route.query.sort || '')

const categories = [
  { key: '', label: 'All' },
  { key: 'mountain_bike', label: 'Mountain' },
  { key: 'road_bike',     label: 'Road' },
  { key: 'fixed_gear',   label: 'Fixed Gear' },
  { key: 'gravel',       label: 'Gravel' },
]

const sorts = [
  { key: '',           label: 'Default' },
  { key: 'price_asc',  label: 'Price: Low → High' },
  { key: 'price_desc', label: 'Price: High → Low' },
  { key: 'name',       label: 'Name A–Z' },
]

async function fetchProducts() {
  loading.value = true
  error.value   = null
  try {
    const params = {}
    if (category.value) params.category = category.value
    if (search.value)   params.search   = search.value
    const { data } = await api.get('/products/', { params })
    products.value = data || []
  } catch {
    error.value = 'Could not load products.'
  } finally {
    loading.value = false
  }
}

const sorted = computed(() => {
  const list = [...products.value]
  if (sortBy.value === 'price_asc')  return list.sort((a,b) => a.price - b.price)
  if (sortBy.value === 'price_desc') return list.sort((a,b) => b.price - a.price)
  if (sortBy.value === 'name')       return list.sort((a,b) => a.name.localeCompare(b.name))
  return list
})

function setCategory(key) {
  category.value = key
  router.replace({ query: { ...route.query, category: key || undefined } })
}

watch([category, search], () => fetchProducts())
onMounted(fetchProducts)
</script>

<template>
  <div class="fade-in max-w-7xl mx-auto px-6 py-12">
    <!-- Header -->
    <div class="mb-8">
      <p class="eyebrow mb-2">Shop</p>
      <h1 class="font-display text-5xl tracking-tight">Catalog</h1>
    </div>

    <!-- Controls -->
    <div class="flex flex-wrap gap-3 mb-8 items-center justify-between">
      <!-- Category tabs -->
      <div class="flex gap-2 flex-wrap">
        <button
          v-for="cat in categories" :key="cat.key"
          @click="setCategory(cat.key)"
          :class="[
            'px-4 py-1.5 rounded-full text-sm font-medium border transition-all',
            category === cat.key
              ? 'bg-clay-700 text-cream border-clay-700'
              : 'bg-white text-stone-700 border-stone-300 hover:border-clay-500'
          ]"
        >{{ cat.label }}</button>
      </div>

      <div class="flex gap-2 items-center flex-wrap">
        <!-- Search -->
        <input v-model="search" type="search" placeholder="Search bikes…" class="input !w-48 !py-1.5 !text-sm" />
        <!-- Sort -->
        <select v-model="sortBy" class="input !w-44 !py-1.5 !text-sm">
          <option v-for="s in sorts" :key="s.key" :value="s.key">{{ s.label }}</option>
        </select>
      </div>
    </div>

    <!-- Grid -->
    <div v-if="loading" class="flex justify-center py-24"><span class="spinner"></span></div>
    <div v-else-if="error" class="text-center py-24 text-stone-500">{{ error }}</div>
    <div v-else-if="sorted.length === 0" class="text-center py-24 text-stone-500">
      No bikes match your filters.
    </div>
    <div v-else class="grid grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-5">
      <ProductCard v-for="p in sorted" :key="p.id" :product="p" />
    </div>
  </div>
</template>