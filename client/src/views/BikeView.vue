<script setup>
import { ref, onMounted } from "vue";
import { useRoute, useRouter } from "vue-router";
import api from "../services/api";
import { useCartStore } from "../stores/cart";
import { useUserStore } from "../stores/user";

const route = useRoute();
const router = useRouter();
const cartStore = useCartStore();
const userStore = useUserStore();

const product = ref(null);
const loading = ref(true);
const error = ref("");
const quantity = ref(1);
const addedToCart = ref(false);

const formatPrice = (n) => `₱${Number(n).toLocaleString("en-PH")}`;
const formatCategory = (name) =>
  (name || "").replace(/_/g, " ").replace(/\b\w/g, (c) => c.toUpperCase());

function logout() {
  userStore.logout();
  router.push("/login");
}

onMounted(async () => {
  try {
    const res = await api.get(`/products/${route.params.id}`);
    product.value = res.data;
  } catch (err) {
    error.value = "Product not found.";
  } finally {
    loading.value = false;
  }
});

function addToCart() {
  cartStore.addItem(product.value, quantity.value);
  addedToCart.value = true;
  setTimeout(() => (addedToCart.value = false), 2000);
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
            <router-link
              to="/builder"
              class="hover:text-lime-400 transition-colors"
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
            aria-label="Cart"
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
      <div
        class="max-w-7xl mx-auto px-6 py-4 flex items-center gap-2 font-mono text-xs text-neutral-500 uppercase tracking-widest"
      >
        <router-link to="/shop" class="hover:text-lime-400 transition-colors"
          >Shop</router-link
        >
        <span>→</span>
        <span v-if="product">{{ formatCategory(product.category) }}</span>
        <span v-if="product">→</span>
        <span v-if="product" class="text-neutral-300">{{ product.name }}</span>
      </div>
    </div>

    <div v-if="loading" class="max-w-7xl mx-auto px-6 py-20">
      <div class="grid md:grid-cols-2 gap-12">
        <div class="aspect-square bg-neutral-900 animate-pulse"></div>
        <div class="space-y-4">
          <div class="h-8 bg-neutral-900 animate-pulse w-3/4"></div>
          <div class="h-4 bg-neutral-900 animate-pulse w-1/2"></div>
        </div>
      </div>
    </div>

    <div v-else-if="error" class="max-w-7xl mx-auto px-6 py-20 text-center">
      <div class="font-display text-4xl text-neutral-700 mb-4">{{ error }}</div>
      <router-link
        to="/shop"
        class="font-mono text-xs uppercase tracking-widest text-lime-400 hover:text-lime-300 transition-colors"
        >← Back to Shop</router-link
      >
    </div>

    <div v-else-if="product" class="max-w-7xl mx-auto px-6 py-12">
      <div class="grid md:grid-cols-2 gap-12 items-start">
        <div
          class="aspect-square bg-neutral-900 border border-neutral-800 flex items-center justify-center sticky top-24"
        >
          <img
            v-if="product.image_url"
            :src="product.image_url"
            :alt="product.name"
            class="w-full h-full object-cover"
          />
          <div v-else class="w-full h-full flex items-center justify-center">
            <svg
              viewBox="0 0 200 120"
              class="w-2/3 text-neutral-700"
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
        </div>

        <div>
          <div class="flex items-center gap-3 mb-4">
            <span
              class="font-mono text-xs uppercase tracking-widest text-lime-400 border border-lime-400/30 px-2 py-1"
              >{{ product.brand_name || "BikeHub" }}</span
            >
            <span
              class="font-mono text-xs uppercase tracking-widest text-neutral-500 border border-neutral-800 px-2 py-1"
              >{{ formatCategory(product.category) }}</span
            >
          </div>
          <h1 class="font-display text-5xl md:text-6xl leading-tight mb-4">
            {{ product.name }}
          </h1>
          <div class="font-display text-4xl text-lime-400 mb-6">
            {{ formatPrice(product.price) }}
          </div>
          <p class="text-neutral-400 leading-relaxed mb-8">
            {{ product.description }}
          </p>

          <div
            class="grid grid-cols-2 gap-px bg-neutral-800 border border-neutral-800 mb-8"
          >
            <div class="bg-neutral-950 p-4">
              <div
                class="font-mono text-[10px] uppercase tracking-widest text-neutral-500 mb-1"
              >
                Category
              </div>
              <div class="font-mono text-sm">
                {{ formatCategory(product.category) }}
              </div>
            </div>
            <div class="bg-neutral-950 p-4">
              <div
                class="font-mono text-[10px] uppercase tracking-widest text-neutral-500 mb-1"
              >
                Riding Style
              </div>
              <div class="font-mono text-sm">
                {{ formatCategory(product.riding_style) }}
              </div>
            </div>
            <div class="bg-neutral-950 p-4">
              <div
                class="font-mono text-[10px] uppercase tracking-widest text-neutral-500 mb-1"
              >
                Frame Size
              </div>
              <div class="font-mono text-sm">
                {{ product.frame_size || "—" }}
              </div>
            </div>
            <div class="bg-neutral-950 p-4">
              <div
                class="font-mono text-[10px] uppercase tracking-widest text-neutral-500 mb-1"
              >
                Stock
              </div>
              <div
                class="font-mono text-sm"
                :class="
                  product.stock_quantity <= product.low_stock_threshold
                    ? 'text-red-400'
                    : ''
                "
              >
                {{
                  product.stock_quantity <= product.low_stock_threshold
                    ? `Low — ${product.stock_quantity} left`
                    : `${product.stock_quantity} available`
                }}
              </div>
            </div>
          </div>

          <div class="flex items-center gap-4 mb-4">
            <div class="flex items-center border border-neutral-800">
              <button
                @click="quantity = Math.max(1, quantity - 1)"
                class="px-4 py-3 font-mono text-neutral-400 hover:text-lime-400 hover:bg-neutral-900 transition-colors"
              >
                −
              </button>
              <span
                class="px-4 py-3 font-mono text-sm min-w-[3rem] text-center"
                >{{ quantity }}</span
              >
              <button
                @click="
                  quantity = Math.min(product.stock_quantity, quantity + 1)
                "
                class="px-4 py-3 font-mono text-neutral-400 hover:text-lime-400 hover:bg-neutral-900 transition-colors"
              >
                +
              </button>
            </div>
            <button
              @click="addToCart"
              :disabled="product.stock_quantity === 0"
              class="flex-1 font-mono text-sm uppercase tracking-widest py-3 transition-colors"
              :class="
                addedToCart
                  ? 'bg-neutral-700 text-neutral-300'
                  : product.stock_quantity === 0
                    ? 'bg-neutral-800 text-neutral-600 cursor-not-allowed'
                    : 'bg-lime-400 hover:bg-lime-300 text-neutral-950'
              "
            >
              {{
                addedToCart
                  ? "✓ Added to Cart"
                  : product.stock_quantity === 0
                    ? "Out of Stock"
                    : "Add to Cart"
              }}
            </button>
          </div>

          <router-link
            to="/cart"
            class="block text-center font-mono text-xs uppercase tracking-widest text-neutral-500 hover:text-lime-400 transition-colors py-2"
            >View Cart →</router-link
          >

          <div
            v-if="product.brand_tier"
            class="mt-8 pt-8 border-t border-neutral-800"
          >
            <div
              class="font-mono text-xs uppercase tracking-widest text-neutral-500 mb-2"
            >
              Brand Tier
            </div>
            <div class="flex items-center gap-2">
              <span
                v-for="n in 5"
                :key="n"
                class="w-6 h-1"
                :class="
                  n <= product.brand_tier ? 'bg-lime-400' : 'bg-neutral-800'
                "
              ></span>
              <span class="font-mono text-xs text-neutral-500 ml-2">{{
                product.brand_name
              }}</span>
            </div>
          </div>
        </div>
      </div>

      <div class="mt-16 pt-8 border-t border-neutral-800">
        <button
          @click="router.back()"
          class="font-mono text-xs uppercase tracking-widest text-neutral-500 hover:text-lime-400 transition-colors"
        >
          ← Back
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
</style>
