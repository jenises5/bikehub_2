import { defineStore } from 'pinia'
import { computed, ref } from 'vue'
import api from '@/api'

export const useAuthStore = defineStore('auth', () => {
  // State (hydrated from localStorage)
  const token = ref(localStorage.getItem('token') || null)
  const user  = ref(JSON.parse(localStorage.getItem('user') || 'null'))

  // Computed
  const isLoggedIn = computed(() => !!token.value)
  const isAdmin    = computed(() => user.value?.role === 'admin')

  // Helper: persist current state to localStorage
  function persist() {
    if (token.value) localStorage.setItem('token', token.value)
    else localStorage.removeItem('token')
    if (user.value) localStorage.setItem('user', JSON.stringify(user.value))
    else localStorage.removeItem('user')
  }

  // Actions
  async function login(email, password) {
    const { data } = await api.post('/auth/login', { email, password })
    token.value = data.access_token
    user.value  = data.user
    persist()
    return user.value
  }

  async function register(name, email, password) {
    const { data } = await api.post('/auth/register', { name, email, password })
    return data
  }

  function logout() {
    token.value = null
    user.value = null
    persist()
  }

  return { token, user, isLoggedIn, isAdmin, login, register, logout }
})