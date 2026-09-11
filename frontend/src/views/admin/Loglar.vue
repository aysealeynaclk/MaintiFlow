<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import client, { getErrorMessage } from '../../api/client'
import { t } from '../../stores/i18n'
import { useSiralama } from '../../composables/useSiralama'

const SAYFA_BOYUTU = 20

const loglar = ref([])
const yukleniyor = ref(true)
const hata = ref('')
const sayfa = ref(1)

const replaySleep = ref(0.3)
const replayLimit = ref(200)
const replayDurum = ref({ calisiyor: false, islenen: 0, toplam: 0, uyari: 0 })
const replayHata = ref('')
const replayBaslatiliyor = ref(false)
let replayZamanlayici = null

async function replayDurumGetir() {
  try {
    const { data } = await client.get('/admin/replay/durum')
    replayDurum.value = data
    if (!data.calisiyor && replayZamanlayici) {
      clearInterval(replayZamanlayici)
      replayZamanlayici = null
      await yukle()
    }
  } catch {
    // sessizce gec, bir sonraki tikte tekrar denenir
  }
}

async function replayBaslatTikla() {
  replayHata.value = ''
  replayBaslatiliyor.value = true
  try {
    await client.post('/admin/replay/baslat', null, {
      params: { sleep: replaySleep.value, limit: replayLimit.value },
    })
    await replayDurumGetir()
    if (!replayZamanlayici) {
      replayZamanlayici = setInterval(replayDurumGetir, 1000)
    }
  } catch (err) {
    replayHata.value = getErrorMessage(err, 'Replay başlatılamadı.')
  } finally {
    replayBaslatiliyor.value = false
  }
}

onUnmounted(() => clearInterval(replayZamanlayici))

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

async function yukle() {
  try {
    const { data } = await client.get('/admin/loglar')
    loglar.value = data
  } catch (err) {
    hata.value = getErrorMessage(err, 'Loglar yüklenemedi.')
  } finally {
    yukleniyor.value = false
  }
}

onMounted(async () => {
  await yukle()
  await replayDurumGetir()
  if (replayDurum.value.calisiyor) {
    replayZamanlayici = setInterval(replayDurumGetir, 1000)
  }
})
</script>

<template>
  <div>
    <h1 class="mb-4 text-xl font-semibold text-slate-900 dark:text-white">{{ t('loglar') }}</h1>

    <div class="mb-4 flex flex-wrap items-end gap-3 rounded-lg border border-slate-200 bg-white p-4 dark:border-slate-800 dark:bg-slate-900">
      <div>
        <label class="mb-1 block text-xs text-slate-500 dark:text-slate-400">{{ t('replaySleepLabel') }}</label>
        <input
          v-model.number="replaySleep"
          type="number"
          min="0"
          max="5"
          step="0.1"
          :disabled="replayDurum.calisiyor"
          class="w-24 rounded-md border border-slate-300 px-2 py-1.5 text-sm dark:border-slate-700 dark:bg-slate-800 dark:text-white"
        />
      </div>
      <div>
        <label class="mb-1 block text-xs text-slate-500 dark:text-slate-400">{{ t('replayLimitLabel') }}</label>
        <input
          v-model.number="replayLimit"
          type="number"
          min="1"
          max="10000"
          :disabled="replayDurum.calisiyor"
          class="w-28 rounded-md border border-slate-300 px-2 py-1.5 text-sm dark:border-slate-700 dark:bg-slate-800 dark:text-white"
        />
      </div>
      <button
        @click="replayBaslatTikla"
        :disabled="replayBaslatiliyor || replayDurum.calisiyor"
        class="rounded-md bg-sky-600 px-4 py-1.5 text-sm font-medium text-white hover:bg-sky-700 disabled:opacity-60"
      >
        {{ replayBaslatiliyor ? t('replayBaslatiliyor') : t('replayBaslat') }}
      </button>

      <span class="flex items-center gap-1.5 text-sm">
        <span class="h-2 w-2 rounded-full" :class="replayDurum.calisiyor ? 'bg-emerald-500' : 'bg-slate-300 dark:bg-slate-600'"></span>
        <span v-if="replayDurum.calisiyor" class="text-slate-600 dark:text-slate-300">
          {{ t('replayCalisiyorEtiket') }}: {{ replayDurum.islenen }}/{{ replayDurum.toplam }} — {{ replayDurum.uyari }} {{ t('replayUyariKelimesi') }}
        </span>
        <span v-else class="text-slate-400 dark:text-slate-500">{{ t('replayBostaEtiket') }}</span>
      </span>

      <p v-if="replayHata" class="w-full text-sm text-red-600 dark:text-red-400">{{ replayHata }}</p>
    </div>

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
