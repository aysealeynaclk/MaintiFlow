<script setup>
import { ref, computed, onMounted } from 'vue'
import client, { getErrorMessage } from '../api/client'
import { t } from '../stores/i18n'

const SAYFA_BOYUTU = 20

const isEmirleri = ref([])
const yukleniyor = ref(true)
const hata = ref('')
const sayfa = ref(1)

const toplamSayfa = computed(() => Math.max(1, Math.ceil(isEmirleri.value.length / SAYFA_BOYUTU)))
const sayfalanmis = computed(() => {
  const baslangic = (sayfa.value - 1) * SAYFA_BOYUTU
  return isEmirleri.value.slice(baslangic, baslangic + SAYFA_BOYUTU)
})

onMounted(async () => {
  try {
    const { data } = await client.get('/is-emirleri')
    isEmirleri.value = data
  } catch (err) {
    hata.value = getErrorMessage(err, 'İş emirleri yüklenemedi.')
  } finally {
    yukleniyor.value = false
  }
})
</script>

<template>
  <div>
    <h1 class="mb-4 text-xl font-semibold text-slate-900 dark:text-white">{{ t('isEmirleri') }}</h1>

    <p v-if="hata" class="text-sm text-red-600 dark:text-red-400">{{ hata }}</p>
    <p v-else-if="yukleniyor" class="text-sm text-slate-500 dark:text-slate-400">{{ t('yukleniyor') }}</p>
    <p v-else-if="isEmirleri.length === 0" class="text-sm text-slate-500 dark:text-slate-400">{{ t('isEmriYok') }}</p>

    <template v-else>
      <div class="overflow-x-auto rounded-lg border border-slate-200 dark:border-slate-800">
        <table class="w-full text-left text-sm">
          <thead class="bg-slate-100 text-slate-600 dark:bg-slate-800 dark:text-slate-300">
            <tr>
              <th class="px-4 py-2">{{ t('colMakine') }}</th>
              <th class="px-4 py-2">{{ t('colAksiyon') }}</th>
              <th class="px-4 py-2">{{ t('colParca') }}</th>
              <th class="px-4 py-2">{{ t('colOncelik') }}</th>
              <th class="px-4 py-2">{{ t('colDurum') }}</th>
              <th class="px-4 py-2">{{ t('colTarih') }}</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="e in sayfalanmis" :key="e.id" class="border-t border-slate-200 dark:border-slate-800">
              <td class="px-4 py-2 font-medium text-slate-900 dark:text-white">{{ e.makine_kodu }}</td>
              <td class="px-4 py-2">{{ e.aksiyon }}</td>
              <td class="px-4 py-2 text-slate-500 dark:text-slate-400">{{ e.parca_kodu }}</td>
              <td class="px-4 py-2">{{ e.oncelik }}</td>
              <td class="px-4 py-2">{{ e.durum }}</td>
              <td class="px-4 py-2 text-slate-500 dark:text-slate-400">{{ new Date(e.created_at).toLocaleString('tr-TR') }}</td>
            </tr>
          </tbody>
        </table>
      </div>

      <div class="mt-3 flex items-center justify-between text-sm text-slate-500 dark:text-slate-400">
        <span>{{ t('toplam') }} {{ isEmirleri.length }} {{ t('kayit') }} — {{ t('sayfa') }} {{ sayfa }} / {{ toplamSayfa }}</span>
        <div class="flex gap-2">
          <button @click="sayfa > 1 && sayfa--" :disabled="sayfa <= 1" class="rounded-md border border-slate-300 px-3 py-1 disabled:opacity-40 dark:border-slate-700">
            {{ t('oncekiSayfa') }}
          </button>
          <button @click="sayfa < toplamSayfa && sayfa++" :disabled="sayfa >= toplamSayfa" class="rounded-md border border-slate-300 px-3 py-1 disabled:opacity-40 dark:border-slate-700">
            {{ t('sonrakiSayfa') }}
          </button>
        </div>
      </div>
    </template>
  </div>
</template>
