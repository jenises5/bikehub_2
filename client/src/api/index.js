import axios from 'axios'

// ── Base URL from environment variable ────────────────
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

// ── Create the configured Axios instance ──────────────
const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

// ── Request interceptor ───────────────────────────────
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

// ── Response interceptor ──────────────────────────────
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      const path = window.location.pathname
      if (path !== '/login' && path !== '/register') {
        localStorage.removeItem('token')
        localStorage.removeItem('user')
        window.location.href = '/login'
      }
    }
    return Promise.reject(error)
  }
)

// ── fileUrl helper ────────────────────────────────────
export const fileUrl = (relativePath) => {
  if (!relativePath) return ''
  if (relativePath.startsWith('http')) return relativePath
  const base = API_BASE_URL.replace(/\/$/, '')
  const path = relativePath.startsWith('/') ? relativePath : `/${relativePath}`
  return `${base}${path}`
}

export const API_BASE = API_BASE_URL
export default api