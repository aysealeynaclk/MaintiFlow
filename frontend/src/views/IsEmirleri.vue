<script setup>
import { ref, onMounted } from 'vue'
import client, { getErrorMessage } from '../api/client'

const isEmirleri = ref([])
const yukleniyor = ref(true)
const hata = ref('')

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
    <h1 class="mb-4 text-xl font-semibold text-slate-900 dark:text-white">İş Emirleri</h1>

    <p v-if="hata" class="text-sm text-red-600 dark:text-red-400">{{ hata }}</p>
    <p v-else-if="yukleniyor" class="text-sm text-slate-500 dark:text-slate-400">Yükleniyor...</p>
    <p v-else-if="isEmirleri.length === 0" class="text-sm text-slate-500 dark:text-slate-400">Henüz onaylanmış bir iş emri yok.</p>

    <div v-else class="overflow-x-auto rounded-lg border border-slate-200 dark:border-slate-800">
      <table class="w-full text-left text-sm">
        <thead class="bg-slate-100 text-slate-600 dark:bg-slate-800 dark:text-slate-300">
          <tr>
            <th class="px-4 py-2">Makine</th>
            <th class="px-4 py-2">Aksiyon</th>
            <th class="px-4 py-2">Parça</th>
            <th class="px-4 py-2">Öncelik</th>
            <th class="px-4 py-2">Durum</th>
            <th class="px-4 py-2">Tarih</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="e in isEmirleri" :key="e.id" class="border-t border-slate-200 dark:border-slate-800">
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
  </div>
</template>
