<script setup>
import { ref, onMounted } from 'vue'
import client, { getErrorMessage } from '../api/client'
import { t } from '../stores/i18n'

const props = defineProps({
  id: { type: [String, Number], required: true },
  username: { type: String, required: true },
})
const emit = defineEmits(['kapat'])

const istatistik = ref(null)
const yukleniyor = ref(true)
const hata = ref('')

onMounted(async () => {
  try {
    const { data } = await client.get(`/admin/kullanicilar/${props.id}/istatistik`)
    istatistik.value = data
  } catch (err) {
    hata.value = getErrorMessage(err, 'İstatistik yüklenemedi.')
  } finally {
    yukleniyor.value = false
  }
})
</script>

<template>
  <div class="fixed inset-0 z-50 flex items-center justify-center bg-black/50 p-4" @click.self="$emit('kapat')">
    <div class="w-full max-w-md rounded-xl bg-white p-6 shadow-2xl dark:bg-slate-900">
      <div class="mb-4 flex items-center justify-between">
        <h2 class="text-lg font-semibold text-slate-900 dark:text-white">{{ t('kullaniciIstatistigi') }} — {{ username }}</h2>
        <button @click="$emit('kapat')" class="text-xl leading-none text-slate-400 hover:text-slate-700 dark:hover:text-white">✕</button>
      </div>

      <p v-if="hata" class="text-sm text-red-600 dark:text-red-400">{{ hata }}</p>
      <p v-else-if="yukleniyor" class="text-sm text-slate-500 dark:text-slate-400">{{ t('yukleniyor') }}</p>

      <div v-else-if="istatistik" class="grid grid-cols-2 gap-3">
        <div class="rounded-lg border border-slate-200 p-4 dark:border-slate-800">
          <div class="text-2xl font-bold text-emerald-600 dark:text-emerald-400">{{ istatistik.onaylanan_tahmin }}</div>
          <div class="mt-1 text-xs text-slate-500 dark:text-slate-400">{{ t('onaylananTahmin') }}</div>
        </div>
        <div class="rounded-lg border border-slate-200 p-4 dark:border-slate-800">
          <div class="text-2xl font-bold text-slate-600 dark:text-slate-400">{{ istatistik.reddedilen_tahmin }}</div>
          <div class="mt-1 text-xs text-slate-500 dark:text-slate-400">{{ t('reddedilenTahmin') }}</div>
        </div>
        <div class="rounded-lg border border-slate-200 p-4 dark:border-slate-800">
          <div class="text-2xl font-bold text-sky-600 dark:text-sky-400">{{ istatistik.toplam_is_emri }}</div>
          <div class="mt-1 text-xs text-slate-500 dark:text-slate-400">{{ t('toplamIsEmri') }}</div>
        </div>
        <div class="rounded-lg border border-slate-200 p-4 dark:border-slate-800">
          <div class="text-2xl font-bold text-emerald-600 dark:text-emerald-400">{{ istatistik.tamamlanan_is_emri }}</div>
          <div class="mt-1 text-xs text-slate-500 dark:text-slate-400">{{ t('tamamlananIsEmri') }}</div>
        </div>
        <div class="rounded-lg border border-slate-200 p-4 dark:border-slate-800">
          <div class="text-2xl font-bold text-slate-600 dark:text-slate-400">{{ istatistik.iptal_edilen_is_emri }}</div>
          <div class="mt-1 text-xs text-slate-500 dark:text-slate-400">{{ t('iptalEdilenIsEmri') }}</div>
        </div>
        <div class="rounded-lg border border-slate-200 p-4 dark:border-slate-800">
          <div class="text-2xl font-bold text-amber-600 dark:text-amber-400">{{ istatistik.bekleyen_is_emri }}</div>
          <div class="mt-1 text-xs text-slate-500 dark:text-slate-400">{{ t('bekleyenIsEmri') }}</div>
        </div>
      </div>
    </div>
  </div>
</template>
