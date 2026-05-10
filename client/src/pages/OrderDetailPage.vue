<script setup>
import { onMounted, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import api, { fileUrl } from '@/api'

const route   = useRoute()
const router  = useRouter()
const order   = ref(null)
const items   = ref([])
const loading = ref(true)
const error   = ref(null)
const uploading  = ref(false)
const uploadDone = ref(false)

onMounted(async () => {
  try {
    const { data } = await api.get(`/orders/my-orders/${route.params.id}`)
    order.value = data.order
    items.value = data.items || []
  } catch {
    error.value = 'Order not found.'
  } finally {
    loading.value = false
  }
})

async function uploadProof(e) {
  const file = e.target.files[0]
  if (!file) return
  uploading.value = true
  try {
    const form = new FormData()
    form.append('file', file)
    await api.post(`/orders/${route.params.id}/payment-proof`, form, {
      headers: { 'Content-Type': 'multipart/form-data' }
    })
    uploadDone.value = true
    const { data } = await api.get(`/orders/my-orders/${route.params.id}`)
    order.value = data.order
    items.value = data.items || []
  } catch {
    alert('Upload failed. Please try again.')
  } finally {
    uploading.value = false
  }
}

const fmt     = (n) => '₱' + Number(n).toLocaleString()
const fmtDate = (d) => new Date(d).toLocaleDateString('en-PH', { year:'numeric', month:'short', day:'numeric', hour:'2-digit', minute:'2-digit' })
</script>

<template>
  <div class="fade-in max-w-3xl mx-auto px-6 py-12">
    <button @click="router.push('/orders')" class="text-sm text-stone-500 hover:text-stone-800 mb-8 flex items-center gap-1">← My Orders</button>

    <div v-if="loading" class="flex justify-center py-24"><span class="spinner"></span></div>
    <div v-else-if="error" class="text-center py-24 text-stone-500">{{ error }}</div>

    <div v-else-if="order">
      <div class="flex items-start justify-between flex-wrap gap-4 mb-8">
        <div>
          <p class="eyebrow mb-1">Order confirmed</p>
          <h1 class="font-display text-4xl tracking-tight">Order #{{ order.id }}</h1>
          <p class="text-sm text-stone-500 mt-1">{{ fmtDate(order.created_at) }}</p>
        </div>
        <span :class="`badge-${order.status}`">{{ order.status?.replace('_',' ') }}</span>
      </div>

      <!-- Items -->
      <div class="bg-white border border-stone-200 rounded-lg divide-y divide-stone-100 mb-6">
        <div v-for="item in items" :key="item.product_id" class="flex gap-4 p-4">
          <div class="w-16 h-16 bg-cream-deep rounded border border-stone-100 flex-shrink-0 overflow-hidden">
            <img v-if="item.image_url" :src="fileUrl(item.image_url)" class="w-full h-full object-cover" />
            <div v-else class="w-full h-full flex items-center justify-center text-stone-300 text-xl">🚲</div>
          </div>
          <div class="flex-1">
            <p class="font-medium">{{ item.name }}</p>
            <p class="text-sm text-stone-500">Qty: {{ item.quantity }} × {{ fmt(item.price_at_purchase) }}</p>
          </div>
          <p class="font-medium">{{ fmt(item.quantity * item.price_at_purchase) }}</p>
        </div>
        <div class="flex justify-between p-4 font-medium">
          <span>Total</span>
          <span class="text-clay-700 font-display text-xl">{{ fmt(order.total_amount) }}</span>
        </div>
      </div>

      <!-- Delivery -->
      <div class="bg-white border border-stone-200 rounded-lg p-5 mb-6">
        <h3 class="font-medium mb-2">Delivery address</h3>
        <p class="text-sm text-stone-600">{{ order.delivery_address || 'Pickup' }}</p>
      </div>

      <!-- Payment proof -->
      <div v-if="order.payment_method !== 'cod'" class="bg-white border border-stone-200 rounded-lg p-5">
        <h3 class="font-medium mb-3">Payment proof</h3>
        <div v-if="order.payment_screenshot_url">
          <img :src="fileUrl(order.payment_screenshot_url)" class="max-w-xs rounded border border-stone-200" />
          <p class="text-xs text-stone-500 mt-2">
            Status: <span :class="`badge-${order.payment_status}`">{{ order.payment_status?.replace('_',' ') }}</span>
          </p>
        </div>
        <div v-else>
          <p class="text-sm text-stone-600 mb-3">Upload your GCash/Maya payment screenshot.</p>
          <label class="btn-secondary cursor-pointer">
            <span v-if="uploading">Uploading…</span>
            <span v-else-if="uploadDone">✓ Uploaded</span>
            <span v-else>Upload screenshot</span>
            <input type="file" accept="image/*" class="hidden" @change="uploadProof" :disabled="uploading" />
          </label>
        </div>
      </div>
    </div>
  </div>
</template>