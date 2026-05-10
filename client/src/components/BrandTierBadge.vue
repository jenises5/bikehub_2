<script setup>
import { computed } from 'vue'

const props = defineProps({
  tier: { type: [Number, String], default: null },
  size: { type: String, default: 'md' },
})

const label = computed(() => {
  switch (Number(props.tier)) {
    case 1: return 'Tier 1 · Premium'
    case 2: return 'Tier 2 · Mid/High'
    case 3: return 'Tier 3 · Budget/Mid'
    default: return 'Unverified'
  }
})

const tierClass = computed(() => {
  switch (Number(props.tier)) {
    case 1: return 'bg-violet-100 text-violet-900'
    case 2: return 'bg-emerald-100 text-emerald-900'
    case 3: return 'bg-amber-100 text-amber-900'
    default: return 'bg-stone-200 text-stone-700'
  }
})

const sizeClass = computed(() =>
  props.size === 'sm' ? 'text-2xs px-1.5 py-0.5' : 'text-xs px-2 py-0.5'
)
</script>

<template>
  <span
    class="inline-flex items-center gap-1 font-medium rounded-full tracking-wider"
    :class="[tierClass, sizeClass]"
  >
    {{ label }}
  </span>
</template>