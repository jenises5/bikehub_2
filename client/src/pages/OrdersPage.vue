<script setup>
import { onMounted, ref } from 'vue'
import { RouterLink } from 'vue-router'
import api from '@/api'

const orders  = ref([])
const loading = ref(true)
const error   = ref(null)

onMounted(async () => {
  try {
    const { data } = await api.get('/orders/my-orders')
    orders.value = data || []
  } catch {
    error.value = 'Could not load orders.'
  } finally {
    loading.value = false
  }
})

const fmt     = (n) => '₱' + Number(n).toLocaleString()
const fmtDate = (d) => new Date(d).toLocaleDateString('en-PH', { year:'numeric', month:'short', day:'numeric' })
</script>

<template>
  <div class="fade-in max-w-4xl mx-auto px-6 py-12">
    <p class="eyebrow mb-2">Account</p>
    <h1 class="font-display text-4xl tracking-tight mb-8">My Orders</h1>

    <div v-if="loading" class="flex justify-center py-24"><span class="spinner"></span></div>
    <div v-else-if="error" class="text-center py-24 text-stone-500">{{ error }}</div>
    <div v-else-if="orders.length === 0" class="text-center py-24">
      <p class="text-stone-500 mb-4">You haven't placed any orders yet.</p>
      <RouterLink to="/catalog" class="btn-primary">Start shopping</RouterLink>
    </div>

    <div v-else class="space-y-4">
      <RouterLink
        v-for="order in orders" :key="order.id"
        :to="`/orders/${order.id}`"
        class="block bg-white border border-stone-200 rounded-lg p-5 hover:border-stone-300 hover:shadow-soft transition-all"
      >
        <div class="flex items-start justify-between gap-4 flex-wrap">
          <div>
            <p class="font-medium text-stone-900 mb-1">Order #{{ order.id }}</p>
            <p class="text-sm text-stone-500">{{ fmtDate(order.created_at) }}</p>
            <p class="text-sm text-stone-600 mt-1 capitalize">{{ order.payment_method }} · {{ order.fulfillment_type }}</p>
          </div>
          <div class="text-right">
            <p class="font-display text-xl text-clay-700">{{ fmt(order.total_amount) }}</p>
            <span :class="`badge-${order.status} mt-1 inline-block`">{{ order.status?.replace('_',' ') }}</span>
          </div>
        </div>
      </RouterLink>
    </div>
  </div>
</template>