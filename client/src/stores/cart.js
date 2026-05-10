import { defineStore } from 'pinia'
import { computed, ref, watch } from 'vue'

export const useCartStore = defineStore('cart', () => {
  const items = ref(JSON.parse(localStorage.getItem('cart') || '[]'))

  watch(items, (v) => localStorage.setItem('cart', JSON.stringify(v)), { deep: true })

  const count   = computed(() => items.value.reduce((s, i) => s + i.qty, 0))
  const total   = computed(() => items.value.reduce((s, i) => s + i.price * i.qty, 0))

  function add(product, qty = 1) {
    const existing = items.value.find(i => i.id === product.id)
    if (existing) existing.qty += qty
    else items.value.push({ id: product.id, name: product.name, price: product.price, image: product.images?.[0] ?? null, qty })
  }

  function remove(id) { items.value = items.value.filter(i => i.id !== id) }

  function updateQty(id, qty) {
    const item = items.value.find(i => i.id === id)
    if (item) item.qty = Math.max(1, qty)
  }

  function clear() { items.value = [] }

  return { items, count, total, add, remove, updateQty, clear }
})