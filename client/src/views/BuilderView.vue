<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";
import api from "../services/api";
import { useCartStore } from "../stores/cart";
import { useUserStore } from "../stores/user";

const router = useRouter();
const cartStore = useCartStore();
const userStore = useUserStore();

const step = ref(1);
const loading = ref(false);
const error = ref("");
const results = ref(null);

const budgetMin = ref(20000);
const budgetMax = ref(80000);
const heightCm = ref(170);
const ridingStyle = ref("road");
const mode = ref("complete_bike");

const ridingStyles = ["road", "mountain", "gravel", "urban", "commute"];

const formatPrice = (n) => `₱${Number(n).toLocaleString("en-PH")}`;
const formatCategory = (name) =>
  (name || "").replace(/_/g, " ").replace(/\b\w/g, (c) => c.toUpperCase());

function logout() {
  userStore.logout();
  router.push("/login");
}

async function generate() {
  if (budgetMin.value > budgetMax.value) {
    error.value = "Minimum budget cannot exceed maximum budget.";
    return;
  }
  error.value = "";
  loading.value = true;
  try {
    const res = await api.post("/builder/generate", {
      budget_min: budgetMin.value,
      budget_max: budgetMax.value,
      height_cm: heightCm.value,
      riding_style: ridingStyle.value,
      mode: mode.value,
    });
    results.value = res.data;
    step.value = 2;
  } catch (err) {
    error.value =
      err.response?.data?.detail ||
      "Failed to generate builds. Please try again.";
  } finally {
    loading.value = false;
  }
}

function reset() {
  step.value = 1;
  results.value = null;
  error.value = "";
}
function scoreColor(score) {
  return score >= 0.8
    ? "text-lime-400"
    : score >= 0.6
      ? "text-yellow-400"
      : "text-neutral-400";
}
function scoreBg(score) {
  return score >= 0.8
    ? "bg-lime-400"
    : score >= 0.6
      ? "bg-yellow-400"
      : "bg-neutral-600";
}
function scorePercent(score) {
  return Math.round(score * 100);
}
</script>

<template>
  <div
    class="min-h-screen bg-neutral-950 text-neutral-100 font-body antialiased"
  >
    <nav
      class="sticky top-0 z-50 backdrop-blur-md bg-neutral-950/80 border-b border-neutral-800"
    >
      <div
        class="max-w-7xl mx-auto px-6 py-4 flex items-center justify-between"
      >
        <div class="flex items-center gap-12">
          <router-link to="/" class="font-display text-2xl tracking-tight"
            >BIKE<span class="text-lime-400">HUB</span></router-link
          >
          <div
            class="hidden md:flex items-center gap-8 font-mono text-xs uppercase tracking-widest text-neutral-400"
          >
            <router-link
              to="/shop"
              class="hover:text-lime-400 transition-colors"
              >Shop</router-link
            >
            <router-link to="/builder" class="text-lime-400"
              >Builder</router-link
            >
            <router-link
              to="/about"
              class="hover:text-lime-400 transition-colors"
              >About</router-link
            >
            <router-link
              to="/support"
              class="hover:text-lime-400 transition-colors"
              >Support</router-link
            >
          </div>
        </div>
        <div class="flex items-center gap-6">
          <template v-if="userStore.isLoggedIn">
            <span
              class="hidden md:inline font-mono text-xs uppercase tracking-widest text-lime-400"
              >{{ userStore.user?.name?.split(" ")[0] }}</span
            >
            <button
              @click="logout"
              class="hidden md:inline font-mono text-xs uppercase tracking-widest text-neutral-400 hover:text-red-400 transition-colors"
            >
              Logout
            </button>
          </template>
          <router-link
            v-else
            to="/login"
            class="hidden md:inline font-mono text-xs uppercase tracking-widest text-neutral-400 hover:text-lime-400 transition-colors"
            >Login</router-link
          >
          <router-link
            to="/cart"
            class="relative text-neutral-400 hover:text-lime-400 transition-colors"
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
            <span
              v-if="cartStore.count > 0"
              class="absolute -top-2 -right-2 bg-lime-400 text-neutral-950 text-[10px] font-bold w-4 h-4 rounded-full flex items-center justify-center"
              >{{ cartStore.count }}</span
            >
          </router-link>
        </div>
      </div>
    </nav>

    <div class="border-b border-neutral-800">
      <div class="max-w-7xl mx-auto px-6 py-12">
        <div
          class="font-mono text-xs uppercase tracking-widest text-neutral-500 mb-3"
        >
          // CUSTOM BUILDER
        </div>
        <h1 class="font-display text-5xl md:text-7xl leading-tight">
          Build it<br /><span class="text-lime-400">your way.</span>
        </h1>
        <p class="mt-4 text-neutral-400 max-w-lg">
          Tell us your budget, height, and riding style — we'll score and
          recommend the best builds from our catalog.
        </p>
      </div>
    </div>

    <!-- FORM -->
    <div v-if="step === 1" class="max-w-3xl mx-auto px-6 py-16">
      <div class="mb-10">
        <div
          class="font-mono text-xs uppercase tracking-widest text-neutral-500 mb-3"
        >
          Build Mode
        </div>
        <div class="flex border border-neutral-800">
          <button
            @click="mode = 'complete_bike'"
            class="flex-1 font-mono text-xs uppercase tracking-widest py-3 transition-colors"
            :class="
              mode === 'complete_bike'
                ? 'bg-lime-400 text-neutral-950'
                : 'text-neutral-400 hover:text-neutral-100'
            "
          >
            Complete Bike
          </button>
          <button
            @click="mode = 'custom_build'"
            class="flex-1 font-mono text-xs uppercase tracking-widest py-3 transition-colors"
            :class="
              mode === 'custom_build'
                ? 'bg-lime-400 text-neutral-950'
                : 'text-neutral-400 hover:text-neutral-100'
            "
          >
            Custom Build
          </button>
        </div>
        <p class="font-mono text-xs text-neutral-600 mt-2">
          {{
            mode === "complete_bike"
              ? "Find a ready-to-ride complete bicycle within your budget."
              : "Get component recommendations to build your own custom bike."
          }}
        </p>
      </div>
      <div class="space-y-8">
        <div>
          <div
            class="font-mono text-xs uppercase tracking-widest text-neutral-500 mb-3"
          >
            Budget Range
          </div>
          <div class="grid grid-cols-2 gap-4">
            <div>
              <label class="font-mono text-xs text-neutral-600 mb-1 block"
                >Min (₱)</label
              ><input
                v-model.number="budgetMin"
                type="number"
                min="0"
                step="1000"
                class="w-full bg-neutral-900 border border-neutral-800 text-neutral-100 font-mono text-sm px-4 py-3 focus:outline-none focus:border-lime-400 transition-colors"
              />
            </div>
            <div>
              <label class="font-mono text-xs text-neutral-600 mb-1 block"
                >Max (₱)</label
              ><input
                v-model.number="budgetMax"
                type="number"
                min="0"
                step="1000"
                class="w-full bg-neutral-900 border border-neutral-800 text-neutral-100 font-mono text-sm px-4 py-3 focus:outline-none focus:border-lime-400 transition-colors"
              />
            </div>
          </div>
          <div
            class="flex justify-between font-mono text-xs text-neutral-500 mt-2"
          >
            <span>{{ formatPrice(budgetMin) }}</span
            ><span>{{ formatPrice(budgetMax) }}</span>
          </div>
        </div>
        <div>
          <div
            class="font-mono text-xs uppercase tracking-widest text-neutral-500 mb-3"
          >
            Your Height — <span class="text-lime-400">{{ heightCm }} cm</span>
          </div>
          <input
            v-model.number="heightCm"
            type="range"
            min="140"
            max="210"
            step="1"
            class="w-full accent-lime-400"
          />
          <div
            class="flex justify-between font-mono text-xs text-neutral-600 mt-1"
          >
            <span>140 cm</span><span>210 cm</span>
          </div>
        </div>
        <div>
          <div
            class="font-mono text-xs uppercase tracking-widest text-neutral-500 mb-3"
          >
            Riding Style
          </div>
          <div class="grid grid-cols-3 md:grid-cols-5 gap-2">
            <button
              v-for="style in ridingStyles"
              :key="style"
              @click="ridingStyle = style"
              class="font-mono text-xs uppercase tracking-widest py-3 border transition-colors"
              :class="
                ridingStyle === style
                  ? 'bg-lime-400 text-neutral-950 border-lime-400'
                  : 'bg-neutral-900 text-neutral-400 border-neutral-800 hover:border-neutral-600'
              "
            >
              {{ formatCategory(style) }}
            </button>
          </div>
        </div>
        <div
          v-if="error"
          class="font-mono text-xs text-red-400 border border-red-900 bg-red-950/50 px-4 py-3"
        >
          {{ error }}
        </div>
        <button
          @click="generate"
          :disabled="loading"
          class="w-full font-mono text-sm uppercase tracking-widest py-5 transition-colors"
          :class="
            loading
              ? 'bg-neutral-700 text-neutral-500'
              : 'bg-lime-400 hover:bg-lime-300 text-neutral-950'
          "
        >
          <span v-if="loading">Scoring builds…</span
          ><span v-else>Generate My Build →</span>
        </button>
      </div>
    </div>

    <!-- RESULTS -->
    <div v-else-if="step === 2 && results" class="max-w-7xl mx-auto px-6 py-12">
      <div class="flex items-center justify-between mb-8">
        <div>
          <div
            class="font-mono text-xs uppercase tracking-widest text-neutral-500 mb-2"
          >
            // RESULTS
          </div>
          <h2 class="font-display text-4xl">
            {{
              mode === "complete_bike"
                ? "Recommended Bikes"
                : "Your Custom Build"
            }}
          </h2>
          <p class="font-mono text-xs text-neutral-500 mt-1">
            {{ formatPrice(budgetMin) }} – {{ formatPrice(budgetMax) }} ·
            {{ heightCm }}cm · {{ formatCategory(ridingStyle) }} · Size
            {{ results.recommended_size }}
          </p>
        </div>
        <button
          @click="reset"
          class="font-mono text-xs uppercase tracking-widest text-neutral-400 hover:text-lime-400 transition-colors border border-neutral-800 hover:border-lime-400 px-4 py-2"
        >
          ← New Build
        </button>
      </div>

      <!-- Complete Bike -->
      <div v-if="mode === 'complete_bike'" class="grid md:grid-cols-3 gap-6">
        <div
          v-if="results.results?.best_match"
          class="group bg-neutral-900 border border-lime-400"
        >
          <div
            class="bg-lime-400 text-neutral-950 font-mono text-xs uppercase tracking-widest px-4 py-2 text-center"
          >
            ★ {{ results.results.best_match.label }}
          </div>
          <div
            class="aspect-square bg-neutral-950 border-b border-neutral-800 flex items-center justify-center"
          >
            <svg
              viewBox="0 0 200 120"
              class="w-2/3 text-lime-400"
              fill="none"
              stroke="currentColor"
              stroke-width="2"
            >
              <circle cx="44" cy="84" r="28" />
              <circle cx="156" cy="84" r="28" />
              <path
                d="M44 84 L96 24 L156 84 M96 24 L124 84 M96 24 L72 84 M44 84 L72 84"
              />
            </svg>
          </div>
          <div class="p-6">
            <div class="flex items-center justify-between mb-2">
              <span class="font-mono text-xs text-neutral-500 uppercase"
                >Score</span
              ><span class="font-display text-2xl text-lime-400">{{
                scorePercent(results.results.best_match.product.final_score)
              }}</span>
            </div>
            <div class="h-1 bg-neutral-800 mb-4">
              <div
                class="h-1 bg-lime-400"
                :style="`width:${scorePercent(results.results.best_match.product.final_score)}%`"
              ></div>
            </div>
            <h3 class="font-display text-2xl mb-1">
              {{ results.results.best_match.product.name }}
            </h3>
            <p class="font-mono text-xs text-neutral-500 mb-2 line-clamp-2">
              {{ results.results.best_match.product.description }}
            </p>
            <p class="font-mono text-xs text-neutral-600 mb-4">
              {{ results.results.best_match.description }}
            </p>
            <div
              class="flex items-baseline justify-between pt-4 border-t border-neutral-800"
            >
              <span class="font-display text-3xl text-lime-400">{{
                formatPrice(results.results.best_match.product.price)
              }}</span>
              <router-link
                :to="`/bike/${results.results.best_match.product.id}`"
                class="font-mono text-xs uppercase tracking-widest text-neutral-400 hover:text-lime-400 transition-colors"
                >View →</router-link
              >
            </div>
          </div>
        </div>
        <div
          v-if="results.results?.best_brand"
          class="group bg-neutral-900 border border-neutral-800 hover:border-lime-400 transition-colors"
        >
          <div
            class="bg-neutral-800 text-neutral-300 font-mono text-xs uppercase tracking-widest px-4 py-2 text-center"
          >
            {{ results.results.best_brand.label }}
          </div>
          <div
            class="aspect-square bg-neutral-950 border-b border-neutral-800 flex items-center justify-center"
          >
            <svg
              viewBox="0 0 200 120"
              class="w-2/3 text-neutral-700 group-hover:text-lime-400 transition-colors"
              fill="none"
              stroke="currentColor"
              stroke-width="2"
            >
              <circle cx="44" cy="84" r="28" />
              <circle cx="156" cy="84" r="28" />
              <path
                d="M44 84 L96 24 L156 84 M96 24 L124 84 M96 24 L72 84 M44 84 L72 84"
              />
            </svg>
          </div>
          <div class="p-6">
            <div class="flex items-center justify-between mb-2">
              <span class="font-mono text-xs text-neutral-500 uppercase"
                >Score</span
              ><span
                class="font-display text-2xl"
                :class="
                  scoreColor(results.results.best_brand.product.final_score)
                "
                >{{
                  scorePercent(results.results.best_brand.product.final_score)
                }}</span
              >
            </div>
            <div class="h-1 bg-neutral-800 mb-4">
              <div
                class="h-1"
                :class="scoreBg(results.results.best_brand.product.final_score)"
                :style="`width:${scorePercent(results.results.best_brand.product.final_score)}%`"
              ></div>
            </div>
            <h3 class="font-display text-2xl mb-1">
              {{ results.results.best_brand.product.name }}
            </h3>
            <p class="font-mono text-xs text-neutral-500 mb-2 line-clamp-2">
              {{ results.results.best_brand.product.description }}
            </p>
            <p class="font-mono text-xs text-neutral-600 mb-4">
              {{ results.results.best_brand.description }}
            </p>
            <div
              class="flex items-baseline justify-between pt-4 border-t border-neutral-800"
            >
              <span class="font-display text-3xl text-lime-400">{{
                formatPrice(results.results.best_brand.product.price)
              }}</span>
              <router-link
                :to="`/bike/${results.results.best_brand.product.id}`"
                class="font-mono text-xs uppercase tracking-widest text-neutral-400 hover:text-lime-400 transition-colors"
                >View →</router-link
              >
            </div>
          </div>
        </div>
        <div
          v-if="results.results?.budget_pick"
          class="group bg-neutral-900 border border-neutral-800 hover:border-lime-400 transition-colors"
        >
          <div
            class="bg-neutral-800 text-neutral-300 font-mono text-xs uppercase tracking-widest px-4 py-2 text-center"
          >
            {{ results.results.budget_pick.label }}
          </div>
          <div
            class="aspect-square bg-neutral-950 border-b border-neutral-800 flex items-center justify-center"
          >
            <svg
              viewBox="0 0 200 120"
              class="w-2/3 text-neutral-700 group-hover:text-lime-400 transition-colors"
              fill="none"
              stroke="currentColor"
              stroke-width="2"
            >
              <circle cx="44" cy="84" r="28" />
              <circle cx="156" cy="84" r="28" />
              <path
                d="M44 84 L96 24 L156 84 M96 24 L124 84 M96 24 L72 84 M44 84 L72 84"
              />
            </svg>
          </div>
          <div class="p-6">
            <div class="flex items-center justify-between mb-2">
              <span class="font-mono text-xs text-neutral-500 uppercase"
                >Score</span
              ><span
                class="font-display text-2xl"
                :class="
                  scoreColor(results.results.budget_pick.product.final_score)
                "
                >{{
                  scorePercent(results.results.budget_pick.product.final_score)
                }}</span
              >
            </div>
            <div class="h-1 bg-neutral-800 mb-4">
              <div
                class="h-1"
                :class="
                  scoreBg(results.results.budget_pick.product.final_score)
                "
                :style="`width:${scorePercent(results.results.budget_pick.product.final_score)}%`"
              ></div>
            </div>
            <h3 class="font-display text-2xl mb-1">
              {{ results.results.budget_pick.product.name }}
            </h3>
            <p class="font-mono text-xs text-neutral-500 mb-2 line-clamp-2">
              {{ results.results.budget_pick.product.description }}
            </p>
            <p class="font-mono text-xs text-neutral-600 mb-4">
              {{ results.results.budget_pick.description }}
            </p>
            <div
              class="flex items-baseline justify-between pt-4 border-t border-neutral-800"
            >
              <span class="font-display text-3xl text-lime-400">{{
                formatPrice(results.results.budget_pick.product.price)
              }}</span>
              <router-link
                :to="`/bike/${results.results.budget_pick.product.id}`"
                class="font-mono text-xs uppercase tracking-widest text-neutral-400 hover:text-lime-400 transition-colors"
                >View →</router-link
              >
            </div>
          </div>
        </div>
      </div>

      <!-- Custom Build -->
      <div
        v-else-if="
          mode === 'custom_build' && results.results?.best_match?.components
        "
        class="space-y-6"
      >
        <div
          class="bg-neutral-900 border border-lime-400 p-6 flex items-center justify-between"
        >
          <div>
            <div
              class="font-mono text-xs uppercase tracking-widest text-neutral-500 mb-1"
            >
              Estimated Total
            </div>
            <div class="font-display text-4xl text-lime-400">
              {{ formatPrice(results.results.best_match.total_price || 0) }}
            </div>
          </div>
          <div class="font-mono text-xs text-neutral-500 text-right">
            <div>
              Budget: {{ formatPrice(budgetMin) }} –
              {{ formatPrice(budgetMax) }}
            </div>
            <div class="mt-1">
              Recommended Size: {{ results.recommended_size }}
            </div>
          </div>
        </div>
        <div class="grid md:grid-cols-2 gap-4">
          <div
            v-for="(component, type) in results.results.best_match.components"
            :key="type"
            class="bg-neutral-900 border border-neutral-800 p-5"
          >
            <div
              class="font-mono text-xs uppercase tracking-widest text-lime-400 mb-3"
            >
              {{ formatCategory(type) }}
            </div>
            <div v-if="component">
              <div class="flex items-start justify-between gap-4">
                <div class="flex-1">
                  <h4 class="font-display text-xl mb-1">
                    {{ component.name }}
                  </h4>
                  <p
                    class="font-mono text-xs text-neutral-500 line-clamp-2 mb-2"
                  >
                    {{ component.description }}
                  </p>
                  <div class="flex items-center gap-2">
                    <div class="h-1 flex-1 bg-neutral-800">
                      <div
                        class="h-1"
                        :class="scoreBg(component.final_score)"
                        :style="`width:${scorePercent(component.final_score)}%`"
                      ></div>
                    </div>
                    <span
                      class="font-mono text-xs"
                      :class="scoreColor(component.final_score)"
                      >{{ scorePercent(component.final_score) }}</span
                    >
                  </div>
                </div>
                <div class="text-right shrink-0">
                  <div class="font-display text-xl text-lime-400">
                    {{ formatPrice(component.price) }}
                  </div>
                  <div class="font-mono text-xs text-neutral-500 mt-1">
                    {{ component.brand_name }}
                  </div>
                  <router-link
                    :to="`/bike/${component.id}`"
                    class="font-mono text-xs text-neutral-600 hover:text-lime-400 transition-colors"
                    >View →</router-link
                  >
                </div>
              </div>
            </div>
            <div v-else class="font-mono text-xs text-neutral-600">
              No match found
            </div>
          </div>
        </div>
      </div>

      <div v-else class="py-16 text-center">
        <div class="font-display text-3xl text-neutral-700 mb-4">
          No results found
        </div>
        <p class="font-mono text-xs text-neutral-500 mb-6">
          Try adjusting your budget or riding style.
        </p>
        <button
          @click="reset"
          class="font-mono text-xs uppercase tracking-widest text-lime-400 hover:text-lime-300 transition-colors"
        >
          ← Try Again
        </button>
      </div>
    </div>
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
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>
