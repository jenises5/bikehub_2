<<<<<<< HEAD
import { defineStore } from "pinia";
import { ref, computed } from "vue";

export const useCartStore = defineStore("cart", () => {
  const items = ref(JSON.parse(localStorage.getItem("cart") || "[]"));

  const count = computed(() =>
    items.value.reduce((sum, i) => sum + i.quantity, 0),
  );

  function setItems(newItems) {
    items.value = newItems;
    localStorage.setItem("cart", JSON.stringify(newItems));
  }

  function addItem(product, quantity = 1) {
    const existing = items.value.find((i) => i.id === product.id);
    if (existing) {
      existing.quantity += quantity;
    } else {
      items.value.push({ ...product, quantity });
    }
    localStorage.setItem("cart", JSON.stringify(items.value));
  }

  function removeItem(id) {
    items.value = items.value.filter((i) => i.id !== id);
    localStorage.setItem("cart", JSON.stringify(items.value));
  }

  function clear() {
    items.value = [];
    localStorage.removeItem("cart");
  }

  return { items, count, setItems, addItem, removeItem, clear };
});
=======
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
>>>>>>> 48da94096a2a516f3758e317689b63040e8a024f
