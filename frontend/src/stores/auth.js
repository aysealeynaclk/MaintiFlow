import { reactive } from 'vue'

function loadFrom(storage) {
  const token = storage.getItem('maintiflow_token')
  const rawUser = storage.getItem('maintiflow_user')
  return token && rawUser ? { token, user: JSON.parse(rawUser) } : null
}

const mevcutOturum = loadFrom(localStorage) || loadFrom(sessionStorage)

export const auth = reactive({
  token: mevcutOturum?.token || null,
  user: mevcutOturum?.user || null,

  /**
   * beniHatirla=true ise oturum localStorage'da tarayici kapansa bile kalir,
   * false ise sessionStorage'da tutulur ve sekme/tarayici kapaninca silinir.
   */
  setSession(token, user, beniHatirla = true) {
    this.token = token
    this.user = user

    const hedef = beniHatirla ? localStorage : sessionStorage
    const diger = beniHatirla ? sessionStorage : localStorage
    hedef.setItem('maintiflow_token', token)
    hedef.setItem('maintiflow_user', JSON.stringify(user))
    diger.removeItem('maintiflow_token')
    diger.removeItem('maintiflow_user')
  },

  clearSession() {
    this.token = null
    this.user = null
    localStorage.removeItem('maintiflow_token')
    localStorage.removeItem('maintiflow_user')
    sessionStorage.removeItem('maintiflow_token')
    sessionStorage.removeItem('maintiflow_user')
  },

  get isLoggedIn() {
    return !!this.token
  },

  get isAdmin() {
    return this.user?.role === 'admin'
  },
})
