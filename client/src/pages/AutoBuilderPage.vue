<script setup>
import { ref, computed } from 'vue'
import api from '@/api'
import { useCartStore } from '@/stores/cart'
import { useRouter, RouterLink } from 'vue-router'
import ScoreBreakdownBar from '@/components/ScoreBreakdownBar.vue'
import BrandTierBadge from '@/components/BrandTierBadge.vue'
import { fileUrl } from '@/api'

const cart   = useCartStore()
const router = useRouter()

const mode = ref('complete')
const form = ref({
  budget:       '',
  height:       '',
  riding_style: 'mixed',
  brand_tier:   '',
  priority:     'balanced',
})

const loading = ref(false)
const error   = ref('')
const results = ref(null)
const addedId = ref(null)

const ridingStyles = [
  { key: 'speed',   label: 'Speed',   icon: '⚡', desc: 'Road & performance' },
  { key: 'trail',   label: 'Trail',   icon: '🏔️', desc: 'Off-road & mountain' },
  { key: 'commute', label: 'Commute', icon: '🏙️', desc: 'Daily city riding' },
  { key: 'mixed',   label: 'Mixed',   icon: '🔄', desc: 'Versatile all-around' },
]

const priorities = [
  { key: 'balanced', label: 'Balanced',   icon: '⚖️' },
  { key: 'budget',   label: 'Best value', icon: '💰' },
  { key: 'brand',    label: 'Top brand',  icon: '🏆' },
  { key: 'fit',      label: 'Best fit',   icon: '📐' },
]

const tiers = [
  { key: '',  label: 'Any tier' },
  { key: '1', label: 'Tier 1 — Premium' },
  { key: '2', label: 'Tier 2 — Mid-range' },
  { key: '3', label: 'Tier 3 — Budget' },
]

const fmt      = (n) => '₱' + Number(n).toLocaleString()
const isValid  = computed(() =>
  form.value.budget && Number(form.value.budget) > 0 &&
  form.value.height && Number(form.value.height) > 0
)

async function runBuilder() {
  if (!isValid.value) { error.value = 'Please fill in budget and height.'; return }
  error.value = ''
  loading.value = true
  results.value = null
  try {
    const payload = {
      budget:       Number(form.value.budget),
      height_cm:    Number(form.value.height),
      riding_style: form.value.riding_style,
      priority:     form.value.priority,
      brand_tier:   form.value.brand_tier ? Number(form.value.brand_tier) : null,
      mode:         mode.value,
    }
    const { data } = await api.post('/builder/recommend', payload)
    results.value = data
  } catch (err) {
    error.value = err.response?.data?.detail || 'Builder failed. Please try again.'
  } finally {
    loading.value = false
  }
}

function addToCart(product) {
  cart.add(product)
  addedId.value = product.id
  setTimeout(() => addedId.value = null, 2000)
}

const rankConfig = [
  { label: 'Best Match',   bg: 'bg-clay-700',    text: 'text-cream', ring: 'ring-clay-300' },
  { label: 'Top Brand',    bg: 'bg-stone-800',   text: 'text-cream', ring: 'ring-stone-300' },
  { label: 'Budget Pick',  bg: 'bg-emerald-700', text: 'text-cream', ring: 'ring-emerald-300' },
]

const scoreLabels = {
  budget_score: 'Budget fit',
  size_score:   'Size match',
  style_score:  'Riding style',
  review_score: 'Reviews',
  brand_score:  'Brand tier',
}
</script>

<template>
  <div class="fade-in min-h-screen">

    <!-- Hero banner -->
    <div class="relative overflow-hidden border-b border-stone-200 bg-stone-950">
      <!-- Grid background -->
      <div class="absolute inset-0 opacity-[0.07]"
        style="background-image: linear-gradient(rgba(255,255,255,0.5) 1px, transparent 1px),
               linear-gradient(90deg, rgba(255,255,255,0.5) 1px, transparent 1px);
               background-size: 40px 40px;">
      </div>
      <!-- Glow -->
      <div class="absolute top-0 left-1/2 -translate-x-1/2 w-[600px] h-[200px] bg-clay-600/20 blur-[80px] rounded-full"></div>

      <div class="relative max-w-5xl mx-auto px-6 py-14 text-center">
        <div class="inline-flex items-center gap-2 px-3 py-1 rounded-full border border-stone-700 bg-stone-900 text-stone-400 text-xs font-mono mb-6">
          <span class="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse"></span>
          FIVE-FACTOR SCORING ENGINE · ACTIVE
        </div>
        <h1 class="font-display text-5xl md:text-6xl text-white tracking-tight leading-[0.95] mb-4">
          Auto-Builder
        </h1>
        <p class="text-stone-400 max-w-lg mx-auto text-base leading-relaxed">
          Tell us your budget, height, and how you ride. Our engine scores every bike in the catalog and ranks the top matches — and explains why.
        </p>
      </div>
    </div>

    <div class="max-w-5xl mx-auto px-6 py-10">

      <!-- Mode toggle -->
      <div class="flex justify-center mb-10">
        <div class="flex gap-1 p-1 bg-stone-100 rounded-xl border border-stone-200">
          <button
            v-for="m in [{ key: 'complete', label: '🚲  Complete bike' }, { key: 'custom', label: '🔧  Component build' }]"
            :key="m.key"
            @click="mode = m.key; results = null"
            :class="['px-6 py-2.5 rounded-lg text-sm font-medium transition-all',
              mode === m.key
                ? 'bg-white text-stone-900 shadow-sm border border-stone-200'
                : 'text-stone-500 hover:text-stone-700']"
          >{{ m.label }}</button>
        </div>
      </div>

      <div class="grid lg:grid-cols-5 gap-8">

        <!-- ── FORM PANEL ── -->
        <div class="lg:col-span-2">
          <div class="sticky top-24 space-y-5 bg-white border border-stone-200 rounded-2xl p-6 shadow-sm">

            <!-- Panel header -->
            <div class="flex items-center gap-2 pb-4 border-b border-stone-100">
              <div class="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></div>
              <span class="text-xs font-mono text-stone-400 uppercase tracking-widest">Input parameters</span>
            </div>

            <!-- Budget -->
            <div>
              <label class="input-label">Budget (₱)</label>
              <div class="relative">
                <span class="absolute left-3 top-1/2 -translate-y-1/2 text-stone-400 text-sm font-mono">₱</span>
                <input
                  v-model="form.budget"
                  type="number" min="1000"
                  class="input !pl-7 font-mono"
                  placeholder="15000"
                />
              </div>
            </div>

            <!-- Height -->
            <div>
              <label class="input-label">Height (cm)</label>
              <div class="relative">
                <input
                  v-model="form.height"
                  type="number" min="100" max="250"
                  class="input font-mono"
                  placeholder="170"
                />
                <span class="absolute right-3 top-1/2 -translate-y-1/2 text-stone-400 text-xs font-mono">cm</span>
              </div>
            </div>

            <!-- Riding style -->
            <div>
              <label class="input-label">Riding style</label>
              <div class="grid grid-cols-2 gap-2">
                <button
                  v-for="s in ridingStyles" :key="s.key"
                  @click="form.riding_style = s.key"
                  :class="['p-3 rounded-xl border text-left transition-all',
                    form.riding_style === s.key
                      ? 'border-clay-500 bg-clay-50 ring-1 ring-clay-200'
                      : 'border-stone-200 hover:border-stone-300 bg-white']"
                >
                  <p class="text-base mb-0.5">{{ s.icon }}</p>
                  <p class="text-xs font-semibold" :class="form.riding_style === s.key ? 'text-clay-800' : 'text-stone-700'">{{ s.label }}</p>
                  <p class="text-2xs text-stone-400 leading-tight mt-0.5">{{ s.desc }}</p>
                </button>
              </div>
            </div>

            <!-- Priority -->
            <div>
              <label class="input-label">Optimize for</label>
              <div class="grid grid-cols-2 gap-2">
                <button
                  v-for="p in priorities" :key="p.key"
                  @click="form.priority = p.key"
                  :class="['px-3 py-2.5 rounded-xl border text-sm font-medium transition-all flex items-center gap-2',
                    form.priority === p.key
                      ? 'border-clay-500 bg-clay-50 text-clay-800 ring-1 ring-clay-200'
                      : 'border-stone-200 text-stone-600 hover:border-stone-300 bg-white']"
                >
                  <span>{{ p.icon }}</span>{{ p.label }}
                </button>
              </div>
            </div>

            <!-- Brand tier -->
            <div>
              <label class="input-label">Brand tier</label>
              <select v-model="form.brand_tier" class="input">
                <option v-for="t in tiers" :key="t.key" :value="t.key">{{ t.label }}</option>
              </select>
            </div>

            <p v-if="error" class="text-sm text-red-700 bg-red-50 border border-red-200 px-3 py-2 rounded-lg">{{ error }}</p>

            <!-- Submit -->
            <button
              @click="runBuilder"
              :disabled="loading || !isValid"
              class="w-full py-3 rounded-xl font-medium text-sm transition-all relative overflow-hidden
                     disabled:opacity-50 disabled:cursor-not-allowed
                     bg-stone-950 text-white hover:bg-stone-800 active:scale-[0.98]"
            >
              <span v-if="loading" class="flex items-center justify-center gap-2">
                <span class="w-4 h-4 border-2 border-white/20 border-t-white rounded-full animate-spin"></span>
                Scoring builds…
              </span>
              <span v-else class="flex items-center justify-center gap-2">
                <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M9.813 15.904L9 18.75l-.813-2.846a4.5 4.5 0 00-3.09-3.09L2.25 12l2.846-.813a4.5 4.5 0 003.09-3.09L9 5.25l.813 2.846a4.5 4.5 0 003.09 3.09L15.75 12l-2.846.813a4.5 4.5 0 00-3.09 3.09z" />
                </svg>
                Find my bike
              </span>
            </button>
          </div>
        </div>

        <!-- ── RESULTS PANEL ── -->
        <div class="lg:col-span-3 min-h-[500px]">

          <!-- Empty state -->
          <div v-if="!results && !loading"
            class="h-full min-h-[500px] flex flex-col items-center justify-center rounded-2xl border-2 border-dashed border-stone-200 p-12 text-center gap-5"
          >
            <div class="w-20 h-20 rounded-2xl bg-stone-100 flex items-center justify-center">
              <svg viewBox="0 0 64 64" class="w-10 h-10 text-stone-400" fill="none" stroke="currentColor" stroke-width="1.5">
                <circle cx="16" cy="44" r="12"/><circle cx="48" cy="44" r="12"/>
                <path d="M16 44L28 20L48 44"/><path d="M28 20L24 10H18"/>
                <path d="M38 20L44 8"/>
              </svg>
            </div>
            <div>
              <p class="font-display text-2xl text-stone-400 mb-2">Awaiting input</p>
              <p class="text-sm text-stone-400 max-w-xs leading-relaxed">Set your preferences and run the scoring engine to get personalized recommendations.</p>
            </div>
            <div class="flex gap-2 flex-wrap justify-center">
              <span class="px-3 py-1 rounded-full bg-stone-100 text-stone-400 text-xs font-mono">budget_score</span>
              <span class="px-3 py-1 rounded-full bg-stone-100 text-stone-400 text-xs font-mono">size_score</span>
              <span class="px-3 py-1 rounded-full bg-stone-100 text-stone-400 text-xs font-mono">style_score</span>
              <span class="px-3 py-1 rounded-full bg-stone-100 text-stone-400 text-xs font-mono">review_score</span>
              <span class="px-3 py-1 rounded-full bg-stone-100 text-stone-400 text-xs font-mono">brand_score</span>
            </div>
          </div>

          <!-- Loading -->
          <div v-else-if="loading"
            class="h-full min-h-[500px] flex flex-col items-center justify-center gap-6 rounded-2xl border border-stone-200 bg-white p-12"
          >
            <div class="relative w-16 h-16">
              <div class="absolute inset-0 rounded-full border-2 border-stone-100"></div>
              <div class="absolute inset-0 rounded-full border-2 border-t-clay-600 animate-spin"></div>
              <div class="absolute inset-2 rounded-full border-2 border-stone-100"></div>
              <div class="absolute inset-2 rounded-full border-2 border-t-emerald-400 animate-spin" style="animation-duration:0.7s; animation-direction: reverse"></div>
            </div>
            <div class="text-center">
              <p class="font-medium text-stone-700 mb-1">Scoring catalog…</p>
              <p class="text-sm text-stone-400 font-mono">Running five-factor analysis</p>
            </div>
            <div class="flex gap-1">
              <span v-for="i in 5" :key="i"
                class="w-1.5 h-6 rounded-full bg-stone-200 animate-pulse"
                :style="`animation-delay: ${i * 0.1}s`"
              ></span>
            </div>
          </div>

          <!-- Results -->
          <div v-else-if="results" class="space-y-4">
            <div class="flex items-center justify-between mb-2">
              <div class="flex items-center gap-2">
                <span class="w-2 h-2 rounded-full bg-emerald-400"></span>
                <p class="text-sm text-stone-500 font-mono">
                  {{ results.recommendations?.length || 0 }} matches · scored
                </p>
              </div>
              <button @click="results = null; error = ''" class="text-xs text-stone-400 hover:text-stone-600 font-mono transition-colors">
                ← new search
              </button>
            </div>

            <!-- Recommendation cards -->
            <div
              v-for="(rec, idx) in results.recommendations"
              :key="rec.product?.id || idx"
              :class="['bg-white rounded-2xl overflow-hidden border transition-all',
                idx === 0 ? 'border-clay-300 ring-1 ring-clay-100 shadow-sm' : 'border-stone-200']"
            >
              <!-- Rank banner -->
              <div :class="[rankConfig[idx]?.bg || 'bg-stone-700', rankConfig[idx]?.text || 'text-white',
                'px-4 py-2 flex items-center justify-between text-xs font-mono tracking-widest uppercase']">
                <span>{{ rankConfig[idx]?.label || `Match #${idx + 1}` }}</span>
                <span class="opacity-60">#{{ String(idx + 1).padStart(2, '0') }}</span>
              </div>

              <div class="p-5">
                <div class="flex gap-4 mb-5">
                  <!-- Image -->
                  <div class="w-24 h-24 bg-stone-50 rounded-xl border border-stone-100 flex-shrink-0 overflow-hidden">
                    <img
                      v-if="rec.product?.image_url"
                      :src="fileUrl(rec.product.image_url)"
                      :alt="rec.product?.name"
                      class="w-full h-full object-cover"
                    />
                    <div v-else class="w-full h-full flex items-center justify-center text-stone-300">
                      <svg viewBox="0 0 40 40" class="w-10 h-10" fill="none" stroke="currentColor" stroke-width="1.5">
                        <circle cx="8" cy="28" r="8"/><circle cx="32" cy="28" r="8"/>
                        <path d="M8 28L18 12L32 28"/>
                      </svg>
                    </div>
                  </div>

                  <!-- Product info -->
                  <div class="flex-1 min-w-0">
                    <div class="flex items-center gap-2 mb-1.5 flex-wrap">
                      <BrandTierBadge :tier="rec.product?.brand_tier" size="sm" />
                      <span class="badge bg-stone-100 text-stone-500 text-2xs capitalize">
                        {{ rec.product?.category?.replace('_',' ') }}
                      </span>
                    </div>
                    <h3 class="font-semibold text-stone-900 leading-snug text-sm mb-0.5">{{ rec.product?.name }}</h3>
                    <p class="text-xs text-stone-400 mb-2">{{ rec.product?.brand }}</p>
                    <p class="font-display text-2xl text-clay-700">{{ fmt(rec.product?.price) }}</p>
                  </div>

                  <!-- Score dial -->
                  <div class="flex-shrink-0 text-right">
                    <div :class="['inline-flex flex-col items-center justify-center w-16 h-16 rounded-xl border-2',
                      idx === 0 ? 'border-clay-200 bg-clay-50' : 'border-stone-100 bg-stone-50']">
                      <span :class="['text-2xl font-display leading-none',
                        idx === 0 ? 'text-clay-700' : 'text-stone-700']">
                        {{ rec.total_score }}
                      </span>
                      <span class="text-2xs text-stone-400 font-mono mt-0.5">/100</span>
                    </div>
                  </div>
                </div>

                <!-- Score breakdown -->
                <div v-if="rec.scores" class="space-y-2.5 pt-4 border-t border-stone-100 mb-4">
                  <p class="text-2xs font-mono uppercase tracking-widest text-stone-400 mb-3">Score breakdown</p>
                  <ScoreBreakdownBar
                    v-for="(val, key) in rec.scores"
                    :key="key"
                    :label="scoreLabels[key] || key"
                    :score="Math.round(val)"
                    :max="20"
                  />
                </div>

                <!-- AI reason -->
                <div v-if="rec.reason" class="flex gap-2.5 bg-stone-950 rounded-xl px-4 py-3 mb-4">
                  <svg class="w-3.5 h-3.5 text-emerald-400 mt-0.5 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M9.813 15.904L9 18.75l-.813-2.846a4.5 4.5 0 00-3.09-3.09L2.25 12l2.846-.813a4.5 4.5 0 003.09-3.09L9 5.25l.813 2.846a4.5 4.5 0 003.09 3.09L15.75 12l-2.846.813a4.5 4.5 0 00-3.09 3.09z" />
                  </svg>
                  <p class="text-xs text-stone-400 leading-relaxed">{{ rec.reason }}</p>
                </div>

                <!-- Actions -->
                <div class="flex gap-2">
                  <button
                    @click="addToCart(rec.product)"
                    :disabled="!rec.product?.stock_quantity"
                    :class="['flex-1 py-2.5 rounded-xl text-sm font-medium transition-all',
                      addedId === rec.product?.id
                        ? 'bg-emerald-600 text-white'
                        : 'bg-stone-950 text-white hover:bg-stone-800 disabled:opacity-40 disabled:cursor-not-allowed']"
                  >
                    {{ addedId === rec.product?.id ? '✓ Added' : rec.product?.stock_quantity ? 'Add to cart' : 'Out of stock' }}
                  </button>
                  <RouterLink
                    :to="`/catalog/${rec.product?.id}`"
                    class="px-4 py-2.5 rounded-xl text-sm font-medium border border-stone-200 text-stone-700 hover:bg-stone-50 transition-all"
                  >
                    View →
                  </RouterLink>
                </div>
              </div>
            </div>

            <!-- No results -->
            <div v-if="!results.recommendations?.length" class="text-center py-16 text-stone-400">
              <p class="font-display text-xl mb-2">No matches found</p>
              <p class="text-sm">Try increasing your budget or removing the brand tier filter.</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>