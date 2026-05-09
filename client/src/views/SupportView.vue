<script setup>
import { ref } from "vue";

const openFaq = ref(null);

const faqs = [
  {
    q: "How do I place an order?",
    a: "Browse the shop or use the Builder to find your perfect bike or components. Add items to your cart, then proceed to checkout. We accept Cash on Delivery, GCash, and Maya.",
  },
  {
    q: "What payment methods do you accept?",
    a: "We currently accept Cash on Delivery (COD), GCash, and Maya. More payment options are coming soon.",
  },
  {
    q: "How long does delivery take?",
    a: "Orders within Cebu typically arrive in 2–3 business days. Provincial orders take 5–7 business days. You can also choose store pickup for same-day availability.",
  },
  {
    q: "What is your return policy?",
    a: "We offer a 30-day warranty on all products. If your item arrives damaged or defective, contact us within 7 days of delivery and we'll arrange a replacement or refund.",
  },
  {
    q: "How does the Builder work?",
    a: "The Builder takes your budget, height, and riding style and scores our entire catalog to find the best match. Complete Bike mode finds ready-to-ride bikes. Custom Build mode picks the best individual components.",
  },
  {
    q: "Are the components compatible with each other?",
    a: "Our scoring system checks compatibility between components. The Builder will only recommend parts that work together. If you're unsure, contact our support team.",
  },
  {
    q: "Can I pick up my order in store?",
    a: "Yes! Select 'Pickup' during checkout and your order will be ready at our Cebu workshop within 1 business day.",
  },
  {
    q: "How do I track my order?",
    a: "After placing an order, you'll receive a confirmation. You can view your order history and status by logging into your account.",
  },
];

const contactForm = ref({ name: "", email: "", subject: "", message: "" });
const submitted = ref(false);

function submitForm() {
  // In a real app this would call an API
  submitted.value = true;
}

function toggleFaq(index) {
  openFaq.value = openFaq.value === index ? null : index;
}
</script>

<template>
  <div
    class="min-h-screen bg-neutral-950 text-neutral-100 font-body antialiased"
  >
    <!-- NAV -->
    <nav
      class="sticky top-0 z-50 backdrop-blur-md bg-neutral-950/80 border-b border-neutral-800"
    >
      <div
        class="max-w-7xl mx-auto px-6 py-4 flex items-center justify-between"
      >
        <div class="flex items-center gap-12">
          <router-link to="/" class="font-display text-2xl tracking-tight">
            BIKE<span class="text-lime-400">HUB</span>
          </router-link>
          <div
            class="hidden md:flex items-center gap-8 font-mono text-xs uppercase tracking-widest text-neutral-400"
          >
            <router-link
              to="/shop"
              class="hover:text-lime-400 transition-colors"
              >Shop</router-link
            >
            <router-link
              to="/builder"
              class="hover:text-lime-400 transition-colors"
              >Builder</router-link
            >
            <router-link
              to="/about"
              class="hover:text-lime-400 transition-colors"
              >About</router-link
            >
            <router-link to="/support" class="text-lime-400"
              >Support</router-link
            >
          </div>
        </div>
        <div class="flex items-center gap-6">
          <router-link
            to="/login"
            class="hidden md:inline font-mono text-xs uppercase tracking-widest text-neutral-400 hover:text-lime-400 transition-colors"
            >Login</router-link
          >
          <router-link
            to="/cart"
            class="text-neutral-400 hover:text-lime-400 transition-colors"
          >
            <svg
              class="w-5 h-5"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              stroke-width="2"
            >
              <circle cx="9" cy="21" r="1" />
              <circle cx="20" cy="21" r="1" />
              <path
                d="M1 1h4l2.7 13.4a2 2 0 0 0 2 1.6h9.7a2 2 0 0 0 2-1.6L23 6H6"
              />
            </svg>
          </router-link>
        </div>
      </div>
    </nav>

    <!-- HEADER -->
    <div class="border-b border-neutral-800">
      <div class="max-w-7xl mx-auto px-6 py-12">
        <div
          class="font-mono text-xs uppercase tracking-widest text-neutral-500 mb-3"
        >
          // SUPPORT
        </div>
        <h1 class="font-display text-5xl md:text-7xl">
          How can we<br /><span class="text-lime-400">help?</span>
        </h1>
      </div>
    </div>

    <!-- QUICK LINKS -->
    <div class="border-b border-neutral-800">
      <div
        class="max-w-7xl mx-auto px-6 py-12 grid grid-cols-2 md:grid-cols-4 gap-4"
      >
        <div
          class="bg-neutral-900 border border-neutral-800 hover:border-lime-400 transition-colors p-6 text-center"
        >
          <div class="text-2xl mb-3">📦</div>
          <div class="font-display text-lg mb-1">Orders</div>
          <div class="font-mono text-xs text-neutral-500">Track & manage</div>
        </div>
        <div
          class="bg-neutral-900 border border-neutral-800 hover:border-lime-400 transition-colors p-6 text-center"
        >
          <div class="text-2xl mb-3">🔄</div>
          <div class="font-display text-lg mb-1">Returns</div>
          <div class="font-mono text-xs text-neutral-500">30-day warranty</div>
        </div>
        <div
          class="bg-neutral-900 border border-neutral-800 hover:border-lime-400 transition-colors p-6 text-center"
        >
          <div class="text-2xl mb-3">🚚</div>
          <div class="font-display text-lg mb-1">Shipping</div>
          <div class="font-mono text-xs text-neutral-500">
            Cebu & nationwide
          </div>
        </div>
        <div
          class="bg-neutral-900 border border-neutral-800 hover:border-lime-400 transition-colors p-6 text-center"
        >
          <div class="text-2xl mb-3">🔧</div>
          <div class="font-display text-lg mb-1">Builder Help</div>
          <div class="font-mono text-xs text-neutral-500">Component guide</div>
        </div>
      </div>
    </div>

    <div class="max-w-7xl mx-auto px-6 py-16 grid md:grid-cols-2 gap-16">
      <!-- FAQ -->
      <div>
        <div
          class="font-mono text-xs uppercase tracking-widest text-neutral-500 mb-3"
        >
          // FAQ
        </div>
        <h2 class="font-display text-4xl mb-8">Frequently Asked</h2>
        <div class="space-y-2">
          <div
            v-for="(faq, index) in faqs"
            :key="index"
            class="border border-neutral-800 hover:border-neutral-700 transition-colors"
          >
            <button
              @click="toggleFaq(index)"
              class="w-full text-left px-5 py-4 flex items-center justify-between gap-4"
            >
              <span class="font-mono text-sm">{{ faq.q }}</span>
              <span
                class="font-mono text-neutral-500 shrink-0 transition-transform"
                :class="openFaq === index ? 'rotate-45' : ''"
                >+</span
              >
            </button>
            <div v-if="openFaq === index" class="px-5 pb-4">
              <p class="text-sm text-neutral-400 leading-relaxed">
                {{ faq.a }}
              </p>
            </div>
          </div>
        </div>
      </div>

      <!-- CONTACT FORM -->
      <div>
        <div
          class="font-mono text-xs uppercase tracking-widest text-neutral-500 mb-3"
        >
          // CONTACT
        </div>
        <h2 class="font-display text-4xl mb-8">Send a Message</h2>

        <div
          v-if="submitted"
          class="bg-neutral-900 border border-lime-400 p-8 text-center"
        >
          <div class="font-display text-3xl text-lime-400 mb-3">
            Message Sent!
          </div>
          <p class="text-neutral-400 text-sm">
            We'll get back to you within 24 hours.
          </p>
          <button
            @click="submitted = false"
            class="mt-4 font-mono text-xs uppercase tracking-widest text-neutral-500 hover:text-lime-400 transition-colors"
          >
            Send Another →
          </button>
        </div>

        <div v-else class="space-y-4">
          <div>
            <label
              class="font-mono text-xs uppercase tracking-widest text-neutral-500 mb-2 block"
              >Name</label
            >
            <input
              v-model="contactForm.name"
              type="text"
              placeholder="Your name"
              class="w-full bg-neutral-900 border border-neutral-800 text-neutral-100 font-mono text-sm px-4 py-3 focus:outline-none focus:border-lime-400 transition-colors placeholder:text-neutral-600"
            />
          </div>
          <div>
            <label
              class="font-mono text-xs uppercase tracking-widest text-neutral-500 mb-2 block"
              >Email</label
            >
            <input
              v-model="contactForm.email"
              type="email"
              placeholder="your@email.com"
              class="w-full bg-neutral-900 border border-neutral-800 text-neutral-100 font-mono text-sm px-4 py-3 focus:outline-none focus:border-lime-400 transition-colors placeholder:text-neutral-600"
            />
          </div>
          <div>
            <label
              class="font-mono text-xs uppercase tracking-widest text-neutral-500 mb-2 block"
              >Subject</label
            >
            <select
              v-model="contactForm.subject"
              class="w-full bg-neutral-900 border border-neutral-800 text-neutral-100 font-mono text-sm px-4 py-3 focus:outline-none focus:border-lime-400 transition-colors"
            >
              <option value="">Select a topic…</option>
              <option>Order Issue</option>
              <option>Return / Warranty</option>
              <option>Product Question</option>
              <option>Builder Help</option>
              <option>Other</option>
            </select>
          </div>
          <div>
            <label
              class="font-mono text-xs uppercase tracking-widest text-neutral-500 mb-2 block"
              >Message</label
            >
            <textarea
              v-model="contactForm.message"
              rows="5"
              placeholder="How can we help?"
              class="w-full bg-neutral-900 border border-neutral-800 text-neutral-100 font-mono text-sm px-4 py-3 focus:outline-none focus:border-lime-400 transition-colors placeholder:text-neutral-600 resize-none"
            ></textarea>
          </div>
          <button
            @click="submitForm"
            class="w-full bg-lime-400 hover:bg-lime-300 text-neutral-950 font-mono text-sm uppercase tracking-widest py-4 transition-colors"
          >
            Send Message →
          </button>
        </div>

        <!-- Contact info -->
        <div class="mt-10 pt-8 border-t border-neutral-800 space-y-3">
          <div
            class="flex items-center gap-3 font-mono text-xs text-neutral-500"
          >
            <span class="text-lime-400">📍</span>
            <span>Cebu City, Philippines</span>
          </div>
          <div
            class="flex items-center gap-3 font-mono text-xs text-neutral-500"
          >
            <span class="text-lime-400">✉️</span>
            <span>support@bikehub.ph</span>
          </div>
          <div
            class="flex items-center gap-3 font-mono text-xs text-neutral-500"
          >
            <span class="text-lime-400">⏰</span>
            <span>Mon–Sat, 9am–6pm</span>
          </div>
        </div>
      </div>
    </div>

    <!-- FOOTER -->
    <footer class="border-t border-neutral-800">
      <div
        class="max-w-7xl mx-auto px-6 py-8 flex flex-col md:flex-row justify-between gap-4 font-mono text-xs text-neutral-500 uppercase tracking-widest"
      >
        <div>© 2026 BIKEHUB · EDGETECH · CEBU, PH</div>
        <router-link to="/" class="hover:text-lime-400 transition-colors"
          >← Back to Home</router-link
        >
      </div>
    </footer>
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
.rotate-45 {
  transform: rotate(45deg);
}
</style>
