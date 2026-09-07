import { reactive, watchEffect } from 'vue'

const stored = localStorage.getItem('maintiflow_theme')
const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches

export const theme = reactive({
  dark: stored ? stored === 'dark' : prefersDark,
  toggle() {
    this.dark = !this.dark
  },
})

watchEffect(() => {
  document.documentElement.classList.toggle('dark', theme.dark)
  localStorage.setItem('maintiflow_theme', theme.dark ? 'dark' : 'light')
})
