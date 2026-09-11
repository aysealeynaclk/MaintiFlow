<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { auth } from '../stores/auth'
import { theme } from '../stores/theme'
import { i18n, t } from '../stores/i18n'

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
      <RouterLink to="/" class="text-lg font-semibold text-slate-900 dark:text-white">MaintiFlow</RouterLink>

      <div class="flex flex-1 gap-4 text-sm">
        <RouterLink to="/" class="text-slate-600 hover:text-slate-900 dark:text-slate-300 dark:hover:text-white"
          active-class="font-semibold text-sky-600 dark:text-sky-400">
          {{ t('riskListesi') }}
        </RouterLink>
        <RouterLink to="/is-emirleri" class="text-slate-600 hover:text-slate-900 dark:text-slate-300 dark:hover:text-white"
          active-class="font-semibold text-sky-600 dark:text-sky-400">
          {{ t('isEmirleri') }}
        </RouterLink>
        <template v-if="auth.isAdmin">
          <span class="text-slate-300 dark:text-slate-700">|</span>
          <RouterLink to="/admin/makineler" class="text-slate-600 hover:text-slate-900 dark:text-slate-300 dark:hover:text-white"
            active-class="font-semibold text-sky-600 dark:text-sky-400">
            {{ t('makineler') }}
          </RouterLink>
          <RouterLink to="/admin/stok" class="text-slate-600 hover:text-slate-900 dark:text-slate-300 dark:hover:text-white"
            active-class="font-semibold text-sky-600 dark:text-sky-400">
            {{ t('stok') }}
          </RouterLink>
          <RouterLink to="/admin/loglar" class="text-slate-600 hover:text-slate-900 dark:text-slate-300 dark:hover:text-white"
            active-class="font-semibold text-sky-600 dark:text-sky-400">
            {{ t('loglar') }}
          </RouterLink>
          <RouterLink to="/admin/kullanicilar" class="text-slate-600 hover:text-slate-900 dark:text-slate-300 dark:hover:text-white"
            active-class="font-semibold text-sky-600 dark:text-sky-400">
            {{ t('kullanicilar') }}
          </RouterLink>
        </template>
      </div>

      <div ref="menuRef" class="relative">
        <button
          @click="menuAcik = !menuAcik"
          class="flex h-9 w-9 items-center justify-center rounded-full bg-sky-600 text-sm font-semibold text-white hover:bg-sky-700"
        >
          {{ initialler }}
        </button>

        <div
          v-if="menuAcik"
          class="absolute right-0 z-10 mt-2 w-64 rounded-lg border border-slate-200 bg-white py-2 shadow-lg dark:border-slate-700 dark:bg-slate-800"
        >
          <div class="flex items-center gap-3 px-4 py-2">
            <div class="flex h-10 w-10 items-center justify-center rounded-lg bg-sky-600 text-sm font-semibold text-white">
              {{ initialler }}
            </div>
            <div>
              <p class="font-medium text-slate-900 dark:text-white">{{ auth.user?.username }}</p>
              <p class="text-xs text-slate-500 dark:text-slate-400">{{ auth.user?.role }}</p>
            </div>
          </div>

          <div class="border-t border-slate-100 px-4 py-2.5 dark:border-slate-700">
            <div class="flex items-center justify-between">
              <span class="text-sm text-slate-700 dark:text-slate-200">{{ t('gorunum') }}</span>
              <div class="flex rounded-full border border-slate-300 p-0.5 text-xs dark:border-slate-600">
                <button
                  @click="theme.dark = false"
                  class="rounded-full px-3 py-1"
                  :class="!theme.dark ? 'bg-sky-600 text-white' : 'text-slate-500 dark:text-slate-400'"
                >
                  {{ t('acik') }}
                </button>
                <button
                  @click="theme.dark = true"
                  class="rounded-full px-3 py-1"
                  :class="theme.dark ? 'bg-sky-600 text-white' : 'text-slate-500 dark:text-slate-400'"
                >
                  {{ t('koyu') }}
                </button>
              </div>
            </div>
          </div>

          <div class="px-4 py-2.5">
            <div class="flex items-center justify-between">
              <span class="text-sm text-slate-700 dark:text-slate-200">{{ t('dil') }}</span>
              <div class="flex rounded-full border border-slate-300 p-0.5 text-xs dark:border-slate-600">
                <button
                  @click="i18n.setLocale('tr')"
                  class="rounded-full px-3 py-1"
                  :class="i18n.locale === 'tr' ? 'bg-sky-600 text-white' : 'text-slate-500 dark:text-slate-400'"
                >
                  TR
                </button>
                <button
                  @click="i18n.setLocale('en')"
                  class="rounded-full px-3 py-1"
                  :class="i18n.locale === 'en' ? 'bg-sky-600 text-white' : 'text-slate-500 dark:text-slate-400'"
                >
                  EN
                </button>
              </div>
            </div>
          </div>

          <div class="border-t border-slate-100 dark:border-slate-700">
            <button @click="profileGit" class="block w-full px-4 py-2.5 text-left text-sm text-slate-700 hover:bg-slate-100 dark:text-slate-200 dark:hover:bg-slate-700">
              {{ t('profilim') }}
            </button>
            <button @click="cikisYap" class="block w-full px-4 py-2.5 text-left text-sm text-red-600 hover:bg-red-50 dark:text-red-400 dark:hover:bg-red-900/20">
              {{ t('cikisYap') }}
            </button>
          </div>
        </div>
      </div>
    </div>
  </nav>
</template>
