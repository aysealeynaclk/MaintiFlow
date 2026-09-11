import { ref, computed } from 'vue'

/** Bir dizi referansini basliga tiklayarak siralamak icin kucuk bir yardimci. */
export function useSiralama(kaynakRef) {
  const siralamaAlan = ref(null)
  const siralamaYon = ref('asc')

  const siralanmis = computed(() => {
    if (!siralamaAlan.value) return kaynakRef.value
    const alan = siralamaAlan.value
    const yon = siralamaYon.value === 'asc' ? 1 : -1
    return [...kaynakRef.value].sort((a, b) => {
      if (a[alan] < b[alan]) return -1 * yon
      if (a[alan] > b[alan]) return 1 * yon
      return 0
    })
  })

  function sirala(alan) {
    if (siralamaAlan.value === alan) {
      siralamaYon.value = siralamaYon.value === 'asc' ? 'desc' : 'asc'
    } else {
      siralamaAlan.value = alan
      siralamaYon.value = 'asc'
    }
  }

  return { siralamaAlan, siralamaYon, siralanmis, sirala }
}
