<script setup>
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import { fileUrl } from '@/api'
import BrandTierBadge from './BrandTierBadge.vue'

const props = defineProps({
  product: { type: Object, required: true },
})

const router = useRouter()

const imgSrc = computed(() =>
  props.product.image_url ? fileUrl(props.product.image_url) : null
)

const inStock = computed(() => (props.product.stock_quantity || 0) > 0)

const formatPHP = (n) =>
  '₱' + (Number(n) || 0).toLocaleString('en-PH', { maximumFractionDigits: 0 })

function goToProduct() {
 router.push(`/catalog/${props.product.id}`)
}
</script>

<template>
  <article
    class="card-hover group cursor-pointer overflow-hidden flex flex-col"
    @click="goToProduct"
  >
    <div class="relative aspect-[4/3] bg-cream-deep flex items-center justify-center overflow-hidden">
      <img
        v-if="imgSrc"
        :src="imgSrc"
        :alt="product.name"
        class="w-full h-full object-cover transition-transform duration-300 group-hover:scale-[1.03]"
        @error="(e) => e.target.style.display = 'none'"
      />
      <svg
        v-else
        viewBox="0 0 64 64"
        class="w-16 h-16 text-stone-400"
        fill="none"
        stroke="currentColor"
        stroke-width="1.5"
        stroke-linecap="round"
        stroke-linejoin="round"
      >
        <circle cx="14" cy="44" r="10" />
        <circle cx="50" cy="44" r="10" />
        <path d="M14 44 L28 22 L46 22 L50 44" />
      </svg>

      <div
        v-if="!inStock"
        class="absolute inset-0 bg-stone-900/40 flex items-center justify-center"
      >
        <span class="text-xs font-medium tracking-wider uppercase text-cream bg-stone-900/80 px-3 py-1 rounded">
          Out of stock
        </span>
      </div>
    </div>

    <div class="p-4 flex flex-col flex-1">
      <p class="text-2xs uppercase tracking-wider text-stone-500 mb-0.5">
        {{ product.brand_name || '—' }}
      </p>
      <h3 class="font-medium text-stone-900 line-clamp-2 leading-snug mb-2 min-h-[2.5rem]">
        {{ product.name }}
      </h3>
      <div class="flex items-center gap-2 mb-3">
        <BrandTierBadge :tier="product.brand_tier" size="sm" />
      </div>
      <div class="mt-auto">
        <p class="font-display text-xl text-stone-900 leading-none">
          {{ formatPHP(product.price) }}
        </p>
        <p class="text-2xs text-stone-500 mt-1">
          <span v-if="inStock">{{ product.stock_quantity }} in stock</span>
          <span v-else>Restocking soon</span>
        </p>
      </div>
    </div>
  </article>
</template>