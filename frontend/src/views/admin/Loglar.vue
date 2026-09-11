<script setup>
import { ref, computed, onMounted } from 'vue'
import client, { getErrorMessage } from '../../api/client'
import { t } from '../../stores/i18n'
import { useSiralama } from '../../composables/useSiralama'

const SAYFA_BOYUTU = 20

const loglar = ref([])
const yukleniyor = ref(true)
const hata = ref('')
const sayfa = ref(1)

const { siralanmis, sirala } = useSiralama(loglar)

const toplamSayfa = computed(() => Math.max(1, Math.ceil(siralanmis.value.length / SAYFA_BOYUTU)))
const sayfalanmis = computed(() => {
  const baslangic = (sayfa.value - 1) * SAYFA_BOYUTU
  return siralanmis.value.slice(baslangic, baslangic + SAYFA_BOYUTU)
})

function siralaVeBastaBasla(alan) {
  sirala(alan)
  sayfa.value = 1
}

onMounted(async () => {
  try {
    const { data } = await client.get('/admin/loglar')
    loglar.value = data
  } catch (err) {
    hata.value = getErrorMessage(err, 'Loglar yüklenemedi.')
  } finally {
    yukleniyor.value = false
  }
})
</script>

<template>
  <div>
    <h1 class="mb-4 text-xl font-semibold text-slate-900 dark:text-white">{{ t('loglar') }}</h1>
    <p v-if="hata" class="text-sm text-red-600 dark:text-red-400">{{ hata }}</p>
    <p v-else-if="yukleniyor" class="text-sm text-slate-500 dark:text-slate-400">{{ t('yukleniyor') }}</p>

    <template v-else>
      <div class="overflow-x-auto rounded-lg border border-slate-200 dark:border-slate-800">
        <table class="w-full text-left text-sm">
          <thead class="bg-slate-100 text-slate-600 dark:bg-slate-800 dark:text-slate-300">
            <tr>
              <th class="cursor-pointer select-none px-4 py-2" @click="siralaVeBastaBasla('created_at')">{{ t('colTarih') }} ⇅</th>
              <th class="cursor-pointer select-none px-4 py-2" @click="siralaVeBastaBasla('makine_kodu')">{{ t('colMakine') }} ⇅</th>
              <th class="cursor-pointer select-none px-4 py-2" @click="siralaVeBastaBasla('risk_orani')">{{ t('colRisk') }} ⇅</th>
              <th class="cursor-pointer select-none px-4 py-2" @click="siralaVeBastaBasla('ariza_tipi')">{{ t('colArizaTipi') }} ⇅</th>
              <th class="cursor-pointer select-none px-4 py-2" @click="siralaVeBastaBasla('oncelik')">{{ t('colOncelik') }} ⇅</th>
              <th class="cursor-pointer select-none px-4 py-2" @click="siralaVeBastaBasla('durum')">{{ t('colKarar') }} ⇅</th>
              <th class="cursor-pointer select-none px-4 py-2" @click="siralaVeBastaBasla('karar_veren_username')">{{ t('colKararVeren') }} ⇅</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="l in sayfalanmis" :key="l.id" class="border-t border-slate-200 dark:border-slate-800">
              <td class="px-4 py-2 text-slate-500 dark:text-slate-400">{{ new Date(l.created_at).toLocaleString('tr-TR') }}</td>
              <td class="px-4 py-2 font-medium text-slate-900 dark:text-white">{{ l.makine_kodu }}</td>
              <td class="px-4 py-2">%{{ Math.round(l.risk_orani * 100) }}</td>
              <td class="px-4 py-2">{{ l.ariza_tipi }}</td>
              <td class="px-4 py-2">{{ l.oncelik }}</td>
              <td class="px-4 py-2">{{ l.durum }}</td>
              <td class="px-4 py-2 text-slate-500 dark:text-slate-400">{{ l.karar_veren_username || '—' }}</td>
            </tr>
          </tbody>
        </table>
      </div>

      <div class="mt-3 flex items-center justify-between text-sm text-slate-500 dark:text-slate-400">
        <span>{{ t('toplam') }} {{ loglar.length }} {{ t('kayit') }} — {{ t('sayfa') }} {{ sayfa }} / {{ toplamSayfa }}</span>
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
