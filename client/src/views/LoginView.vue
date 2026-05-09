<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";
import api from "../services/api";
import { useUserStore } from "../stores/user";

const router = useRouter();
const userStore = useUserStore();
const mode = ref("login");

const email = ref("");
const password = ref("");
const name = ref("");
const error = ref("");
const loading = ref(false);

async function handleSubmit() {
  error.value = "";
  loading.value = true;
  try {
    if (mode.value === "login") {
      const res = await api.post("/auth/login", {
        email: email.value,
        password: password.value,
      });
      userStore.login(res.data.user, res.data.access_token);
      router.push("/");
    } else {
      await api.post("/auth/register", {
        name: name.value,
        email: email.value,
        password: password.value,
      });
      const res = await api.post("/auth/login", {
        email: email.value,
        password: password.value,
      });
      userStore.login(res.data.user, res.data.access_token);
      router.push("/");
    }
  } catch (err) {
    error.value =
      err.response?.data?.detail || "Something went wrong. Please try again.";
  } finally {
    loading.value = false;
  }
}

function switchMode(m) {
  mode.value = m;
  error.value = "";
  email.value = "";
  password.value = "";
  name.value = "";
}
</script>

<template>
  <div
    class="min-h-screen bg-neutral-950 text-neutral-100 font-body antialiased flex flex-col"
  >
    <!-- NAV -->
    <nav
      class="border-b border-neutral-800 px-6 py-4 flex items-center justify-between"
    >
      <router-link to="/" class="font-display text-2xl tracking-tight">
        BIKE<span class="text-lime-400">HUB</span>
      </router-link>
      <router-link
        to="/shop"
        class="font-mono text-xs uppercase tracking-widest text-neutral-400 hover:text-lime-400 transition-colors"
      >
        ← Back to Shop
      </router-link>
    </nav>

    <!-- MAIN -->
    <div class="flex-1 flex items-center justify-center px-6 py-16">
      <div class="w-full max-w-md">
        <div class="mb-10">
          <div
            class="font-mono text-xs uppercase tracking-widest text-neutral-500 mb-3"
          >
            // {{ mode === "login" ? "SIGN IN" : "CREATE ACCOUNT" }}
          </div>
          <h1 class="font-display text-5xl">
            {{ mode === "login" ? "Welcome back." : "Join BikeHub." }}
          </h1>
        </div>

        <div class="flex border border-neutral-800 mb-8">
          <button
            @click="switchMode('login')"
            class="flex-1 font-mono text-xs uppercase tracking-widest py-3 transition-colors"
            :class="
              mode === 'login'
                ? 'bg-lime-400 text-neutral-950'
                : 'text-neutral-400 hover:text-neutral-100'
            "
          >
            Sign In
          </button>
          <button
            @click="switchMode('register')"
            class="flex-1 font-mono text-xs uppercase tracking-widest py-3 transition-colors"
            :class="
              mode === 'register'
                ? 'bg-lime-400 text-neutral-950'
                : 'text-neutral-400 hover:text-neutral-100'
            "
          >
            Register
          </button>
        </div>

        <div class="space-y-4">
          <div v-if="mode === 'register'">
            <label
              class="font-mono text-xs uppercase tracking-widest text-neutral-500 mb-2 block"
              >Full Name</label
            >
            <input
              v-model="name"
              type="text"
              placeholder="Juan dela Cruz"
              class="w-full bg-neutral-900 border border-neutral-800 text-neutral-100 font-mono text-sm px-4 py-3 focus:outline-none focus:border-lime-400 transition-colors placeholder:text-neutral-600"
              @keyup.enter="handleSubmit"
            />
          </div>

          <div>
            <label
              class="font-mono text-xs uppercase tracking-widest text-neutral-500 mb-2 block"
              >Email</label
            >
            <input
              v-model="email"
              type="email"
              placeholder="juan@example.com"
              class="w-full bg-neutral-900 border border-neutral-800 text-neutral-100 font-mono text-sm px-4 py-3 focus:outline-none focus:border-lime-400 transition-colors placeholder:text-neutral-600"
              @keyup.enter="handleSubmit"
            />
          </div>

          <div>
            <label
              class="font-mono text-xs uppercase tracking-widest text-neutral-500 mb-2 block"
              >Password</label
            >
            <input
              v-model="password"
              type="password"
              placeholder="••••••••"
              class="w-full bg-neutral-900 border border-neutral-800 text-neutral-100 font-mono text-sm px-4 py-3 focus:outline-none focus:border-lime-400 transition-colors placeholder:text-neutral-600"
              @keyup.enter="handleSubmit"
            />
          </div>

          <div
            v-if="error"
            class="font-mono text-xs text-red-400 border border-red-900 bg-red-950/50 px-4 py-3"
          >
            {{ error }}
          </div>

          <button
            @click="handleSubmit"
            :disabled="loading"
            class="w-full font-mono text-sm uppercase tracking-widest py-4 transition-colors mt-2"
            :class="
              loading
                ? 'bg-neutral-700 text-neutral-500'
                : 'bg-lime-400 hover:bg-lime-300 text-neutral-950'
            "
          >
            <span v-if="loading">{{
              mode === "login" ? "Signing in…" : "Creating account…"
            }}</span>
            <span v-else>{{
              mode === "login" ? "Sign In →" : "Create Account →"
            }}</span>
          </button>
        </div>

        <p class="mt-8 font-mono text-xs text-neutral-600 text-center">
          {{
            mode === "login"
              ? "Don't have an account?"
              : "Already have an account?"
          }}
          <button
            @click="switchMode(mode === 'login' ? 'register' : 'login')"
            class="text-lime-400 hover:text-lime-300 transition-colors ml-1"
          >
            {{ mode === "login" ? "Register" : "Sign in" }}
          </button>
        </p>
      </div>
    </div>
  </div>
</template>

<style scoped>
.font-display {
  font-family: "Bebas Neue", "Arial Narrow", sans-serif;
  letter-spacing: 0.01em;
}
.font-mono {
  font-family: "JetBrains Mono", "Courier New", monospace;
}
.font-body {
  font-family:
    "Manrope",
    system-ui,
    -apple-system,
    sans-serif;
}
</style>
