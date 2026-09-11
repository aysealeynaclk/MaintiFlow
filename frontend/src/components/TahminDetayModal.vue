<script setup>
import { useTahminDetay } from '../composables/useTahminDetay'
import { t } from '../stores/i18n'

const props = defineProps({ id: { type: [String, Number], required: true } })
const emit = defineEmits(['kapat', 'guncellendi'])

const { tahmin, yukleniyor, hata, islemYapiliyor, islemHata, karaVer } = useTahminDetay(props.id)

const modelGorselleri = [
  { dosya: 'shap_summary.png', baslik: 'SHAP Özellik Önemi' },
  { dosya: 'feature_importance.png', baslik: 'Özellik Önem Sıralaması' },
  { dosya: 'confusion_matrix.png', baslik: 'Confusion Matrix' },
  { dosya: 'pr_curve.png', baslik: 'Precision-Recall Eğrisi' },
  { dosya: 'threshold_confusion_matrix.png', baslik: 'Eşik=0.60 Confusion Matrix' },
  { dosya: 'eda_class_balance.png', baslik: 'Sınıf Dengesizliği' },
  { dosya: 'eda_sensor_distributions.png', baslik: 'Sensör Dağılımları' },
]

async function tikla(islem) {
  const basarili = await karaVer(islem)
  if (basarili) {
    emit('guncellendi')
    emit('kapat')
  }
}
</script>

<template>
  <div class="fixed inset-0 z-50 flex items-center justify-center bg-black/50 p-4" @click.self="$emit('kapat')">
    <div class="max-h-[85vh] w-full max-w-lg overflow-y-auto rounded-xl bg-white p-6 shadow-2xl dark:bg-slate-900">
      <div class="mb-4 flex items-center justify-between">
        <h2 class="text-lg font-semibold text-slate-900 dark:text-white">{{ t('tahminDetayi') }}</h2>
        <button @click="$emit('kapat')" class="text-xl leading-none text-slate-400 hover:text-slate-700 dark:hover:text-white">✕</button>
      </div>

      <p v-if="hata" class="text-sm text-red-600 dark:text-red-400">{{ hata }}</p>
      <p v-else-if="yukleniyor" class="text-sm text-slate-500 dark:text-slate-400">{{ t('yukleniyor') }}</p>

      <div v-else-if="tahmin" class="space-y-5">
        <div class="rounded-lg border border-slate-200 p-4 dark:border-slate-800">
          <div class="mb-2 flex items-center justify-between">
            <h3 class="font-semibold text-slate-900 dark:text-white">{{ tahmin.makine_kodu }} — {{ tahmin.ariza_tipi }}</h3>
            <span class="rounded-full bg-red-100 px-3 py-1 text-sm font-medium text-red-700 dark:bg-red-900/40 dark:text-red-300">
              {{ t('colRisk') }} %{{ Math.round(tahmin.risk_orani * 100) }}
            </span>
          </div>
          <p class="text-sm text-slate-500 dark:text-slate-400">
            {{ t('colOncelik') }}: <span class="font-medium text-slate-800 dark:text-slate-200">{{ tahmin.oncelik }}</span>
            · {{ t('colDurum') }}: <span class="font-medium text-slate-800 dark:text-slate-200">{{ tahmin.durum }}</span>
          </p>
        </div>

        <div class="rounded-lg border border-slate-200 p-4 dark:border-slate-800">
          <h3 class="mb-3 font-medium text-slate-900 dark:text-white">{{ t('tahminGerekcesi') }}</h3>
          <ul class="space-y-2 text-sm">
            <li v-for="g in tahmin.gerekce" :key="g.feature" class="flex justify-between border-b border-slate-100 pb-1 last:border-0 dark:border-slate-800">
              <span class="text-slate-600 dark:text-slate-300">{{ g.feature }}</span>
              <span class="font-mono text-slate-900 dark:text-white">{{ g.value.toFixed(2) }}</span>
            </li>
          </ul>
        </div>

        <div class="rounded-lg border border-slate-200 p-4 dark:border-slate-800">
          <h3 class="mb-3 font-medium text-slate-900 dark:text-white">{{ t('onerilenAksiyon') }}</h3>
          <p v-if="tahmin.onerilen_aksiyon" class="text-sm text-slate-700 dark:text-slate-200">{{ tahmin.onerilen_aksiyon }}</p>
          <p v-if="tahmin.parca_adi" class="mt-2 text-sm text-slate-500 dark:text-slate-400">
            {{ t('gerekliParca') }}: <span class="text-slate-800 dark:text-slate-200">{{ tahmin.parca_adi }}</span>
            ({{ tahmin.parca_kodu }}) — {{ t('stokta') }}:
            <span :class="tahmin.stok_adet > 0 ? 'text-emerald-600 dark:text-emerald-400' : 'text-red-600 dark:text-red-400'">
              {{ tahmin.stok_adet }} {{ t('adet') }}
            </span>
          </p>
        </div>

        <details class="rounded-lg border border-slate-200 dark:border-slate-800">
          <summary class="cursor-pointer px-4 py-3 text-sm font-medium text-slate-700 dark:text-slate-200">
            {{ t('modelDegerlendirmesi') }}
          </summary>
          <div class="grid grid-cols-2 gap-3 border-t border-slate-100 p-4 dark:border-slate-800">
            <a
              v-for="g in modelGorselleri"
              :key="g.dosya"
              :href="`/gorseller/${g.dosya}`"
              target="_blank"
              rel="noopener"
              class="block"
            >
              <img :src="`/gorseller/${g.dosya}`" :alt="g.baslik" class="w-full rounded-md border border-slate-200 dark:border-slate-700" />
              <p class="mt-1 text-center text-xs text-slate-500 dark:text-slate-400">{{ g.baslik }}</p>
            </a>
          </div>
        </details>

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
  </div>
</template>
