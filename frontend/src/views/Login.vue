<script setup>
import { ref } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import client, { getErrorMessage } from '../api/client'
import { auth } from '../stores/auth'
import { t } from '../stores/i18n'

const router = useRouter()
const route = useRoute()

const username = ref('')
const password = ref('')
const hata = ref('')
const yukleniyor = ref(false)

async function girisYap() {
  hata.value = ''
  yukleniyor.value = true
  try {
    const form = new URLSearchParams()
    form.set('username', username.value)
    form.set('password', password.value)
    const { data } = await client.post('/auth/login', form)

    const me = await client.get('/auth/me', {
      headers: { Authorization: `Bearer ${data.access_token}` },
    })

    auth.setSession(data.access_token, me.data)
    router.push(route.query.redirect || '/')
  } catch (err) {
    hata.value = getErrorMessage(err, 'Giriş başarısız, kullanıcı adı veya şifreyi kontrol edin.')
  } finally {
    yukleniyor.value = false
  }
}
</script>

<template>
  <div class="mx-auto mt-16 max-w-sm">
    <h1 class="mb-6 text-center text-2xl font-semibold text-slate-900 dark:text-white">MaintiFlow</h1>

    <form @submit.prevent="girisYap" class="space-y-4 rounded-xl border border-slate-200 bg-white p-6 shadow-sm dark:border-slate-800 dark:bg-slate-900">
      <div>
        <label class="mb-1 block text-sm text-slate-600 dark:text-slate-300">{{ t('kullaniciAdi') }}</label>
        <input
          v-model="username"
          type="text"
          required
          class="w-full rounded-md border border-slate-300 px-3 py-2 dark:border-slate-700 dark:bg-slate-800 dark:text-white"
        />
      </div>
      <div>
        <label class="mb-1 block text-sm text-slate-600 dark:text-slate-300">{{ t('sifre') }}</label>
        <input
          v-model="password"
          type="password"
          required
          class="w-full rounded-md border border-slate-300 px-3 py-2 dark:border-slate-700 dark:bg-slate-800 dark:text-white"
        />
      </div>

      <p v-if="hata" class="text-sm text-red-600 dark:text-red-400">{{ hata }}</p>

      <button
        type="submit"
        :disabled="yukleniyor"
        class="w-full rounded-md bg-sky-600 py-2 font-medium text-white hover:bg-sky-700 disabled:opacity-60"
      >
        {{ yukleniyor ? t('girisYapiliyor') : t('girisYap') }}
      </button>
    </form>
  </div>
</template>
