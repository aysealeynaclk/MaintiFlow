<script setup>
import { ref, onMounted } from 'vue'
import client, { getErrorMessage } from '../../api/client'

const makineler = ref([])
const yukleniyor = ref(true)
const hata = ref('')
const kaydediliyor = ref(null)

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
    <h1 class="mb-4 text-xl font-semibold text-slate-900 dark:text-white">Makine Yönetimi</h1>
    <p v-if="hata" class="mb-3 text-sm text-red-600 dark:text-red-400">{{ hata }}</p>
    <p v-if="yukleniyor" class="text-sm text-slate-500 dark:text-slate-400">Yükleniyor...</p>

    <div v-else class="overflow-x-auto rounded-lg border border-slate-200 dark:border-slate-800">
      <table class="w-full text-left text-sm">
        <thead class="bg-slate-100 text-slate-600 dark:bg-slate-800 dark:text-slate-300">
          <tr>
            <th class="px-4 py-2">Kod</th>
            <th class="px-4 py-2">Ad</th>
            <th class="px-4 py-2">Tip</th>
            <th class="px-4 py-2">Kritiklik (1-5)</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="m in makineler" :key="m.id" class="border-t border-slate-200 dark:border-slate-800">
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
  </div>
</template>
