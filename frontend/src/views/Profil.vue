<script setup>
import { ref, computed } from 'vue'
import client, { getErrorMessage } from '../api/client'
import { auth } from '../stores/auth'
import { t } from '../stores/i18n'

const yeniKullaniciAdi = ref(auth.user?.username || '')
const mevcutSifre = ref('')
const yeniSifre = ref('')
const yeniSifreTekrar = ref('')

const mevcutGoster = ref(false)
const yeniGoster = ref(false)

const kaydediliyor = ref(false)
const hata = ref('')
const basari = ref('')

const initialler = computed(() => (auth.user?.username || '?').slice(0, 2).toUpperCase())

const sifreGucu = computed(() => {
  const s = yeniSifre.value
  if (!s) return 0
  let skor = 0
  if (s.length >= 8) skor++
  if (/[a-z]/.test(s) && /[A-Z]/.test(s)) skor++
  if (/[0-9]/.test(s)) skor++
  if (/[^A-Za-z0-9]/.test(s)) skor++
  return skor
})

const gucRenkleri = [
  'bg-slate-200 dark:bg-slate-700',
  'bg-red-500',
  'bg-orange-500',
  'bg-yellow-500',
  'bg-emerald-500',
]
const gucEtiketleri = ['', 'Zayıf', 'Orta', 'İyi', 'Güçlü']

async function kaydet() {
  hata.value = ''
  basari.value = ''

  if (yeniSifre.value && yeniSifre.value !== yeniSifreTekrar.value) {
    hata.value = 'Yeni şifreler birbiriyle uyuşmuyor.'
    return
  }
  if (!mevcutSifre.value) {
    hata.value = 'Değişiklik yapmak için mevcut şifrenizi girmelisiniz.'
    return
  }

  kaydediliyor.value = true
  try {
    const payload = { current_password: mevcutSifre.value }
    if (yeniKullaniciAdi.value && yeniKullaniciAdi.value !== auth.user.username) {
      payload.new_username = yeniKullaniciAdi.value
    }
    if (yeniSifre.value) {
      payload.new_password = yeniSifre.value
    }

    const { data } = await client.patch('/auth/me', payload)
    auth.setSession(auth.token, data)

    basari.value = 'Bilgileriniz güncellendi.'
    mevcutSifre.value = ''
    yeniSifre.value = ''
    yeniSifreTekrar.value = ''
  } catch (err) {
    hata.value = getErrorMessage(err, 'Güncelleme başarısız.')
  } finally {
    kaydediliyor.value = false
  }
}
</script>

<template>
  <div class="mx-auto max-w-lg space-y-6">
    <div class="flex items-center gap-4 rounded-xl border border-slate-200 bg-white p-5 dark:border-slate-800 dark:bg-slate-900">
      <div class="flex h-14 w-14 items-center justify-center rounded-full bg-sky-600 text-lg font-semibold text-white">
        {{ initialler }}
      </div>
      <div>
        <p class="flex items-center gap-2 text-lg font-semibold text-slate-900 dark:text-white">
          {{ auth.user?.username }}
          <span class="h-2 w-2 rounded-full bg-emerald-500" title="Aktif"></span>
        </p>
        <p class="text-sm text-slate-500 dark:text-slate-400">{{ t('rol') }}: {{ auth.user?.role }}</p>
      </div>
    </div>

    <form @submit.prevent="kaydet" class="space-y-4 rounded-xl border border-slate-200 bg-white p-5 dark:border-slate-800 dark:bg-slate-900">
      <h2 class="font-medium text-slate-900 dark:text-white">{{ t('profilBilgileri') }}</h2>

      <div>
        <label class="mb-1 block text-sm text-slate-600 dark:text-slate-300">{{ t('kullaniciAdi') }}</label>
        <input
          v-model="yeniKullaniciAdi"
          type="text"
          class="w-full rounded-md border border-slate-300 px-3 py-2 dark:border-slate-700 dark:bg-slate-800 dark:text-white"
        />
      </div>

      <div>
        <label class="mb-1 block text-sm text-slate-600 dark:text-slate-300">{{ t('yeniSifreOpsiyonel') }}</label>
        <div class="relative">
          <input
            v-model="yeniSifre"
            :type="yeniGoster ? 'text' : 'password'"
            class="w-full rounded-md border border-slate-300 px-3 py-2 pr-16 dark:border-slate-700 dark:bg-slate-800 dark:text-white"
          />
          <button type="button" @click="yeniGoster = !yeniGoster" class="absolute right-2 top-1/2 -translate-y-1/2 text-xs text-slate-500 hover:text-slate-800 dark:text-slate-400">
            {{ yeniGoster ? t('gizle') : t('goster') }}
          </button>
        </div>

        <div v-if="yeniSifre" class="mt-2 flex items-center gap-2">
          <div class="flex flex-1 gap-1">
            <span v-for="i in 4" :key="i" class="h-1.5 flex-1 rounded-full" :class="i <= sifreGucu ? gucRenkleri[sifreGucu] : 'bg-slate-200 dark:bg-slate-700'"></span>
          </div>
          <span class="text-xs text-slate-500 dark:text-slate-400">{{ gucEtiketleri[sifreGucu] }}</span>
        </div>
      </div>

      <div v-if="yeniSifre">
        <label class="mb-1 block text-sm text-slate-600 dark:text-slate-300">{{ t('yeniSifreTekrar') }}</label>
        <input
          v-model="yeniSifreTekrar"
          :type="yeniGoster ? 'text' : 'password'"
          class="w-full rounded-md border border-slate-300 px-3 py-2 dark:border-slate-700 dark:bg-slate-800 dark:text-white"
        />
      </div>

      <div class="border-t border-slate-100 pt-4 dark:border-slate-800">
        <label class="mb-1 block text-sm text-slate-600 dark:text-slate-300">{{ t('mevcutSifreOnay') }}</label>
        <div class="relative">
          <input
            v-model="mevcutSifre"
            :type="mevcutGoster ? 'text' : 'password'"
            required
            class="w-full rounded-md border border-slate-300 px-3 py-2 pr-16 dark:border-slate-700 dark:bg-slate-800 dark:text-white"
          />
          <button type="button" @click="mevcutGoster = !mevcutGoster" class="absolute right-2 top-1/2 -translate-y-1/2 text-xs text-slate-500 hover:text-slate-800 dark:text-slate-400">
            {{ mevcutGoster ? t('gizle') : t('goster') }}
          </button>
        </div>
      </div>

      <p v-if="hata" class="text-sm text-red-600 dark:text-red-400">{{ hata }}</p>
      <p v-if="basari" class="text-sm text-emerald-600 dark:text-emerald-400">{{ basari }}</p>

      <button
        type="submit"
        :disabled="kaydediliyor"
        class="w-full rounded-md bg-sky-600 py-2 font-medium text-white hover:bg-sky-700 disabled:opacity-60"
      >
        {{ kaydediliyor ? t('kaydediliyor') : t('kaydet') }}
      </button>
    </form>
  </div>
</template>
