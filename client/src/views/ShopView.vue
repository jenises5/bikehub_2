<script setup>
import { ref, computed, onMounted, watch } from "vue";
import { useRoute, useRouter } from "vue-router";
import api from "../services/api";
import { useCartStore } from "../stores/cart";
import { useUserStore } from "../stores/user";

const route = useRoute();
const router = useRouter();
const cartStore = useCartStore();
const userStore = useUserStore();

const products = ref([]);
const categories = ref([]);
const loading = ref(true);
const selectedCategory = ref(route.query.category || "");
const selectedStyle = ref("");
const sortBy = ref("newest");
const searchQuery = ref("");

const formatPrice = (n) => `₱${Number(n).toLocaleString("en-PH")}`;
const formatCategory = (name) =>
  (name || "").replace(/_/g, " ").replace(/\b\w/g, (c) => c.toUpperCase());

const ridingStyles = ["road", "mountain", "gravel", "urban", "commute"];

function logout() {
  userStore.logout();
  router.push("/login");
}

async function fetchProducts() {
  loading.value = true;
  try {
    const params = {};
    if (selectedCategory.value) params.category = selectedCategory.value;
    if (selectedStyle.value) params.riding_style = selectedStyle.value;
    const res = await api.get("/products/", { params });
    products.value = res.data;
  } catch (err) {
    console.error("Failed to fetch products:", err);
  } finally {
    loading.value = false;
  }
}

async function fetchCategories() {
  try {
    const res = await api.get("/products/categories");
    categories.value = res.data;
  } catch (err) {
    console.error("Failed to fetch categories:", err);
  }
}

const filteredProducts = computed(() => {
  let list = [...products.value];
  if (searchQuery.value) {
    const q = searchQuery.value.toLowerCase();
    list = list.filter(
      (p) =>
        p.name.toLowerCase().includes(q) ||
        (p.description || "").toLowerCase().includes(q),
    );
  }
  if (sortBy.value === "price-asc") list.sort((a, b) => a.price - b.price);
  else if (sortBy.value === "price-desc")
    list.sort((a, b) => b.price - a.price);
  else if (sortBy.value === "name")
    list.sort((a, b) => a.name.localeCompare(b.name));
  else list.sort((a, b) => new Date(b.created_at) - new Date(a.created_at));
  return list;
});

function selectCategory(cat) {
  selectedCategory.value = cat;
  router.replace({ query: cat ? { category: cat } : {} });
  fetchProducts();
}

function clearFilters() {
  selectedCategory.value = "";
  selectedStyle.value = "";
  searchQuery.value = "";
  router.replace({ query: {} });
  fetchProducts();
}

watch(selectedStyle, fetchProducts);
onMounted(() => {
  fetchProducts();
  fetchCategories();
});
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
            <router-link to="/shop" class="text-lime-400">Shop</router-link>
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
      <div class="max-w-7xl mx-auto px-6 py-12">
        <div
          class="font-mono text-xs uppercase tracking-widest text-neutral-500 mb-3"
        >
          // SHOP
        </div>
        <h1 class="font-display text-5xl md:text-7xl">All Products</h1>
      </div>
    </div>

    <div class="max-w-7xl mx-auto px-6 py-10 flex flex-col md:flex-row gap-10">
      <aside class="w-full md:w-56 shrink-0">
        <div class="mb-8">
          <div
            class="font-mono text-xs uppercase tracking-widest text-neutral-500 mb-3"
          >
            Search
          </div>
          <input
            v-model="searchQuery"
            type="text"
            placeholder="Search products…"
            class="w-full bg-neutral-900 border border-neutral-800 text-neutral-100 font-mono text-xs px-3 py-2 focus:outline-none focus:border-lime-400 transition-colors placeholder:text-neutral-600"
          />
        </div>
        <div class="mb-8">
          <div
            class="font-mono text-xs uppercase tracking-widest text-neutral-500 mb-3"
          >
            Category
          </div>
          <ul class="space-y-1">
            <li>
              <button
                @click="selectCategory('')"
                class="w-full text-left font-mono text-xs uppercase tracking-widest px-2 py-1.5 transition-colors"
                :class="
                  selectedCategory === ''
                    ? 'text-lime-400'
                    : 'text-neutral-400 hover:text-neutral-100'
                "
              >
                All
              </button>
            </li>
            <li v-for="cat in categories" :key="cat.name">
              <button
                @click="selectCategory(cat.name)"
                class="w-full text-left font-mono text-xs uppercase tracking-widest px-2 py-1.5 transition-colors flex items-center justify-between"
                :class="
                  selectedCategory === cat.name
                    ? 'text-lime-400'
                    : 'text-neutral-400 hover:text-neutral-100'
                "
              >
                <span>{{ formatCategory(cat.name) }}</span
                ><span class="text-neutral-600">{{ cat.count }}</span>
              </button>
            </li>
          </ul>
        </div>
        <div class="mb-8">
          <div
            class="font-mono text-xs uppercase tracking-widest text-neutral-500 mb-3"
          >
            Riding Style
          </div>
          <ul class="space-y-1">
            <li>
              <button
                @click="selectedStyle = ''"
                class="w-full text-left font-mono text-xs uppercase tracking-widest px-2 py-1.5 transition-colors"
                :class="
                  selectedStyle === ''
                    ? 'text-lime-400'
                    : 'text-neutral-400 hover:text-neutral-100'
                "
              >
                All
              </button>
            </li>
            <li v-for="style in ridingStyles" :key="style">
              <button
                @click="selectedStyle = style"
                class="w-full text-left font-mono text-xs uppercase tracking-widest px-2 py-1.5 transition-colors"
                :class="
                  selectedStyle === style
                    ? 'text-lime-400'
                    : 'text-neutral-400 hover:text-neutral-100'
                "
              >
                {{ formatCategory(style) }}
              </button>
            </li>
          </ul>
        </div>
        <button
          v-if="selectedCategory || selectedStyle || searchQuery"
          @click="clearFilters"
          class="font-mono text-xs uppercase tracking-widest text-neutral-500 hover:text-lime-400 transition-colors"
        >
          ✕ Clear Filters
        </button>
      </aside>

      <div class="flex-1 min-w-0">
        <div class="flex items-center justify-between mb-6">
          <span
            class="font-mono text-xs text-neutral-500 uppercase tracking-widest"
            >{{ filteredProducts.length }} products</span
          >
          <select
            v-model="sortBy"
            class="bg-neutral-900 border border-neutral-800 text-neutral-400 font-mono text-xs uppercase tracking-widest px-3 py-2 focus:outline-none focus:border-lime-400 transition-colors"
          >
            <option value="newest">Newest</option>
            <option value="price-asc">Price: Low → High</option>
            <option value="price-desc">Price: High → Low</option>
            <option value="name">Name A–Z</option>
          </select>
        </div>
        <div v-if="loading" class="grid grid-cols-2 md:grid-cols-3 gap-4">
          <div
            v-for="n in 6"
            :key="n"
            class="bg-neutral-900 border border-neutral-800 animate-pulse aspect-[3/4]"
          ></div>
        </div>
        <div
          v-else-if="filteredProducts.length === 0"
          class="py-24 text-center"
        >
          <div class="font-display text-4xl text-neutral-700 mb-4">
            No products found
          </div>
          <button
            @click="clearFilters"
            class="font-mono text-xs uppercase tracking-widest text-lime-400 hover:text-lime-300 transition-colors"
          >
            Clear filters
          </button>
        </div>
        <div v-else class="grid grid-cols-2 md:grid-cols-3 gap-4">
          <router-link
            v-for="product in filteredProducts"
            :key="product.id"
            :to="`/bike/${product.id}`"
            class="group bg-neutral-900 border border-neutral-800 hover:border-lime-400 transition-colors"
          >
            <div
              class="aspect-square relative overflow-hidden bg-neutral-950 border-b border-neutral-800"
            >
              <img
                v-if="product.image_url"
                :src="product.image_url"
                :alt="product.name"
                class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500"
              />
              <div
                v-else
                class="absolute inset-0 flex items-center justify-center"
              >
                <svg
                  viewBox="0 0 100 60"
                  class="w-2/3 text-neutral-700 group-hover:text-lime-400 transition-colors"
                  fill="none"
                  stroke="currentColor"
                  stroke-width="1.5"
                >
                  <circle cx="22" cy="42" r="14" />
                  <circle cx="78" cy="42" r="14" />
                  <path d="M22 42 L48 12 L78 42 M48 12 L62 42 M48 12 L36 42" />
                </svg>
              </div>
              <span
                class="absolute top-3 left-3 font-mono text-[10px] uppercase tracking-widest bg-neutral-950/80 px-2 py-1 border border-neutral-800"
                >{{ formatCategory(product.category) }}</span
              >
              <span
                v-if="product.stock_quantity <= product.low_stock_threshold"
                class="absolute top-3 right-3 font-mono text-[10px] uppercase tracking-widest bg-red-900/80 text-red-400 px-2 py-1 border border-red-800"
                >Low Stock</span
              >
            </div>
            <div class="p-4">
              <h3 class="font-display text-xl leading-tight mb-1">
                {{ product.name }}
              </h3>
              <p class="font-mono text-xs text-neutral-500 mb-3 line-clamp-2">
                {{ product.description }}
              </p>
              <div class="flex items-baseline justify-between">
                <span class="font-display text-2xl text-lime-400">{{
                  formatPrice(product.price)
                }}</span>
                <span
                  class="font-mono text-xs uppercase tracking-widest text-neutral-500 group-hover:text-lime-400 transition-colors"
                  >View →</span
                >
              </div>
            </div>
          </router-link>
        </div>
      </div>
    </div>

    <footer class="border-t border-neutral-800 mt-16">
      <div
        class="max-w-7xl mx-auto px-6 py-8 flex flex-col md:flex-row justify-between gap-4 font-mono text-xs text-neutral-500 uppercase tracking-widest"
      >
        <div>© 2026 BIKEHUB · EDGETECH · CEBU, PH</div>
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
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>
