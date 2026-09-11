<script setup>
import { useRouter } from 'vue-router'
import { useTahminDetay } from '../composables/useTahminDetay'
import { t } from '../stores/i18n'

const props = defineProps({ id: { type: [String, Number], required: true } })
const router = useRouter()

const { tahmin, yukleniyor, hata, islemYapiliyor, islemHata, karaVer } = useTahminDetay(props.id)

async function tikla(islem) {
  const basarili = await karaVer(islem)
  if (basarili) router.push('/')
}
</script>

<template>
  <div class="mx-auto max-w-2xl">
    <button @click="$router.push('/')" class="mb-4 text-sm text-slate-500 hover:text-slate-800 dark:text-slate-400 dark:hover:text-white">
      ← {{ t('riskListesi') }}
    </button>

    <p v-if="hata" class="text-sm text-red-600 dark:text-red-400">{{ hata }}</p>
    <p v-else-if="yukleniyor" class="text-sm text-slate-500 dark:text-slate-400">{{ t('yukleniyor') }}</p>

    <div v-else-if="tahmin" class="space-y-5">
      <div class="rounded-lg border border-slate-200 bg-white p-5 dark:border-slate-800 dark:bg-slate-900">
        <div class="mb-3 flex items-center justify-between">
          <h1 class="text-lg font-semibold text-slate-900 dark:text-white">{{ tahmin.makine_kodu }} — {{ tahmin.ariza_tipi }}</h1>
          <span class="rounded-full bg-red-100 px-3 py-1 text-sm font-medium text-red-700 dark:bg-red-900/40 dark:text-red-300">
            {{ t('colRisk') }} %{{ Math.round(tahmin.risk_orani * 100) }}
          </span>
        </div>
        <p class="text-sm text-slate-500 dark:text-slate-400">
          {{ t('colOncelik') }}: <span class="font-medium text-slate-800 dark:text-slate-200">{{ tahmin.oncelik }}</span>
          · {{ t('colDurum') }}: <span class="font-medium text-slate-800 dark:text-slate-200">{{ tahmin.durum }}</span>
        </p>
      </div>

      <div class="rounded-lg border border-slate-200 bg-white p-5 dark:border-slate-800 dark:bg-slate-900">
        <h2 class="mb-3 font-medium text-slate-900 dark:text-white">{{ t('tahminGerekcesi') }}</h2>
        <ul class="space-y-2 text-sm">
          <li v-for="g in tahmin.gerekce" :key="g.feature" class="flex justify-between border-b border-slate-100 pb-1 last:border-0 dark:border-slate-800">
            <span class="text-slate-600 dark:text-slate-300">{{ g.feature }}</span>
            <span class="font-mono text-slate-900 dark:text-white">{{ g.value.toFixed(2) }}</span>
          </li>
        </ul>
      </div>

      <div class="rounded-lg border border-slate-200 bg-white p-5 dark:border-slate-800 dark:bg-slate-900">
        <h2 class="mb-3 font-medium text-slate-900 dark:text-white">{{ t('onerilenAksiyon') }}</h2>
        <p v-if="tahmin.onerilen_aksiyon" class="text-sm text-slate-700 dark:text-slate-200">{{ tahmin.onerilen_aksiyon }}</p>
        <p v-if="tahmin.parca_adi" class="mt-2 text-sm text-slate-500 dark:text-slate-400">
          {{ t('gerekliParca') }}: <span class="text-slate-800 dark:text-slate-200">{{ tahmin.parca_adi }}</span>
          ({{ tahmin.parca_kodu }}) — {{ t('stokta') }}:
          <span :class="tahmin.stok_adet > 0 ? 'text-emerald-600 dark:text-emerald-400' : 'text-red-600 dark:text-red-400'">
            {{ tahmin.stok_adet }} {{ t('adet') }}
          </span>
        </p>
      </div>

      <p v-if="islemHata" class="text-sm text-red-600 dark:text-red-400">{{ islemHata }}</p>

      <div v-if="tahmin.durum === 'bekliyor'" class="flex gap-3">
        <button
          @click="tikla('onayla')"
          :disabled="islemYapiliyor"
          class="flex-1 rounded-md bg-emerald-600 py-2 font-medium text-white hover:bg-emerald-700 disabled:opacity-60"
        >
          {{ t('onayla') }}
        </button>
        <button
          @click="tikla('reddet')"
          :disabled="islemYapiliyor"
          class="flex-1 rounded-md bg-slate-200 py-2 font-medium text-slate-800 hover:bg-slate-300 disabled:opacity-60 dark:bg-slate-800 dark:text-slate-200 dark:hover:bg-slate-700"
        >
          {{ t('reddet') }}
        </button>
      </div>
    </div>
  </div>
</template>
