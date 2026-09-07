<script setup>
import { ref, onMounted } from 'vue'
import client, { getErrorMessage } from '../../api/client'

const loglar = ref([])
const yukleniyor = ref(true)
const hata = ref('')

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
    <h1 class="mb-4 text-xl font-semibold text-slate-900 dark:text-white">Loglar</h1>
    <p v-if="hata" class="text-sm text-red-600 dark:text-red-400">{{ hata }}</p>
    <p v-else-if="yukleniyor" class="text-sm text-slate-500 dark:text-slate-400">Yükleniyor...</p>

    <div v-else class="overflow-x-auto rounded-lg border border-slate-200 dark:border-slate-800">
      <table class="w-full text-left text-sm">
        <thead class="bg-slate-100 text-slate-600 dark:bg-slate-800 dark:text-slate-300">
          <tr>
            <th class="px-4 py-2">Tarih</th>
            <th class="px-4 py-2">Makine</th>
            <th class="px-4 py-2">Risk</th>
            <th class="px-4 py-2">Arıza Tipi</th>
            <th class="px-4 py-2">Öncelik</th>
            <th class="px-4 py-2">Karar</th>
            <th class="px-4 py-2">Karar Veren</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="l in loglar" :key="l.id" class="border-t border-slate-200 dark:border-slate-800">
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
  </div>
</template>
