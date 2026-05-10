<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useCartStore } from '@/stores/cart'
import { useAuthStore } from '@/stores/auth'
import api from '@/api'

const router = useRouter()
const cart   = useCartStore()
const auth   = useAuthStore()

const method    = ref('gcash')
const address   = ref('')
const notes     = ref('')
const loading   = ref(false)
const error     = ref('')

const fmt = (n) => '₱' + Number(n).toLocaleString()

const paymentMethods = [
  { key: 'gcash', label: 'GCash' },
  { key: 'maya',  label: 'Maya' },
  { key: 'cod',   label: 'Cash on Delivery' },
]

const needsQR = computed(() => method.value === 'gcash' || method.value === 'maya')
async function placeOrder() {
  if (!address.value.trim()) { error.value = 'Please enter a delivery address.'; return }
  if (cart.items.length === 0) { error.value = 'Your cart is empty.'; return }
  error.value = ''
  loading.value = true
  try {
    // Step 1: sync local cart to backend
    for (const item of cart.items) {
      await api.post('/orders/cart/add', {
        product_id: item.id,
        quantity: item.qty,
      })
    }

    // Step 2: checkout
    const { data } = await api.post('/orders/checkout', {
      fulfillment_type: 'delivery',
      payment_method: method.value,
      delivery_address: address.value.trim(),
    })

    cart.clear()
    router.push(`/orders/${data.order_id}`)
  } catch (err) {
    error.value = err.response?.data?.detail || 'Could not place order. Please try again.'
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="fade-in max-w-4xl mx-auto px-6 py-12">
    <p class="eyebrow mb-2">Almost there</p>
    <h1 class="font-display text-4xl tracking-tight mb-8">Checkout</h1>

    <div v-if="cart.items.length === 0" class="text-center py-24">
      <p class="text-stone-500 mb-4">Nothing in your cart.</p>
      <RouterLink to="/catalog" class="btn-primary">Browse catalog</RouterLink>
    </div>

    <div v-else class="grid md:grid-cols-3 gap-8">
      <!-- Form -->
      <div class="md:col-span-2 space-y-6">

        <!-- Delivery -->
        <div class="bg-white border border-stone-200 rounded-lg p-6">
          <h2 class="font-display text-xl mb-4">Delivery details</h2>
          <div class="space-y-4">
            <div>
              <label class="input-label">Full name</label>
              <input :value="auth.user?.name" readonly class="input opacity-60 bg-stone-50 cursor-default" />
            </div>
            <div>
              <label class="input-label">Delivery address</label>
              <textarea v-model="address" rows="3" class="input resize-none" placeholder="Street, Barangay, City, Province" />
            </div>
            <div>
              <label class="input-label">Order notes (optional)</label>
              <input v-model="notes" type="text" class="input" placeholder="e.g. Call before delivery" />
            </div>
          </div>
        </div>

        <!-- Payment -->
        <div class="bg-white border border-stone-200 rounded-lg p-6">
          <h2 class="font-display text-xl mb-4">Payment method</h2>
          <div class="grid grid-cols-3 gap-3 mb-4">
            <button
              v-for="pm in paymentMethods" :key="pm.key"
              @click="method = pm.key"
              :class="['py-2.5 rounded border text-sm font-medium transition-all',
                method === pm.key
                  ? 'border-clay-600 bg-clay-50 text-clay-800'
                  : 'border-stone-200 text-stone-600 hover:border-stone-400']"
            >{{ pm.label }}</button>
          </div>

          <div v-if="needsQR" class="flex flex-col items-center gap-3 p-6 bg-cream-deep rounded-lg border border-stone-200">
            <div class="w-36 h-36 bg-white border border-stone-300 rounded flex items-center justify-center text-stone-400 text-xs text-center p-2">
              QR code will appear here once admin uploads it in Settings
            </div>
            <p class="text-xs text-stone-500 text-center">
              Send payment to <strong>{{ method === 'gcash' ? 'GCash' : 'Maya' }}</strong> number, then upload your screenshot after ordering.
            </p>
          </div>

          <div v-else class="p-4 bg-amber-50 border border-amber-200 rounded text-sm text-amber-800">
            Pay the rider upon delivery. Exact change appreciated.
          </div>
        </div>

        <p v-if="error" class="text-sm text-red-700 bg-red-50 border border-red-200 px-3 py-2 rounded">{{ error }}</p>
      </div>

      <!-- Order summary -->
      <div>
        <div class="bg-white border border-stone-200 rounded-lg p-6 sticky top-24">
          <h2 class="font-display text-xl mb-4">Order summary</h2>
          <div class="space-y-2 mb-4">
            <div v-for="item in cart.items" :key="item.id" class="flex justify-between text-sm">
              <span class="text-stone-600 truncate mr-2">{{ item.name }} × {{ item.qty }}</span>
              <span class="whitespace-nowrap">₱{{ Number(item.price * item.qty).toLocaleString() }}</span>
            </div>
          </div>
          <div class="border-t border-stone-200 pt-3 flex justify-between font-medium">
            <span>Total</span>
            <span class="text-clay-700 font-display text-xl">{{ fmt(cart.total) }}</span>
          </div>
          <button
            @click="placeOrder"
            :disabled="loading"
            class="btn-primary w-full mt-5 !py-3"
          >
            <span v-if="loading">Placing order…</span>
            <span v-else>Place order</span>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>