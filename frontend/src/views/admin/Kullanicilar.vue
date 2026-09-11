<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import client, { getErrorMessage } from '../../api/client'
import { t } from '../../stores/i18n'
import KullaniciIstatistikModal from '../../components/KullaniciIstatistikModal.vue'

const secilenKullanici = ref(null) // { id, username }

const SAYFA_BOYUTU = 20

const kullanicilar = ref([])
const yukleniyor = ref(true)
const hata = ref('')

const arama = ref('')
const durumFiltre = ref('')
const siralamaAlan = ref('created_at')
const siralamaYon = ref('desc')
const sayfa = ref(1)

const yeniKullanici = reactive({ username: '', password: '', role: 'user' })
const olusturHata = ref('')
const olusturuluyor = ref(false)

const sifirlananSifre = ref(null)
const islemDurumu = reactive({})

function initialler(username) {
  return (username || '?').slice(0, 2).toUpperCase()
}

async function yukle() {
  yukleniyor.value = true
  hata.value = ''
  try {
    const { data } = await client.get('/admin/kullanicilar')
    kullanicilar.value = data
    data.forEach((u) => {
      if (!islemDurumu[u.id]) islemDurumu[u.id] = { sifirlaniyor: false, siliniyor: false, hata: '' }
    })
  } catch (err) {
    hata.value = getErrorMessage(err, 'Kullanıcılar yüklenemedi.')
  } finally {
    yukleniyor.value = false
  }
}

const filtrelenmis = computed(() => {
  let liste = kullanicilar.value
  if (arama.value) {
    const q = arama.value.toLocaleLowerCase('tr')
    liste = liste.filter((u) => u.username.toLocaleLowerCase('tr').includes(q))
  }
  if (durumFiltre.value) {
    liste = liste.filter((u) => u.status === durumFiltre.value)
  }
  return liste
})

const siralanmis = computed(() => {
  const alan = siralamaAlan.value
  const yon = siralamaYon.value === 'asc' ? 1 : -1
  return [...filtrelenmis.value].sort((a, b) => {
    if (a[alan] < b[alan]) return -1 * yon
    if (a[alan] > b[alan]) return 1 * yon
    return 0
  })
})

const toplamSayfa = computed(() => Math.max(1, Math.ceil(siralanmis.value.length / SAYFA_BOYUTU)))

const sayfalanmis = computed(() => {
  const baslangic = (sayfa.value - 1) * SAYFA_BOYUTU
  return siralanmis.value.slice(baslangic, baslangic + SAYFA_BOYUTU)
})

function sirala(alan) {
  if (siralamaAlan.value === alan) {
    siralamaYon.value = siralamaYon.value === 'asc' ? 'desc' : 'asc'
  } else {
    siralamaAlan.value = alan
    siralamaYon.value = 'asc'
  }
}

async function kullaniciOlustur() {
  olusturHata.value = ''
  olusturuluyor.value = true
  try {
    await client.post('/admin/kullanicilar', { ...yeniKullanici })
    yeniKullanici.username = ''
    yeniKullanici.password = ''
    yeniKullanici.role = 'user'
    await yukle()
  } catch (err) {
    olusturHata.value = getErrorMessage(err, 'Kullanıcı oluşturulamadı.')
  } finally {
    olusturuluyor.value = false
  }
}

async function sifreSifirla(kullanici) {
  const d = islemDurumu[kullanici.id]
  d.hata = ''
  d.sifirlaniyor = true
  try {
    const { data } = await client.post(`/admin/kullanicilar/${kullanici.id}/sifre-sifirla`)
    sifirlananSifre.value = { username: kullanici.username, sifre: data.yeni_sifre }
  } catch (err) {
    d.hata = getErrorMessage(err, 'Şifre sıfırlanamadı.')
  } finally {
    d.sifirlaniyor = false
  }
}

async function durumDegistir(kullanici) {
  hata.value = ''
  const yeniDurum = kullanici.status === 'active' ? 'inactive' : 'active'
  try {
    await client.patch(`/admin/kullanicilar/${kullanici.id}/durum`, { status: yeniDurum })
    await yukle()
  } catch (err) {
    hata.value = getErrorMessage(err, 'Durum güncellenemedi.')
  }
}

async function kullaniciSil(kullanici) {
  if (!confirm(`"${kullanici.username}" kullanıcısını kalıcı olarak silmek istediğinize emin misiniz?`)) return
  const d = islemDurumu[kullanici.id]
  d.hata = ''
  d.siliniyor = true
  try {
    await client.delete(`/admin/kullanicilar/${kullanici.id}`)
    await yukle()
  } catch (err) {
    d.hata = getErrorMessage(err, 'Kullanıcı silinemedi.')
  } finally {
    d.siliniyor = false
  }
}

onMounted(yukle)
</script>

<template>
  <div class="space-y-6">
    <h1 class="text-xl font-semibold text-slate-900 dark:text-white">{{ t('kullaniciYonetimi') }}</h1>

    <div
      v-if="sifirlananSifre"
      class="flex items-center justify-between rounded-lg border border-amber-300 bg-amber-50 px-4 py-3 text-sm dark:border-amber-800 dark:bg-amber-900/30"
    >
      <span class="text-amber-900 dark:text-amber-200">
        <strong>{{ sifirlananSifre.username }}</strong> için yeni şifre:
        <code class="rounded bg-white px-2 py-0.5 font-mono dark:bg-slate-900">{{ sifirlananSifre.sifre }}</code>
        — bu şifre bir daha gösterilmeyecek, kullanıcıya iletin.
      </span>
      <button @click="sifirlananSifre = null" class="text-amber-700 hover:text-amber-900 dark:text-amber-300">✕</button>
    </div>

    <details class="rounded-lg border border-slate-200 bg-white dark:border-slate-800 dark:bg-slate-900">
      <summary class="cursor-pointer px-4 py-3 text-sm font-medium text-slate-700 dark:text-slate-200">{{ t('yeniKullanici') }}</summary>
      <form @submit.prevent="kullaniciOlustur" class="flex flex-wrap items-end gap-3 border-t border-slate-100 p-4 dark:border-slate-800">
        <div>
          <label class="mb-1 block text-xs text-slate-500 dark:text-slate-400">{{ t('kullaniciAdi') }}</label>
          <input v-model="yeniKullanici.username" required class="rounded-md border border-slate-300 px-2 py-1.5 text-sm dark:border-slate-700 dark:bg-slate-800 dark:text-white" />
        </div>
        <div>
          <label class="mb-1 block text-xs text-slate-500 dark:text-slate-400">{{ t('sifre') }}</label>
          <input v-model="yeniKullanici.password" type="password" required class="rounded-md border border-slate-300 px-2 py-1.5 text-sm dark:border-slate-700 dark:bg-slate-800 dark:text-white" />
        </div>
        <div>
          <label class="mb-1 block text-xs text-slate-500 dark:text-slate-400">{{ t('rol') }}</label>
          <select v-model="yeniKullanici.role" class="rounded-md border border-slate-300 px-2 py-1.5 text-sm dark:border-slate-700 dark:bg-slate-800 dark:text-white">
            <option value="user">user</option>
            <option value="admin">admin</option>
          </select>
        </div>
        <button type="submit" :disabled="olusturuluyor" class="rounded-md bg-sky-600 px-4 py-1.5 text-sm font-medium text-white hover:bg-sky-700 disabled:opacity-60">
          {{ t('kullaniciOlustur') }}
        </button>
        <p v-if="olusturHata" class="w-full text-sm text-red-600 dark:text-red-400">{{ olusturHata }}</p>
      </form>
    </details>

    <div class="flex flex-wrap justify-end gap-3">
      <input
        v-model="arama"
        type="text"
        :placeholder="t('araPlaceholder')"
        class="rounded-md border border-slate-300 px-3 py-1.5 text-sm dark:border-slate-700 dark:bg-slate-800 dark:text-white"
      />
      <select v-model="durumFiltre" class="rounded-md border border-slate-300 px-3 py-1.5 text-sm dark:border-slate-700 dark:bg-slate-800 dark:text-white">
        <option value="">{{ t('tumDurumlar') }}</option>
        <option value="active">{{ t('aktif') }}</option>
        <option value="inactive">{{ t('pasif') }}</option>
      </select>
    </div>

    <p v-if="hata" class="text-sm text-red-600 dark:text-red-400">{{ hata }}</p>
    <p v-if="yukleniyor" class="text-sm text-slate-500 dark:text-slate-400">Yükleniyor...</p>

    <template v-else>
      <div class="overflow-x-auto rounded-lg border border-slate-200 dark:border-slate-800">
        <table class="w-full text-left text-sm">
          <thead class="bg-slate-100 text-xs uppercase tracking-wide text-slate-500 dark:bg-slate-800 dark:text-slate-400">
            <tr>
              <th class="cursor-pointer select-none px-4 py-2" @click="sirala('username')">{{ t('kullaniciBaslik') }} ⇅</th>
              <th class="cursor-pointer select-none px-4 py-2" @click="sirala('status')">{{ t('durumBaslik') }} ⇅</th>
              <th class="cursor-pointer select-none px-4 py-2" @click="sirala('created_at')">{{ t('kayitTarihiBaslik') }} ⇅</th>
              <th class="px-4 py-2">{{ t('islemlerBaslik') }}</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="u in sayfalanmis" :key="u.id" class="border-t border-slate-200 dark:border-slate-800">
              <td class="cursor-pointer px-4 py-3" @click="secilenKullanici = { id: u.id, username: u.username }" :title="t('kullaniciIstatistigi')">
                <div class="flex items-center gap-3">
                  <div class="flex h-9 w-9 items-center justify-center rounded-lg bg-sky-600 text-xs font-semibold text-white">
                    {{ initialler(u.username) }}
                  </div>
                  <div>
                    <p class="font-medium text-slate-900 hover:underline dark:text-white">{{ u.username }}</p>
                    <p class="text-xs text-slate-500 dark:text-slate-400">{{ u.role }}</p>
                  </div>
                </div>
              </td>
              <td class="px-4 py-3">
                <span class="flex items-center gap-1.5" :class="u.status === 'active' ? 'text-emerald-600 dark:text-emerald-400' : 'text-slate-400 dark:text-slate-500'">
                  <span class="h-2 w-2 rounded-full" :class="u.status === 'active' ? 'bg-emerald-500' : 'bg-slate-400'"></span>
                  {{ u.status === 'active' ? t('aktif') : t('pasif') }}
                </span>
              </td>
              <td class="px-4 py-3 text-slate-500 dark:text-slate-400">{{ new Date(u.created_at).toLocaleDateString('tr-TR') }}</td>
              <td class="px-4 py-3">
                <div class="flex flex-wrap items-center gap-3 text-sm">
                  <button
                    @click="sifreSifirla(u)"
                    :disabled="islemDurumu[u.id]?.sifirlaniyor"
                    class="text-sky-600 underline hover:text-sky-800 disabled:opacity-50 dark:text-sky-400 dark:hover:text-sky-300"
                  >
                    {{ t('sifre') }}
                  </button>

                  <span v-if="u.role === 'admin'" class="italic text-slate-400 dark:text-slate-500">{{ t('adminKorunuyor') }}</span>
                  <button
                    v-else
                    @click="durumDegistir(u)"
                    class="underline"
                    :class="u.status === 'active' ? 'text-slate-600 hover:text-slate-900 dark:text-slate-300 dark:hover:text-white' : 'text-emerald-600 hover:text-emerald-800 dark:text-emerald-400'"
                  >
                    {{ u.status === 'active' ? t('pasifeAl') : t('aktifEt') }}
                  </button>

                  <button
                    v-if="u.status === 'inactive' && u.role !== 'admin'"
                    @click="kullaniciSil(u)"
                    :disabled="islemDurumu[u.id]?.siliniyor"
                    class="text-red-600 underline hover:text-red-800 disabled:opacity-50 dark:text-red-400 dark:hover:text-red-300"
                  >
                    {{ t('sil') }}
                  </button>
                </div>
                <p v-if="islemDurumu[u.id]?.hata" class="mt-1 text-xs text-red-600 dark:text-red-400">{{ islemDurumu[u.id].hata }}</p>
              </td>
            </tr>
            <tr v-if="sayfalanmis.length === 0">
              <td colspan="4" class="px-4 py-6 text-center text-slate-500 dark:text-slate-400">Kayıt yok.</td>
            </tr>
          </tbody>
        </table>
      </div>

      <div class="flex items-center justify-between text-sm text-slate-500 dark:text-slate-400">
        <span>{{ t('toplam') }} {{ siralanmis.length }} {{ t('kayit') }}</span>
        <div class="flex items-center gap-3">
          <button
            @click="sayfa > 1 && sayfa--"
            :disabled="sayfa <= 1"
            class="rounded-md border border-slate-300 px-3 py-1 disabled:opacity-40 dark:border-slate-700"
          >
            {{ t('oncekiSayfa') }}
          </button>
          <span>{{ t('sayfa') }} {{ sayfa }} / {{ toplamSayfa }}</span>
          <button
            @click="sayfa < toplamSayfa && sayfa++"
            :disabled="sayfa >= toplamSayfa"
            class="rounded-md border border-slate-300 px-3 py-1 disabled:opacity-40 dark:border-slate-700"
          >
            {{ t('sonrakiSayfa') }}
          </button>
        </div>
      </div>
    </template>

    <KullaniciIstatistikModal
      v-if="secilenKullanici"
      :id="secilenKullanici.id"
      :username="secilenKullanici.username"
      @kapat="secilenKullanici = null"
    />
  </div>
</template>
