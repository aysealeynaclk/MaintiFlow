<script setup>
import { ref, computed, onMounted, onUnmounted, watch } from 'vue'
import client, { getErrorMessage } from '../api/client'

const SAYFA_BOYUTU = 20

const tahminler = ref([])
const toplam = ref(0)
const sayfa = ref(1)
const durum = ref('bekliyor')
const arama = ref('')
const yukleniyor = ref(true)
const hata = ref('')

const toplamSayfa = computed(() => Math.max(1, Math.ceil(toplam.value / SAYFA_BOYUTU)))

const durumEtiket = { bekliyor: 'Bekliyor', onaylandi: 'Onaylandı', reddedildi: 'Reddedildi' }
const durumRenk = {
  bekliyor: 'bg-amber-100 text-amber-800 dark:bg-amber-900/40 dark:text-amber-300',
  onaylandi: 'bg-emerald-100 text-emerald-800 dark:bg-emerald-900/40 dark:text-emerald-300',
  reddedildi: 'bg-slate-200 text-slate-600 dark:bg-slate-800 dark:text-slate-400',
}

function oncelikRenk(oncelik) {
  if (oncelik >= 4) return 'bg-red-100 text-red-700 dark:bg-red-900/40 dark:text-red-300'
  if (oncelik === 3) return 'bg-orange-100 text-orange-700 dark:bg-orange-900/40 dark:text-orange-300'
  return 'bg-slate-100 text-slate-600 dark:bg-slate-800 dark:text-slate-300'
}

async function yukle(sessiz = false) {
  if (!sessiz) yukleniyor.value = true
  hata.value = ''
  try {
    const params = {
      page: sayfa.value,
      page_size: SAYFA_BOYUTU,
      ...(durum.value ? { durum: durum.value } : {}),
      ...(arama.value ? { makine_kodu: arama.value } : {}),
    }
    const { data } = await client.get('/tahminler', { params })
    tahminler.value = data.items
    toplam.value = data.total
  } catch (err) {
    hata.value = getErrorMessage(err, 'Risk listesi yüklenemedi.')
  } finally {
    yukleniyor.value = false
  }
}

let zamanlayici = null
let aramaZamanlayici = null

onMounted(() => {
  yukle()
  // Canli akis hissi: yeni tahminler geldikce liste sessizce kendini yeniler.
  zamanlayici = setInterval(() => yukle(true), 3000)
})
onUnmounted(() => {
  clearInterval(zamanlayici)
  clearTimeout(aramaZamanlayici)
})

watch(durum, () => {
  sayfa.value = 1
  yukle()
})

watch(arama, () => {
  clearTimeout(aramaZamanlayici)
  aramaZamanlayici = setTimeout(() => {
    sayfa.value = 1
    yukle()
  }, 300)
})

watch(sayfa, () => yukle())

function sonrakiSayfa() {
  if (sayfa.value < toplamSayfa.value) sayfa.value++
}
function oncekiSayfa() {
  if (sayfa.value > 1) sayfa.value--
}
</script>

<template>
  <div>
    <div class="mb-4 flex flex-wrap items-center justify-between gap-3">
      <h1 class="text-xl font-semibold text-slate-900 dark:text-white">Risk Listesi</h1>
      <div class="flex gap-2">
        <input
          v-model="arama"
          type="text"
          placeholder="Makine ara (ör. M-01)"
          class="rounded-md border border-slate-300 px-3 py-1.5 text-sm dark:border-slate-700 dark:bg-slate-800 dark:text-white"
        />
        <select v-model="durum" class="rounded-md border border-slate-300 px-3 py-1.5 text-sm dark:border-slate-700 dark:bg-slate-800 dark:text-white">
          <option value="bekliyor">Bekleyenler</option>
          <option value="onaylandi">Onaylananlar</option>
          <option value="reddedildi">Reddedilenler</option>
          <option value="">Tümü</option>
        </select>
      </div>
    </div>

    <p v-if="hata" class="text-sm text-red-600 dark:text-red-400">{{ hata }}</p>
    <p v-else-if="yukleniyor" class="text-sm text-slate-500 dark:text-slate-400">Yükleniyor...</p>
    <p v-else-if="tahminler.length === 0" class="text-sm text-slate-500 dark:text-slate-400">Bu durumda kayıt yok.</p>

    <template v-else>
      <div class="overflow-x-auto rounded-lg border border-slate-200 dark:border-slate-800">
        <table class="w-full text-left text-sm">
          <thead class="bg-slate-100 text-slate-600 dark:bg-slate-800 dark:text-slate-300">
            <tr>
              <th class="px-4 py-2">Makine</th>
              <th class="px-4 py-2">Arıza Tipi</th>
              <th class="px-4 py-2">Risk</th>
              <th class="px-4 py-2">Öncelik</th>
              <th class="px-4 py-2">Durum</th>
              <th class="px-4 py-2">Tarih</th>
            </tr>
          </thead>
          <tbody>
            <tr
              v-for="t in tahminler"
              :key="t.id"
              class="cursor-pointer border-t border-slate-200 hover:bg-slate-50 dark:border-slate-800 dark:hover:bg-slate-800/50"
              @click="$router.push(`/tahmin/${t.id}`)"
            >
              <td class="px-4 py-2 font-medium text-slate-900 dark:text-white">{{ t.makine_kodu }}</td>
              <td class="px-4 py-2">{{ t.ariza_tipi }}</td>
              <td class="px-4 py-2">%{{ Math.round(t.risk_orani * 100) }}</td>
              <td class="px-4 py-2">
                <span class="rounded-full px-2 py-0.5 text-xs font-medium" :class="oncelikRenk(t.oncelik)">{{ t.oncelik }}</span>
              </td>
              <td class="px-4 py-2">
                <span class="rounded-full px-2 py-0.5 text-xs font-medium" :class="durumRenk[t.durum]">{{ durumEtiket[t.durum] }}</span>
              </td>
              <td class="px-4 py-2 text-slate-500 dark:text-slate-400">{{ new Date(t.created_at).toLocaleString('tr-TR') }}</td>
            </tr>
          </tbody>
        </table>
      </div>

      <div class="mt-3 flex items-center justify-between text-sm text-slate-500 dark:text-slate-400">
        <span>Toplam {{ toplam }} kayıt — sayfa {{ sayfa }} / {{ toplamSayfa }}</span>
        <div class="flex gap-2">
          <button
            @click="oncekiSayfa"
            :disabled="sayfa <= 1"
            class="rounded-md border border-slate-300 px-3 py-1 disabled:opacity-40 dark:border-slate-700"
          >
            ← Önceki
          </button>
          <button
            @click="sonrakiSayfa"
            :disabled="sayfa >= toplamSayfa"
            class="rounded-md border border-slate-300 px-3 py-1 disabled:opacity-40 dark:border-slate-700"
          >
            Sonraki →
          </button>
        </div>
      </div>
    </template>
  </div>
</template>
