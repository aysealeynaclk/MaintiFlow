<script setup>
import { ref, computed, onMounted } from 'vue'
import client, { getErrorMessage } from '../../api/client'
import { t } from '../../stores/i18n'

const SAYFA_BOYUTU = 20

const stoklar = ref([])
const yukleniyor = ref(true)
const hata = ref('')
const kaydediliyor = ref(null)
const sayfa = ref(1)

const toplamSayfa = computed(() => Math.max(1, Math.ceil(stoklar.value.length / SAYFA_BOYUTU)))
const sayfalanmis = computed(() => {
  const baslangic = (sayfa.value - 1) * SAYFA_BOYUTU
  return stoklar.value.slice(baslangic, baslangic + SAYFA_BOYUTU)
})

async function yukle() {
  yukleniyor.value = true
  hata.value = ''
  try {
    const { data } = await client.get('/admin/stok')
    stoklar.value = data
  } catch (err) {
    hata.value = getErrorMessage(err, 'Stok yüklenemedi.')
  } finally {
    yukleniyor.value = false
  }
}

async function guncelle(s) {
  kaydediliyor.value = s.id
  hata.value = ''
  try {
    await client.patch(`/admin/stok/${s.id}`, {
      adet: Number(s.adet),
      tedarik_gun: Number(s.tedarik_gun),
    })
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
    <h1 class="mb-4 text-xl font-semibold text-slate-900 dark:text-white">{{ t('stokYonetimi') }}</h1>
    <p v-if="hata" class="mb-3 text-sm text-red-600 dark:text-red-400">{{ hata }}</p>
    <p v-if="yukleniyor" class="text-sm text-slate-500 dark:text-slate-400">{{ t('yukleniyor') }}</p>

    <template v-else>
      <div class="overflow-x-auto rounded-lg border border-slate-200 dark:border-slate-800">
        <table class="w-full text-left text-sm">
          <thead class="bg-slate-100 text-slate-600 dark:bg-slate-800 dark:text-slate-300">
            <tr>
              <th class="px-4 py-2">{{ t('colParcaKodu') }}</th>
              <th class="px-4 py-2">{{ t('colAd') }}</th>
              <th class="px-4 py-2">{{ t('colAdet') }}</th>
              <th class="px-4 py-2">{{ t('colTedarikGun') }}</th>
              <th class="px-4 py-2"></th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="s in sayfalanmis" :key="s.id" class="border-t border-slate-200 dark:border-slate-800">
              <td class="px-4 py-2 font-medium text-slate-900 dark:text-white">{{ s.parca_kodu }}</td>
              <td class="px-4 py-2">{{ s.ad }}</td>
              <td class="px-4 py-2">
                <input
                  v-model="s.adet"
                  type="number"
                  min="0"
                  class="w-20 rounded-md border border-slate-300 px-2 py-1 dark:border-slate-700 dark:bg-slate-800 dark:text-white"
                />
              </td>
              <td class="px-4 py-2">
                <input
                  v-model="s.tedarik_gun"
                  type="number"
                  min="0"
                  class="w-20 rounded-md border border-slate-300 px-2 py-1 dark:border-slate-700 dark:bg-slate-800 dark:text-white"
                />
              </td>
              <td class="px-4 py-2">
                <button
                  @click="guncelle(s)"
                  :disabled="kaydediliyor === s.id"
                  class="rounded-md bg-sky-600 px-3 py-1 text-white hover:bg-sky-700 disabled:opacity-60"
                >
                  {{ t('kaydet') }}
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <div class="mt-3 flex items-center justify-between text-sm text-slate-500 dark:text-slate-400">
        <span>{{ t('toplam') }} {{ stoklar.length }} {{ t('kayit') }} — {{ t('sayfa') }} {{ sayfa }} / {{ toplamSayfa }}</span>
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
