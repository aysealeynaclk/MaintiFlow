import { ref } from 'vue'
import client, { getErrorMessage } from '../api/client'

export function useTahminDetay(id) {
  const tahmin = ref(null)
  const yukleniyor = ref(true)
  const hata = ref('')
  const islemYapiliyor = ref(false)
  const islemHata = ref('')

  async function yukle() {
    yukleniyor.value = true
    hata.value = ''
    try {
      const { data } = await client.get(`/tahminler/${id}`)
      tahmin.value = data
    } catch (err) {
      hata.value = getErrorMessage(err, 'Tahmin bulunamadı.')
    } finally {
      yukleniyor.value = false
    }
  }

  async function karaVer(islem) {
    islemHata.value = ''
    islemYapiliyor.value = true
    try {
      await client.post(`/tahminler/${id}/${islem}`)
      return true
    } catch (err) {
      islemHata.value = getErrorMessage(err, 'İşlem gerçekleştirilemedi.')
      return false
    } finally {
      islemYapiliyor.value = false
    }
  }

  yukle()

  return { tahmin, yukleniyor, hata, islemYapiliyor, islemHata, karaVer, yukle }
}
