<script setup>
import { ref, computed, onMounted } from 'vue'
import client, { getErrorMessage } from '../../api/client'
import { t } from '../../stores/i18n'
import { useSiralama } from '../../composables/useSiralama'

const SAYFA_BOYUTU = 20

const makineler = ref([])
const yukleniyor = ref(true)
const hata = ref('')
const kaydediliyor = ref(null)
const sayfa = ref(1)

const { siralanmis, sirala } = useSiralama(makineler)

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
  yukleniyor.value = true
  hata.value = ''
  try {
    const { data } = await client.get('/admin/makineler')
    makineler.value = data
  } catch (err) {
    hata.value = getErrorMessage(err, 'Makineler yüklenemedi.')
  } finally {
    yukleniyor.value = false
  }
}

async function kritiklikGuncelle(makine) {
  kaydediliyor.value = makine.id
  hata.value = ''
  try {
    await client.patch(`/admin/makineler/${makine.id}`, { kritiklik: Number(makine.kritiklik) })
  } catch (err) {
    hata.value = getErrorMessage(err, 'Güncelleme başarısız.')
    await yukle()
  } finally {
    kaydediliyor.value = null
  }
}

onMounted(yukle)
</script>

<template>
  <div>
    <h1 class="mb-4 text-xl font-semibold text-slate-900 dark:text-white">{{ t('makineYonetimi') }}</h1>
    <p v-if="hata" class="mb-3 text-sm text-red-600 dark:text-red-400">{{ hata }}</p>
    <p v-if="yukleniyor" class="text-sm text-slate-500 dark:text-slate-400">{{ t('yukleniyor') }}</p>

    <template v-else>
      <div class="overflow-x-auto rounded-lg border border-slate-200 dark:border-slate-800">
        <table class="w-full text-left text-sm">
          <thead class="bg-slate-100 text-slate-600 dark:bg-slate-800 dark:text-slate-300">
            <tr>
              <th class="cursor-pointer select-none px-4 py-2" @click="siralaVeBastaBasla('makine_kodu')">{{ t('colKod') }} ⇅</th>
              <th class="cursor-pointer select-none px-4 py-2" @click="siralaVeBastaBasla('ad')">{{ t('colAd') }} ⇅</th>
              <th class="cursor-pointer select-none px-4 py-2" @click="siralaVeBastaBasla('tip')">{{ t('colTip') }} ⇅</th>
              <th class="cursor-pointer select-none px-4 py-2" @click="siralaVeBastaBasla('kritiklik')">{{ t('colKritiklik') }} ⇅</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="m in sayfalanmis" :key="m.id" class="border-t border-slate-200 dark:border-slate-800">
              <td class="px-4 py-2 font-medium text-slate-900 dark:text-white">{{ m.makine_kodu }}</td>
              <td class="px-4 py-2">{{ m.ad }}</td>
              <td class="px-4 py-2">{{ m.tip }}</td>
              <td class="px-4 py-2">
                <select
                  v-model="m.kritiklik"
                  @change="kritiklikGuncelle(m)"
                  :disabled="kaydediliyor === m.id"
                  class="rounded-md border border-slate-300 px-2 py-1 dark:border-slate-700 dark:bg-slate-800 dark:text-white"
                >
                  <option v-for="n in [1, 2, 3, 4, 5]" :key="n" :value="n">{{ n }}</option>
                </select>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <div class="mt-3 flex items-center justify-between text-sm text-slate-500 dark:text-slate-400">
        <span>{{ t('toplam') }} {{ makineler.length }} {{ t('kayit') }} — {{ t('sayfa') }} {{ sayfa }} / {{ toplamSayfa }}</span>
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
