<script setup>
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";
import api from "../services/api";
import { useCartStore } from "../stores/cart";
import { useUserStore } from "../stores/user";

const router = useRouter();
const cartStore = useCartStore();
const userStore = useUserStore();

const featuredBikes = ref([]);
const categories = ref([]);
const loading = ref(true);

const formatPrice = (n) => `₱${n.toLocaleString("en-PH")}`;
const formatCategory = (name) =>
  (name || "").replace(/_/g, " ").replace(/\b\w/g, (c) => c.toUpperCase());

function logout() {
  userStore.logout();
  router.push("/login");
}

onMounted(async () => {
  try {
    const [bikesRes, catsRes] = await Promise.all([
      api.get("/products/featured"),
      api.get("/products/categories"),
    ]);
    featuredBikes.value = bikesRes.data;
    categories.value = catsRes.data;
  } catch (err) {
    console.error("Failed to load homepage data:", err);
  } finally {
    loading.value = false;
  }
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
          <button
            aria-label="Search"
            class="text-neutral-400 hover:text-lime-400 transition-colors"
          >
            <svg
              class="w-5 h-5"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              stroke-width="2"
            >
              <circle cx="11" cy="11" r="8" />
              <path d="m21 21-4.3-4.3" />
            </svg>
          </button>
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

    <section class="relative overflow-hidden border-b border-neutral-800">
      <div
        class="absolute inset-0 opacity-[0.04] pointer-events-none"
        style="
          background-image:
            linear-gradient(to right, white 1px, transparent 1px),
            linear-gradient(to bottom, white 1px, transparent 1px);
          background-size: 64px 64px;
        "
      ></div>
      <div
        class="relative max-w-7xl mx-auto px-6 py-24 md:py-32 grid md:grid-cols-12 gap-8 items-center"
      >
        <div class="md:col-span-7">
          <div
            class="flex items-center gap-3 mb-8 font-mono text-xs uppercase tracking-widest text-neutral-500"
          >
            <span class="w-8 h-px bg-lime-400"></span
            ><span>EST. 2024 · CEBU, PH</span>
          </div>
          <h1
            class="font-display text-6xl md:text-8xl lg:text-9xl leading-[0.85] tracking-tight"
          >
            RIDE<br /><span class="text-neutral-500">WHAT YOU</span><br /><span
              class="text-lime-400"
              >BUILD.</span
            >
          </h1>
          <p class="mt-8 max-w-md text-lg text-neutral-400 leading-relaxed">
            Configure every component, frame to bar tape. Real-time
            compatibility scoring. Built in the Philippines.
          </p>
          <div class="mt-10 flex flex-wrap gap-4">
            <router-link
              to="/builder"
              class="group inline-flex items-center gap-3 bg-lime-400 hover:bg-lime-300 text-neutral-950 font-mono text-sm uppercase tracking-widest px-6 py-4 transition-colors"
              >Start Your Build<svg
                class="w-4 h-4 group-hover:translate-x-1 transition-transform"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                stroke-width="2.5"
              >
                <path d="M5 12h14M13 6l6 6-6 6" /></svg
            ></router-link>
            <router-link
              to="/shop"
              class="inline-flex items-center gap-3 border border-neutral-700 hover:border-lime-400 hover:text-lime-400 text-neutral-300 font-mono text-sm uppercase tracking-widest px-6 py-4 transition-colors"
              >Explore Bikes</router-link
            >
          </div>
        </div>
        <div class="md:col-span-5 md:pl-8">
          <div
            class="grid grid-cols-2 gap-px bg-neutral-800 border border-neutral-800"
          >
            <div class="bg-neutral-950 p-6">
              <div
                class="font-mono text-[10px] uppercase tracking-widest text-neutral-500 mb-2"
              >
                Components
              </div>
              <div class="font-display text-4xl">500+</div>
            </div>
            <div class="bg-neutral-950 p-6">
              <div
                class="font-mono text-[10px] uppercase tracking-widest text-neutral-500 mb-2"
              >
                Custom builds
              </div>
              <div class="font-display text-4xl">2.4K</div>
            </div>
            <div class="bg-neutral-950 p-6">
              <div
                class="font-mono text-[10px] uppercase tracking-widest text-neutral-500 mb-2"
              >
                Free shipping
              </div>
              <div class="font-display text-4xl">₱5K+</div>
            </div>
            <div class="bg-neutral-950 p-6">
              <div
                class="font-mono text-[10px] uppercase tracking-widest text-neutral-500 mb-2"
              >
                Warranty
              </div>
              <div class="font-display text-4xl">30 DAY</div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <section class="border-b border-neutral-800">
      <div class="max-w-7xl mx-auto px-6 py-20">
        <div class="flex items-end justify-between mb-12">
          <div>
            <div
              class="font-mono text-xs uppercase tracking-widest text-neutral-500 mb-3"
            >
              // CATEGORIES
            </div>
            <h2 class="font-display text-4xl md:text-5xl">Find Your Terrain</h2>
          </div>
          <router-link
            to="/shop"
            class="hidden md:inline font-mono text-xs uppercase tracking-widest text-neutral-400 hover:text-lime-400 transition-colors"
            >View All →</router-link
          >
        </div>
        <div class="grid grid-cols-2 lg:grid-cols-4 gap-4">
          <router-link
            v-for="cat in categories"
            :key="cat.name"
            :to="`/shop?category=${cat.name.toLowerCase()}`"
            class="group relative aspect-[3/4] bg-neutral-900 border border-neutral-800 overflow-hidden hover:border-lime-400 transition-colors"
          >
            <div class="absolute inset-0 flex items-center justify-center">
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
            <div class="absolute bottom-0 left-0 right-0 p-5">
              <div class="flex items-end justify-between">
                <h3 class="font-display text-2xl">
                  {{ formatCategory(cat.name) }}
                </h3>
                <span class="font-mono text-xs text-neutral-500"
                  >{{ cat.count }} bikes</span
                >
              </div>
            </div>
          </router-link>
        </div>
      </div>
    </section>

    <section class="border-b border-neutral-800">
      <div class="max-w-7xl mx-auto px-6 py-20">
        <div class="flex items-end justify-between mb-12">
          <div>
            <div
              class="font-mono text-xs uppercase tracking-widest text-neutral-500 mb-3"
            >
              // FEATURED BUILDS
            </div>
            <h2 class="font-display text-4xl md:text-5xl">Hand-Picked Rides</h2>
          </div>
          <router-link
            to="/shop"
            class="hidden md:inline font-mono text-xs uppercase tracking-widest text-neutral-400 hover:text-lime-400 transition-colors"
            >All Builds →</router-link
          >
        </div>
        <div class="grid md:grid-cols-3 gap-6">
          <article
            v-for="bike in featuredBikes"
            :key="bike.id"
            class="group bg-neutral-900 border border-neutral-800 hover:border-lime-400 transition-colors"
          >
            <div
              class="aspect-[4/3] relative overflow-hidden bg-neutral-950 border-b border-neutral-800"
            >
              <div class="absolute inset-0 flex items-center justify-center">
                <svg
                  viewBox="0 0 200 120"
                  class="w-3/4 text-neutral-700 group-hover:text-lime-400 transition-colors"
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
              <span
                class="absolute top-4 left-4 font-mono text-[10px] uppercase tracking-widest bg-neutral-950/80 px-2 py-1 border border-neutral-800"
                >{{ formatCategory(bike.category) }}</span
              >
            </div>
            <div class="p-6">
              <h3 class="font-display text-2xl mb-4">{{ bike.name }}</h3>
              <div class="grid grid-cols-2 gap-3 mb-6 font-mono text-xs">
                <div>
                  <div class="text-neutral-500 uppercase tracking-wider mb-1">
                    Frame Size
                  </div>
                  <div class="text-neutral-200">
                    {{ bike.frame_size || "—" }}
                  </div>
                </div>
                <div>
                  <div class="text-neutral-500 uppercase tracking-wider mb-1">
                    Style
                  </div>
                  <div class="text-neutral-200">
                    {{ formatCategory(bike.riding_style || "—") }}
                  </div>
                </div>
              </div>
              <div
                class="flex items-baseline justify-between pt-4 border-t border-neutral-800"
              >
                <div class="font-display text-3xl text-lime-400">
                  {{ formatPrice(bike.price) }}
                </div>
                <router-link
                  :to="`/bike/${bike.id}`"
                  class="font-mono text-xs uppercase tracking-widest text-neutral-400 group-hover:text-lime-400 transition-colors"
                  >View →</router-link
                >
              </div>
            </div>
          </article>
        </div>
      </div>
    </section>

    <section class="relative border-b border-neutral-800 overflow-hidden">
      <div
        class="absolute inset-0 opacity-[0.06] pointer-events-none"
        style="
          background-image:
            linear-gradient(to right, #a3e635 1px, transparent 1px),
            linear-gradient(to bottom, #a3e635 1px, transparent 1px);
          background-size: 32px 32px;
        "
      ></div>
      <div
        class="relative max-w-7xl mx-auto px-6 py-24 grid md:grid-cols-2 gap-12 items-center"
      >
        <div>
          <div
            class="font-mono text-xs uppercase tracking-widest text-lime-400 mb-6"
          >
            // CUSTOM BUILDER
          </div>
          <h2 class="font-display text-5xl md:text-7xl leading-[0.9] mb-6">
            Build it<br /><span class="text-lime-400">your way.</span>
          </h2>
          <p class="text-lg text-neutral-400 mb-10 leading-relaxed max-w-md">
            Configure each component. Get a real-time compatibility score. Order
            with confidence — every part vetted by our shop.
          </p>
          <router-link
            to="/builder"
            class="group inline-flex items-center gap-3 bg-lime-400 hover:bg-lime-300 text-neutral-950 font-mono text-sm uppercase tracking-widest px-8 py-5 transition-colors"
            >Open Builder<svg
              class="w-4 h-4 group-hover:translate-x-1 transition-transform"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              stroke-width="2.5"
            >
              <path d="M5 12h14M13 6l6 6-6 6" /></svg
          ></router-link>
        </div>
        <div class="relative">
          <svg
            viewBox="0 0 400 280"
            class="w-full"
            fill="none"
            stroke-width="1.5"
          >
            <g stroke="#a3e635">
              <line x1="60" y1="200" x2="60" y2="240" stroke-dasharray="2 3" />
              <line x1="200" y1="40" x2="200" y2="80" stroke-dasharray="2 3" />
              <line
                x1="340"
                y1="200"
                x2="340"
                y2="240"
                stroke-dasharray="2 3"
              />
              <circle cx="60" cy="240" r="3" fill="#a3e635" />
              <circle cx="200" cy="40" r="3" fill="#a3e635" />
              <circle cx="340" cy="240" r="3" fill="#a3e635" />
            </g>
            <g font-family="monospace" font-size="10" fill="#a3e635">
              <text x="60" y="258" text-anchor="middle">WHEELS</text>
              <text x="200" y="32" text-anchor="middle">FRAME</text>
              <text x="340" y="258" text-anchor="middle">DRIVETRAIN</text>
            </g>
            <g stroke="#d4d4d4">
              <circle cx="80" cy="200" r="50" />
              <circle cx="320" cy="200" r="50" />
              <path
                d="M80 200 L200 70 L320 200 M200 70 L260 200 M200 70 L150 200 M150 200 L80 200"
              />
              <line x1="200" y1="70" x2="200" y2="120" />
            </g>
          </svg>
        </div>
      </div>
    </section>

    <section class="border-b border-neutral-800">
      <div
        class="max-w-7xl mx-auto px-6 py-12 grid grid-cols-2 md:grid-cols-4 gap-8"
      >
        <div>
          <div
            class="font-mono text-xs uppercase tracking-widest text-lime-400 mb-2"
          >
            01
          </div>
          <div class="font-display text-xl mb-1">Free Shipping</div>
          <div class="text-sm text-neutral-500">Orders over ₱5,000</div>
        </div>
        <div>
          <div
            class="font-mono text-xs uppercase tracking-widest text-lime-400 mb-2"
          >
            02
          </div>
          <div class="font-display text-xl mb-1">Expert Support</div>
          <div class="text-sm text-neutral-500">Real mechanics, real fast</div>
        </div>
        <div>
          <div
            class="font-mono text-xs uppercase tracking-widest text-lime-400 mb-2"
          >
            03
          </div>
          <div class="font-display text-xl mb-1">PayMongo Secure</div>
          <div class="text-sm text-neutral-500">Cards, GCash, Maya</div>
        </div>
        <div>
          <div
            class="font-mono text-xs uppercase tracking-widest text-lime-400 mb-2"
          >
            04
          </div>
          <div class="font-display text-xl mb-1">30-Day Warranty</div>
          <div class="text-sm text-neutral-500">No-questions returns</div>
        </div>
      </div>
    </section>

    <footer class="bg-neutral-950">
      <div class="max-w-7xl mx-auto px-6 py-16">
        <div class="grid grid-cols-2 md:grid-cols-5 gap-8 mb-12">
          <div class="md:col-span-2">
            <router-link to="/" class="font-display text-2xl tracking-tight"
              >BIKE<span class="text-lime-400">HUB</span></router-link
            >
            <p class="mt-4 text-sm text-neutral-500 max-w-xs leading-relaxed">
              Custom-built bikes from Cebu. Engineered to ride, designed to
              last.
            </p>
          </div>
          <div>
            <div
              class="font-mono text-xs uppercase tracking-widest text-neutral-300 mb-4"
            >
              Shop
            </div>
            <ul class="space-y-2 text-sm text-neutral-500">
              <li><a href="#" class="hover:text-lime-400">Road</a></li>
              <li><a href="#" class="hover:text-lime-400">Mountain</a></li>
              <li><a href="#" class="hover:text-lime-400">Gravel</a></li>
              <li><a href="#" class="hover:text-lime-400">Urban</a></li>
            </ul>
          </div>
          <div>
            <div
              class="font-mono text-xs uppercase tracking-widest text-neutral-300 mb-4"
            >
              Company
            </div>
            <ul class="space-y-2 text-sm text-neutral-500">
              <li><a href="#" class="hover:text-lime-400">About</a></li>
              <li><a href="#" class="hover:text-lime-400">Workshop</a></li>
              <li><a href="#" class="hover:text-lime-400">Press</a></li>
              <li><a href="#" class="hover:text-lime-400">Contact</a></li>
            </ul>
          </div>
          <div>
            <div
              class="font-mono text-xs uppercase tracking-widest text-neutral-300 mb-4"
            >
              Support
            </div>
            <ul class="space-y-2 text-sm text-neutral-500">
              <li><a href="#" class="hover:text-lime-400">Help Center</a></li>
              <li><a href="#" class="hover:text-lime-400">Shipping</a></li>
              <li><a href="#" class="hover:text-lime-400">Returns</a></li>
              <li><a href="#" class="hover:text-lime-400">Warranty</a></li>
            </ul>
          </div>
        </div>
        <div
          class="pt-8 border-t border-neutral-800 flex flex-col md:flex-row justify-between gap-4 font-mono text-xs text-neutral-500 uppercase tracking-widest"
        >
          <div>© 2026 BIKEHUB · EDGETECH · CEBU, PH</div>
          <div class="flex gap-6">
            <a href="#" class="hover:text-lime-400">Privacy</a
            ><a href="#" class="hover:text-lime-400">Terms</a
            ><a href="#" class="hover:text-lime-400">Cookies</a>
          </div>
        </div>
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
</style>
