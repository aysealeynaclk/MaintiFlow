<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { auth } from '../stores/auth'
import { theme } from '../stores/theme'

const router = useRouter()

const menuAcik = ref(false)
const menuRef = ref(null)

const initialler = computed(() => (auth.user?.username || '?').slice(0, 2).toUpperCase())

function disaTikla(e) {
  if (menuRef.value && !menuRef.value.contains(e.target)) menuAcik.value = false
}
onMounted(() => document.addEventListener('click', disaTikla))
onUnmounted(() => document.removeEventListener('click', disaTikla))

function profileGit() {
  menuAcik.value = false
  router.push('/profil')
}

function cikisYap() {
  menuAcik.value = false
  auth.clearSession()
  router.push('/login')
}
</script>

<template>
  <nav class="border-b border-slate-200 bg-white dark:border-slate-800 dark:bg-slate-900">
    <div class="mx-auto flex max-w-6xl items-center gap-6 px-4 py-3">
      <span class="text-lg font-semibold text-slate-900 dark:text-white">MaintiFlow</span>

      <div class="flex flex-1 gap-4 text-sm">
        <RouterLink to="/" class="text-slate-600 hover:text-slate-900 dark:text-slate-300 dark:hover:text-white"
          active-class="font-semibold text-sky-600 dark:text-sky-400">
          Risk Listesi
        </RouterLink>
        <RouterLink to="/is-emirleri" class="text-slate-600 hover:text-slate-900 dark:text-slate-300 dark:hover:text-white"
          active-class="font-semibold text-sky-600 dark:text-sky-400">
          İş Emirleri
        </RouterLink>
        <template v-if="auth.isAdmin">
          <span class="text-slate-300 dark:text-slate-700">|</span>
          <RouterLink to="/admin/makineler" class="text-slate-600 hover:text-slate-900 dark:text-slate-300 dark:hover:text-white"
            active-class="font-semibold text-sky-600 dark:text-sky-400">
            Makineler
          </RouterLink>
          <RouterLink to="/admin/stok" class="text-slate-600 hover:text-slate-900 dark:text-slate-300 dark:hover:text-white"
            active-class="font-semibold text-sky-600 dark:text-sky-400">
            Stok
          </RouterLink>
          <RouterLink to="/admin/loglar" class="text-slate-600 hover:text-slate-900 dark:text-slate-300 dark:hover:text-white"
            active-class="font-semibold text-sky-600 dark:text-sky-400">
            Loglar
          </RouterLink>
          <RouterLink to="/admin/kullanicilar" class="text-slate-600 hover:text-slate-900 dark:text-slate-300 dark:hover:text-white"
            active-class="font-semibold text-sky-600 dark:text-sky-400">
            Kullanıcılar
          </RouterLink>
        </template>
      </div>

      <button
        @click="theme.toggle()"
        class="rounded-full border border-slate-300 px-3 py-1 text-sm text-slate-600 hover:bg-slate-100 dark:border-slate-700 dark:text-slate-300 dark:hover:bg-slate-800"
      >
        {{ theme.dark ? '☀️ Açık' : '🌙 Koyu' }}
      </button>

      <div ref="menuRef" class="relative">
        <button
          @click="menuAcik = !menuAcik"
          class="flex h-9 w-9 items-center justify-center rounded-full bg-sky-600 text-sm font-semibold text-white hover:bg-sky-700"
        >
          {{ initialler }}
        </button>

        <div
          v-if="menuAcik"
          class="absolute right-0 z-10 mt-2 w-48 rounded-md border border-slate-200 bg-white py-1 shadow-lg dark:border-slate-700 dark:bg-slate-800"
        >
          <div class="border-b border-slate-100 px-4 py-2 text-sm dark:border-slate-700">
            <p class="font-medium text-slate-900 dark:text-white">{{ auth.user?.username }}</p>
            <p class="text-xs text-slate-500 dark:text-slate-400">{{ auth.user?.role }}</p>
          </div>
          <button @click="profileGit" class="block w-full px-4 py-2 text-left text-sm text-slate-700 hover:bg-slate-100 dark:text-slate-200 dark:hover:bg-slate-700">
            Profilim
          </button>
          <button @click="cikisYap" class="block w-full px-4 py-2 text-left text-sm text-slate-700 hover:bg-slate-100 dark:text-slate-200 dark:hover:bg-slate-700">
            Çıkış Yap
          </button>
        </div>
      </div>
    </div>
  </nav>
</template>
