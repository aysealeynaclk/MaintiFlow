import { reactive } from 'vue'

function loadUser() {
  const raw = localStorage.getItem('maintiflow_user')
  return raw ? JSON.parse(raw) : null
}

export const auth = reactive({
  token: localStorage.getItem('maintiflow_token') || null,
  user: loadUser(),

  setSession(token, user) {
    this.token = token
    this.user = user
    localStorage.setItem('maintiflow_token', token)
    localStorage.setItem('maintiflow_user', JSON.stringify(user))
  },

  clearSession() {
    this.token = null
    this.user = null
    localStorage.removeItem('maintiflow_token')
    localStorage.removeItem('maintiflow_user')
  },

  get isLoggedIn() {
    return !!this.token
  },

  get isAdmin() {
    return this.user?.role === 'admin'
  },
})
