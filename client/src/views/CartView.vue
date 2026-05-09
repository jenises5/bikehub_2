<script setup>
import { ref, computed, onMounted } from "vue";
import { useRouter } from "vue-router";
import api from "../services/api";
import { useCartStore } from "../stores/cart";
import { useUserStore } from "../stores/user";

const router = useRouter();
const cartStore = useCartStore();
const userStore = useUserStore();

const loading = ref(true);
const checkingOut = ref(false);
const orderSuccess = ref(false);
const error = ref("");

const paymentMethod = ref("cod");
const fulfillmentType = ref("pickup");
const deliveryAddress = ref("");

const formatPrice = (n) => `₱${Number(n).toLocaleString("en-PH")}`;

const cartItems = computed(() => cartStore.items);

const subtotal = computed(() =>
  cartItems.value.reduce((sum, i) => sum + i.price * i.quantity, 0),
);

const shippingFee = computed(() =>
  fulfillmentType.value === "delivery" && subtotal.value < 5000 ? 250 : 0,
);

const total = computed(() => subtotal.value + shippingFee.value);

function logout() {
  userStore.logout();
  router.push("/login");
}

async function loadCart() {
  loading.value = true;
  if (userStore.isLoggedIn) {
    try {
      const res = await api.get("/cart");
      cartStore.setItems(
        res.data.map((i) => ({
          id: i.product_id,
          cart_item_id: i.id,
          name: i.name,
          price: i.price,
          image_url: i.image_url,
          stock_quantity: i.stock_quantity,
          quantity: i.quantity,
        })),
      );
    } catch (err) {
      error.value = "Failed to load cart.";
    }
  }
  loading.value = false;
}

function updateQuantity(item, qty) {
  if (qty < 1 || qty > item.stock_quantity) return;
  item.quantity = qty;
  cartStore.setItems([...cartStore.items]);
}

async function checkout() {
  if (!userStore.isLoggedIn) {
    router.push("/login");
    return;
  }
  if (fulfillmentType.value === "delivery" && !deliveryAddress.value.trim()) {
    error.value = "Please enter a delivery address.";
    return;
  }
  error.value = "";
  checkingOut.value = true;
  try {
    await api.post("/checkout", {
      payment_method: paymentMethod.value,
      fulfillment_type: fulfillmentType.value,
      delivery_address:
        fulfillmentType.value === "delivery" ? deliveryAddress.value : null,
    });
    orderSuccess.value = true;
    cartStore.clear();
  } catch (err) {
    error.value =
      err.response?.data?.detail || "Checkout failed. Please try again.";
  } finally {
    checkingOut.value = false;
  }
}

onMounted(loadCart);
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
      <div class="max-w-7xl mx-auto px-6 py-12">
        <div
          class="font-mono text-xs uppercase tracking-widest text-neutral-500 mb-3"
        >
          // CART
        </div>
        <h1 class="font-display text-5xl md:text-7xl">Your Cart</h1>
      </div>
    </div>

    <div v-if="orderSuccess" class="max-w-7xl mx-auto px-6 py-24 text-center">
      <div class="font-display text-6xl text-lime-400 mb-4">Order Placed!</div>
      <p class="text-neutral-400 font-mono text-sm mb-8">
        Thank you for your order. We'll contact you shortly.
      </p>
      <router-link
        to="/shop"
        class="inline-block bg-lime-400 hover:bg-lime-300 text-neutral-950 font-mono text-sm uppercase tracking-widest px-8 py-4 transition-colors"
        >Continue Shopping →</router-link
      >
    </div>

    <div v-else-if="loading" class="max-w-7xl mx-auto px-6 py-12">
      <div class="space-y-4">
        <div
          v-for="n in 3"
          :key="n"
          class="h-24 bg-neutral-900 animate-pulse"
        ></div>
      </div>
    </div>

    <div
      v-else-if="cartItems.length === 0"
      class="max-w-7xl mx-auto px-6 py-24 text-center"
    >
      <div class="font-display text-4xl text-neutral-700 mb-4">
        Your cart is empty
      </div>
      <router-link
        to="/shop"
        class="font-mono text-xs uppercase tracking-widest text-lime-400 hover:text-lime-300 transition-colors"
        >Browse Products →</router-link
      >
    </div>

    <div v-else class="max-w-7xl mx-auto px-6 py-12 grid md:grid-cols-3 gap-10">
      <div class="md:col-span-2 space-y-4">
        <div
          v-for="item in cartItems"
          :key="item.id"
          class="flex gap-4 bg-neutral-900 border border-neutral-800 p-4"
        >
          <div
            class="w-20 h-20 bg-neutral-950 border border-neutral-800 flex items-center justify-center shrink-0"
          >
            <img
              v-if="item.image_url"
              :src="item.image_url"
              :alt="item.name"
              class="w-full h-full object-cover"
            />
            <svg
              v-else
              viewBox="0 0 100 60"
              class="w-3/4 text-neutral-700"
              fill="none"
              stroke="currentColor"
              stroke-width="1.5"
            >
              <circle cx="22" cy="42" r="14" />
              <circle cx="78" cy="42" r="14" />
              <path d="M22 42 L48 12 L78 42 M48 12 L62 42 M48 12 L36 42" />
            </svg>
          </div>
          <div class="flex-1 min-w-0">
            <h3 class="font-display text-xl leading-tight mb-1">
              {{ item.name }}
            </h3>
            <div class="font-display text-lg text-lime-400">
              {{ formatPrice(item.price) }}
            </div>
          </div>
          <div class="flex flex-col items-end justify-between shrink-0">
            <button
              @click="cartStore.removeItem(item.id)"
              class="font-mono text-xs text-neutral-600 hover:text-red-400 transition-colors"
            >
              ✕
            </button>
            <div class="flex items-center border border-neutral-800">
              <button
                @click="updateQuantity(item, item.quantity - 1)"
                class="px-3 py-1 font-mono text-neutral-400 hover:text-lime-400 transition-colors"
              >
                −
              </button>
              <span class="px-3 py-1 font-mono text-sm">{{
                item.quantity
              }}</span>
              <button
                @click="updateQuantity(item, item.quantity + 1)"
                class="px-3 py-1 font-mono text-neutral-400 hover:text-lime-400 transition-colors"
              >
                +
              </button>
            </div>
            <div class="font-mono text-xs text-neutral-500">
              {{ formatPrice(item.price * item.quantity) }}
            </div>
          </div>
        </div>
        <button
          @click="cartStore.clear()"
          class="font-mono text-xs uppercase tracking-widest text-neutral-600 hover:text-red-400 transition-colors"
        >
          ✕ Clear Cart
        </button>
      </div>

      <div class="space-y-6">
        <div class="bg-neutral-900 border border-neutral-800 p-6">
          <div
            class="font-mono text-xs uppercase tracking-widest text-neutral-500 mb-4"
          >
            Order Summary
          </div>
          <div class="space-y-3 font-mono text-sm">
            <div class="flex justify-between">
              <span class="text-neutral-400">Subtotal</span
              ><span>{{ formatPrice(subtotal) }}</span>
            </div>
            <div class="flex justify-between">
              <span class="text-neutral-400">Shipping</span
              ><span :class="shippingFee === 0 ? 'text-lime-400' : ''">{{
                shippingFee === 0 ? "FREE" : formatPrice(shippingFee)
              }}</span>
            </div>
            <div
              class="flex justify-between pt-3 border-t border-neutral-800 font-display text-2xl"
            >
              <span>Total</span
              ><span class="text-lime-400">{{ formatPrice(total) }}</span>
            </div>
          </div>
        </div>

        <div class="bg-neutral-900 border border-neutral-800 p-6 space-y-5">
          <div
            class="font-mono text-xs uppercase tracking-widest text-neutral-500"
          >
            Checkout
          </div>
          <div>
            <div
              class="font-mono text-xs uppercase tracking-widest text-neutral-500 mb-2"
            >
              Fulfillment
            </div>
            <div class="flex border border-neutral-800">
              <button
                @click="fulfillmentType = 'pickup'"
                class="flex-1 font-mono text-xs uppercase tracking-widest py-2 transition-colors"
                :class="
                  fulfillmentType === 'pickup'
                    ? 'bg-lime-400 text-neutral-950'
                    : 'text-neutral-400 hover:text-neutral-100'
                "
              >
                Pickup
              </button>
              <button
                @click="fulfillmentType = 'delivery'"
                class="flex-1 font-mono text-xs uppercase tracking-widest py-2 transition-colors"
                :class="
                  fulfillmentType === 'delivery'
                    ? 'bg-lime-400 text-neutral-950'
                    : 'text-neutral-400 hover:text-neutral-100'
                "
              >
                Delivery
              </button>
            </div>
          </div>
          <div v-if="fulfillmentType === 'delivery'">
            <div
              class="font-mono text-xs uppercase tracking-widest text-neutral-500 mb-2"
            >
              Delivery Address
            </div>
            <textarea
              v-model="deliveryAddress"
              rows="3"
              placeholder="Enter your full address…"
              class="w-full bg-neutral-950 border border-neutral-800 text-neutral-100 font-mono text-xs px-3 py-2 focus:outline-none focus:border-lime-400 transition-colors placeholder:text-neutral-600 resize-none"
            ></textarea>
          </div>
          <div>
            <div
              class="font-mono text-xs uppercase tracking-widest text-neutral-500 mb-2"
            >
              Payment
            </div>
            <div class="space-y-2">
              <label
                v-for="method in ['cod', 'gcash', 'maya']"
                :key="method"
                class="flex items-center gap-3 cursor-pointer group"
              >
                <div
                  class="w-4 h-4 border transition-colors flex items-center justify-center"
                  :class="
                    paymentMethod === method
                      ? 'border-lime-400 bg-lime-400'
                      : 'border-neutral-700 group-hover:border-neutral-400'
                  "
                  @click="paymentMethod = method"
                >
                  <svg
                    v-if="paymentMethod === method"
                    viewBox="0 0 12 12"
                    class="w-2.5 h-2.5"
                    fill="none"
                    stroke="#171717"
                    stroke-width="2"
                  >
                    <path d="M2 6l3 3 5-5" />
                  </svg>
                </div>
                <span
                  class="font-mono text-xs uppercase tracking-widest text-neutral-300"
                  @click="paymentMethod = method"
                  >{{
                    method === "cod"
                      ? "Cash on Delivery"
                      : method === "gcash"
                        ? "GCash"
                        : "Maya"
                  }}</span
                >
              </label>
            </div>
          </div>
          <div
            v-if="error"
            class="font-mono text-xs text-red-400 border border-red-900 bg-red-950/50 px-3 py-2"
          >
            {{ error }}
          </div>
          <button
            @click="checkout"
            :disabled="checkingOut"
            class="w-full font-mono text-sm uppercase tracking-widest py-4 transition-colors"
            :class="
              checkingOut
                ? 'bg-neutral-700 text-neutral-500'
                : 'bg-lime-400 hover:bg-lime-300 text-neutral-950'
            "
          >
            {{
              !userStore.isLoggedIn
                ? "Login to Checkout →"
                : checkingOut
                  ? "Placing Order…"
                  : "Place Order →"
            }}
          </button>
          <p
            v-if="!userStore.isLoggedIn"
            class="font-mono text-xs text-neutral-600 text-center"
          >
            You need to be logged in to place an order.
          </p>
        </div>
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
