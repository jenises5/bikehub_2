<script setup>
import { useCartStore } from '@/stores/cart'
import { RouterLink } from 'vue-router'
import { fileUrl } from '@/api'

const cart = useCartStore()
const fmt  = (n) => '₱' + Number(n).toLocaleString()
</script>

<template>
  <div class="fade-in max-w-4xl mx-auto px-6 py-12">
    <p class="eyebrow mb-2">Your cart</p>
    <h1 class="font-display text-4xl tracking-tight mb-8">Cart</h1>

    <div v-if="cart.items.length === 0" class="text-center py-24">
      <p class="text-stone-500 mb-4">Your cart is empty.</p>
      <RouterLink to="/catalog" class="btn-primary">Browse catalog</RouterLink>
    </div>

    <div v-else class="grid md:grid-cols-3 gap-8">
      <!-- Items -->
      <div class="md:col-span-2 space-y-4">
        <div
          v-for="item in cart.items" :key="item.id"
          class="flex gap-4 p-4 bg-white border border-stone-200 rounded-lg"
        >
          <div class="w-20 h-20 bg-cream-deep rounded-lg overflow-hidden flex-shrink-0 border border-stone-100">
            <img v-if="item.image" :src="fileUrl(item.image)" class="w-full h-full object-cover" />
            <div v-else class="w-full h-full flex items-center justify-center text-stone-300 text-2xl">🚲</div>
          </div>
          <div class="flex-1 min-w-0">
            <p class="font-medium text-stone-900 truncate">{{ item.name }}</p>
            <p class="text-clay-700 font-display text-lg">{{ fmt(item.price) }}</p>
            <div class="flex items-center gap-2 mt-2">
              <div class="flex items-center border border-stone-200 rounded">
                <button @click="cart.updateQty(item.id, item.qty-1)" class="px-2 py-1 text-stone-500 hover:bg-stone-50 text-sm">−</button>
                <span class="px-3 text-sm">{{ item.qty }}</span>
                <button @click="cart.updateQty(item.id, item.qty+1)" class="px-2 py-1 text-stone-500 hover:bg-stone-50 text-sm">+</button>
              </div>
              <button @click="cart.remove(item.id)" class="text-xs text-red-600 hover:underline ml-2">Remove</button>
            </div>
          </div>
          <p class="font-medium text-stone-900 whitespace-nowrap">{{ fmt(item.price * item.qty) }}</p>
        </div>
      </div>

      <!-- Summary -->
      <div class="md:col-span-1">
        <div class="bg-white border border-stone-200 rounded-lg p-6 sticky top-24">
          <h2 class="font-display text-xl mb-4">Summary</h2>
          <div class="flex justify-between text-sm mb-2">
            <span class="text-stone-500">Subtotal ({{ cart.count }} item{{ cart.count !== 1 ? 's' : '' }})</span>
            <span>{{ fmt(cart.total) }}</span>
          </div>
          <div class="border-t border-stone-200 pt-3 mt-3 flex justify-between font-medium">
            <span>Total</span>
            <span class="text-clay-700 font-display text-xl">{{ fmt(cart.total) }}</span>
          </div>
          <RouterLink to="/checkout" class="btn-primary w-full mt-5 !py-3 text-center">
            Proceed to checkout
          </RouterLink>
          <RouterLink to="/catalog" class="btn-ghost w-full mt-2 !py-2 text-center text-sm">
            Continue shopping
          </RouterLink>
        </div>
      </div>
    </div>
  </div>
</template>