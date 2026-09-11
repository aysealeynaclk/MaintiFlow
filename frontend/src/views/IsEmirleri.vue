<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import client, { getErrorMessage } from '../api/client'
import { t } from '../stores/i18n'
import { useSiralama } from '../composables/useSiralama'

const SAYFA_BOYUTU = 20

const isEmirleri = ref([])
const yukleniyor = ref(true)
const hata = ref('')
const sayfa = ref(1)
const islemDurumu = reactive({}) // { [id]: { yapiliyor, hata } }

const { siralanmis, sirala } = useSiralama(isEmirleri)

const durumEtiketAnahtari = { bekliyor: 'durumBekliyor', tamamlandi: 'durumTamamlandi', iptal: 'durumIptal' }
const durumRenk = {
  bekliyor: 'bg-amber-100 text-amber-800 dark:bg-amber-900/40 dark:text-amber-300',
  tamamlandi: 'bg-emerald-100 text-emerald-800 dark:bg-emerald-900/40 dark:text-emerald-300',
  iptal: 'bg-slate-200 text-slate-600 dark:bg-slate-800 dark:text-slate-400',
}

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
    const { data } = await client.get('/is-emirleri')
    isEmirleri.value = data
    data.forEach((e) => {
      if (!islemDurumu[e.id]) islemDurumu[e.id] = { yapiliyor: false, hata: '' }
    })
  } catch (err) {
    hata.value = getErrorMessage(err, 'İş emirleri yüklenemedi.')
  } finally {
    yukleniyor.value = false
  }
}

async function karaVer(isEmri, islem) {
  const d = islemDurumu[isEmri.id]
  d.hata = ''
  d.yapiliyor = true
  try {
    await client.post(`/is-emirleri/${isEmri.id}/${islem}`)
    await yukle()
  } catch (err) {
    d.hata = getErrorMessage(err, 'İşlem gerçekleştirilemedi.')
  } finally {
    d.yapiliyor = false
  }
}

onMounted(yukle)
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
              <th class="cursor-pointer select-none px-4 py-2" @click="siralaVeBastaBasla('makine_kodu')">{{ t('colMakine') }} ⇅</th>
              <th class="cursor-pointer select-none px-4 py-2" @click="siralaVeBastaBasla('aksiyon')">{{ t('colAksiyon') }} ⇅</th>
              <th class="cursor-pointer select-none px-4 py-2" @click="siralaVeBastaBasla('parca_kodu')">{{ t('colParca') }} ⇅</th>
              <th class="cursor-pointer select-none px-4 py-2" @click="siralaVeBastaBasla('oncelik')">{{ t('colOncelik') }} ⇅</th>
              <th class="cursor-pointer select-none px-4 py-2" @click="siralaVeBastaBasla('durum')">{{ t('colDurum') }} ⇅</th>
              <th class="cursor-pointer select-none px-4 py-2" @click="siralaVeBastaBasla('created_at')">{{ t('colTarih') }} ⇅</th>
              <th class="px-4 py-2"></th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="e in sayfalanmis" :key="e.id" class="border-t border-slate-200 dark:border-slate-800">
              <td class="px-4 py-2 font-medium text-slate-900 dark:text-white">{{ e.makine_kodu }}</td>
              <td class="px-4 py-2">{{ e.aksiyon }}</td>
              <td class="px-4 py-2 text-slate-500 dark:text-slate-400">{{ e.parca_kodu }}</td>
              <td class="px-4 py-2">{{ e.oncelik }}</td>
              <td class="px-4 py-2">
                <span class="rounded-full px-2 py-0.5 text-xs font-medium" :class="durumRenk[e.durum]">{{ t(durumEtiketAnahtari[e.durum]) }}</span>
              </td>
              <td class="px-4 py-2 text-slate-500 dark:text-slate-400">{{ new Date(e.created_at).toLocaleString('tr-TR') }}</td>
              <td class="px-4 py-2">
                <div v-if="e.durum === 'bekliyor'" class="flex gap-2">
                  <button
                    @click="karaVer(e, 'tamamla')"
                    :disabled="islemDurumu[e.id]?.yapiliyor"
                    class="rounded-md bg-emerald-50 px-2 py-1 text-xs text-emerald-700 hover:bg-emerald-100 disabled:opacity-50 dark:bg-emerald-900/30 dark:text-emerald-300 dark:hover:bg-emerald-900/50"
                  >
                    {{ t('tamamla') }}
                  </button>
                  <button
                    @click="karaVer(e, 'iptal-et')"
                    :disabled="islemDurumu[e.id]?.yapiliyor"
                    class="rounded-md bg-slate-100 px-2 py-1 text-xs text-slate-600 hover:bg-slate-200 disabled:opacity-50 dark:bg-slate-800 dark:text-slate-300 dark:hover:bg-slate-700"
                  >
                    {{ t('iptalEt') }}
                  </button>
                </div>
                <p v-if="islemDurumu[e.id]?.hata" class="mt-1 text-xs text-red-600 dark:text-red-400">{{ islemDurumu[e.id].hata }}</p>
              </td>
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
