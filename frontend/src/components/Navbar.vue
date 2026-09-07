<script setup>
import { useRouter } from 'vue-router'
import { auth } from '../stores/auth'
import { theme } from '../stores/theme'

const router = useRouter()

function cikisYap() {
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

      <div class="flex items-center gap-3 text-sm">
        <span class="text-slate-500 dark:text-slate-400">{{ auth.user?.username }}</span>
        <button @click="cikisYap" class="rounded-md bg-slate-100 px-3 py-1 text-slate-700 hover:bg-slate-200 dark:bg-slate-800 dark:text-slate-200 dark:hover:bg-slate-700">
          Çıkış
        </button>
      </div>
    </div>
  </nav>
</template>
