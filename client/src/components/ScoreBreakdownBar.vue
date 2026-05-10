<script setup>
import { computed } from 'vue'

const props = defineProps({
  label: { type: String, required: true },
  score: { type: Number, required: true },
  max:   { type: Number, default: 20 },
})

const pct = computed(() => Math.round((props.score / props.max) * 100))

const color = computed(() => {
  if (pct.value >= 80) return 'high'
  if (pct.value >= 50) return 'mid'
  return 'low'
})
</script>

<template>
  <div class="group relative">
    <div class="flex justify-between items-center mb-1.5">
      <div class="flex items-center gap-1.5">
        <!-- Glowing dot indicator -->
        <span :class="[
          'w-1.5 h-1.5 rounded-full flex-shrink-0',
          color === 'high' ? 'bg-emerald-400 shadow-[0_0_6px_2px_rgba(52,211,153,0.5)]' :
          color === 'mid'  ? 'bg-clay-400  shadow-[0_0_6px_2px_rgba(180,100,60,0.4)]' :
                             'bg-stone-400'
        ]"></span>
        <span class="text-xs font-medium text-stone-500 tracking-wide">{{ label }}</span>
      </div>
      <div class="flex items-baseline gap-0.5">
        <span :class="[
          'text-sm font-semibold font-mono tabular-nums',
          color === 'high' ? 'text-emerald-600' :
          color === 'mid'  ? 'text-clay-700' :
                             'text-stone-500'
        ]">{{ score }}</span>
        <span class="text-2xs text-stone-400 font-mono">/{{ max }}</span>
      </div>
    </div>

    <!-- Track -->
    <div class="relative h-1.5 bg-stone-100 rounded-full overflow-hidden">
      <!-- Subtle grid lines -->
      <div class="absolute inset-0 flex justify-between px-[20%]">
        <span class="w-px h-full bg-stone-200/60"></span>
        <span class="w-px h-full bg-stone-200/60"></span>
        <span class="w-px h-full bg-stone-200/60"></span>
      </div>

      <!-- Fill bar -->
      <div
        :class="[
          'absolute inset-y-0 left-0 rounded-full transition-all duration-700 ease-out',
          color === 'high'
            ? 'bg-gradient-to-r from-emerald-400 to-emerald-500'
            : color === 'mid'
            ? 'bg-gradient-to-r from-clay-500 to-clay-700'
            : 'bg-gradient-to-r from-stone-300 to-stone-400'
        ]"
        :style="{ width: pct + '%' }"
      >
        <!-- Shimmer effect -->
        <span class="absolute inset-0 bg-gradient-to-r from-transparent via-white/30 to-transparent -translate-x-full animate-[shimmer_2s_ease-in-out_infinite]"></span>
      </div>
    </div>

    <!-- Percentage label -->
    <div class="flex justify-end mt-0.5">
      <span class="text-2xs font-mono text-stone-300">{{ pct }}%</span>
    </div>
  </div>
</template>

<style scoped>
@keyframes shimmer {
  0%   { transform: translateX(-100%); }
  60%  { transform: translateX(200%); }
  100% { transform: translateX(200%); }
}
</style>