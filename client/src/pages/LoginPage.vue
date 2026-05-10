<script setup>
import { ref } from 'vue'
import { useRouter, useRoute, RouterLink } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const route = useRoute()
const auth = useAuthStore()

const email = ref('')
const password = ref('')
const loading = ref(false)
const error = ref('')

async function handleSubmit() {
  error.value = ''
  if (!email.value || !password.value) {
    error.value = 'Please enter your email and password.'
    return
  }
  loading.value = true
  try {
    const user = await auth.login(email.value.trim(), password.value)
    if (user?.role === 'admin') {
      router.push('/admin')
    } else {
      const redirect = route.query.redirect
      router.push(typeof redirect === 'string' ? redirect : '/')
    }
  } catch (err) {
    error.value = err.response?.data?.detail || 'Invalid email or password.'
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="fade-in min-h-[calc(100vh-4rem)] grid md:grid-cols-2">
    <!-- Left editorial side -->
    <div class="hidden md:flex bg-cream-deep border-r border-stone-200 p-12 flex-col justify-between">
      <RouterLink to="/" class="flex items-center gap-2 w-fit">
        <span class="w-8 h-8 rounded-md bg-clay-700 text-cream flex items-center justify-center font-display text-lg leading-none">B</span>
        <span class="font-display text-xl text-stone-900">BikeHub</span>
      </RouterLink>

      <div class="max-w-md">
        <p class="eyebrow mb-4">Welcome back</p>
        <h1 class="font-display text-5xl leading-[1.05] tracking-tight text-stone-900">
          Pick up where you<br/>
          <span class="italic">left off.</span>
        </h1>
        <p class="text-stone-600 mt-6 leading-relaxed">
          Your saved builds, wishlist, and order history are waiting.
        </p>
      </div>

      <p class="text-xs text-stone-500">© 2026 BikeHub · CTU-Main</p>
    </div>

    <!-- Form side -->
    <div class="flex items-center justify-center p-6 md:p-12">
      <div class="w-full max-w-sm">
        <h2 class="font-display text-3xl tracking-tight mb-2">Log in</h2>
        <p class="text-sm text-stone-600 mb-8">
          Don't have an account?
          <RouterLink to="/register" class="text-clay-700 font-medium hover:underline">
            Create one
          </RouterLink>
        </p>

        <form @submit.prevent="handleSubmit" class="space-y-5" novalidate>
          <div>
            <label class="input-label" for="email">Email</label>
            <input
              id="email"
              v-model="email"
              type="email"
              autocomplete="email"
              class="input"
              placeholder="you@example.com"
              required
            />
          </div>

          <div>
            <label class="input-label" for="password">Password</label>
            <input
              id="password"
              v-model="password"
              type="password"
              autocomplete="current-password"
              class="input"
              placeholder="••••••••"
              required
            />
          </div>

          <p
            v-if="error"
            class="text-sm text-red-700 bg-red-50 border border-red-200 px-3 py-2 rounded"
          >
            {{ error }}
          </p>

          <button
            type="submit"
            class="btn-primary w-full !py-3"
            :disabled="loading"
          >
            <span v-if="loading">Logging in...</span>
            <span v-else>Log in</span>
          </button>
        </form>
      </div>
    </div>
  </div>
</template>