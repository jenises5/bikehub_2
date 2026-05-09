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
