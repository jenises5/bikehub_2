<script setup>
import { ref, computed } from 'vue'
import { useRouter, RouterLink } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const auth = useAuthStore()

const name = ref('')
const email = ref('')
const password = ref('')
const confirm = ref('')
const loading = ref(false)
const error = ref('')
const success = ref('')

const passwordTooShort = computed(() => password.value.length > 0 && password.value.length < 8)
const passwordMismatch = computed(() => confirm.value.length > 0 && confirm.value !== password.value)

async function handleSubmit() {
  error.value = ''
  success.value = ''
  if (!name.value || !email.value || !password.value) {
    error.value = 'All fields are required.'
    return
  }
  if (password.value.length < 8) {
    error.value = 'Password must be at least 8 characters.'
    return
  }
  if (password.value !== confirm.value) {
    error.value = 'Passwords do not match.'
    return
  }

  loading.value = true
  try {
    await auth.register(name.value.trim(), email.value.trim(), password.value)
    success.value = 'Account created. Redirecting to login...'
    setTimeout(() => router.push('/login'), 1100)
  } catch (err) {
    error.value = err.response?.data?.detail || 'Registration failed. Please try again.'
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="fade-in min-h-[calc(100vh-4rem)] grid md:grid-cols-2">
    <div class="hidden md:flex bg-cream-deep border-r border-stone-200 p-12 flex-col justify-between">
      <RouterLink to="/" class="flex items-center gap-2 w-fit">
        <span class="w-8 h-8 rounded-md bg-clay-700 text-cream flex items-center justify-center font-display text-lg leading-none">B</span>
        <span class="font-display text-xl text-stone-900">BikeHub</span>
      </RouterLink>

      <div class="max-w-md">
        <p class="eyebrow mb-4">Join BikeHub</p>
        <h1 class="font-display text-5xl leading-[1.05] tracking-tight text-stone-900">
          Build smarter,<br/>
          <span class="italic">ride sooner.</span>
        </h1>
        <p class="text-stone-600 mt-6 leading-relaxed">
          Save builds, get restock alerts, and track your orders in one place.
        </p>
      </div>

      <p class="text-xs text-stone-500">© 2026 BikeHub · CTU-Main</p>
    </div>

    <div class="flex items-center justify-center p-6 md:p-12">
      <div class="w-full max-w-sm">
        <h2 class="font-display text-3xl tracking-tight mb-2">Create your account</h2>
        <p class="text-sm text-stone-600 mb-8">
          Already have one?
          <RouterLink to="/login" class="text-clay-700 font-medium hover:underline">
            Log in
          </RouterLink>
        </p>

        <form @submit.prevent="handleSubmit" class="space-y-5" novalidate>
          <div>
            <label class="input-label" for="name">Full name</label>
            <input id="name" v-model="name" type="text" autocomplete="name" class="input" placeholder="Juan dela Cruz" required />
          </div>

          <div>
            <label class="input-label" for="email">Email</label>
            <input id="email" v-model="email" type="email" autocomplete="email" class="input" placeholder="you@example.com" required />
          </div>

          <div>
            <label class="input-label" for="password">Password</label>
            <input
              id="password" v-model="password" type="password"
              autocomplete="new-password" class="input"
              placeholder="At least 8 characters" required
            />
            <p v-if="passwordTooShort" class="text-2xs text-amber-700 mt-1">
              Password must be at least 8 characters.
            </p>
          </div>

          <div>
            <label class="input-label" for="confirm">Confirm password</label>
            <input
              id="confirm" v-model="confirm" type="password"
              autocomplete="new-password" class="input"
              placeholder="Re-type your password" required
            />
            <p v-if="passwordMismatch" class="text-2xs text-red-700 mt-1">
              Passwords don't match.
            </p>
          </div>

          <p v-if="error" class="text-sm text-red-700 bg-red-50 border border-red-200 px-3 py-2 rounded">
            {{ error }}
          </p>
          <p v-if="success" class="text-sm text-emerald-800 bg-emerald-50 border border-emerald-200 px-3 py-2 rounded">
            {{ success }}
          </p>

          <button type="submit" class="btn-primary w-full !py-3" :disabled="loading">
            <span v-if="loading">Creating account...</span>
            <span v-else>Create account</span>
          </button>
        </form>
      </div>
    </div>
  </div>
</template>