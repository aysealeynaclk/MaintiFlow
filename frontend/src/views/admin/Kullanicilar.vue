<script setup>
import { ref, reactive, onMounted } from 'vue'
import client, { getErrorMessage } from '../../api/client'
import { auth } from '../../stores/auth'

const kullanicilar = ref([])
const yukleniyor = ref(true)
const hata = ref('')

const yeniKullanici = reactive({ username: '', password: '', role: 'user' })
const olusturHata = ref('')
const olusturuluyor = ref(false)

const sifirlananSifre = ref(null) // { username, sifre }
const islemDurumu = reactive({}) // { [userId]: { sifirlaniyor, siliniyor, hata } }

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
    <h1 class="text-xl font-semibold text-slate-900 dark:text-white">Kullanıcı Yönetimi</h1>

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

    <form @submit.prevent="kullaniciOlustur" class="flex flex-wrap items-end gap-3 rounded-lg border border-slate-200 bg-white p-4 dark:border-slate-800 dark:bg-slate-900">
      <div>
        <label class="mb-1 block text-xs text-slate-500 dark:text-slate-400">Kullanıcı adı</label>
        <input v-model="yeniKullanici.username" required class="rounded-md border border-slate-300 px-2 py-1.5 text-sm dark:border-slate-700 dark:bg-slate-800 dark:text-white" />
      </div>
      <div>
        <label class="mb-1 block text-xs text-slate-500 dark:text-slate-400">Şifre</label>
        <input v-model="yeniKullanici.password" type="password" required class="rounded-md border border-slate-300 px-2 py-1.5 text-sm dark:border-slate-700 dark:bg-slate-800 dark:text-white" />
      </div>
      <div>
        <label class="mb-1 block text-xs text-slate-500 dark:text-slate-400">Rol</label>
        <select v-model="yeniKullanici.role" class="rounded-md border border-slate-300 px-2 py-1.5 text-sm dark:border-slate-700 dark:bg-slate-800 dark:text-white">
          <option value="user">user</option>
          <option value="admin">admin</option>
        </select>
      </div>
      <button type="submit" :disabled="olusturuluyor" class="rounded-md bg-sky-600 px-4 py-1.5 text-sm font-medium text-white hover:bg-sky-700 disabled:opacity-60">
        Kullanıcı Oluştur
      </button>
      <p v-if="olusturHata" class="w-full text-sm text-red-600 dark:text-red-400">{{ olusturHata }}</p>
    </form>

    <p v-if="hata" class="text-sm text-red-600 dark:text-red-400">{{ hata }}</p>
    <p v-if="yukleniyor" class="text-sm text-slate-500 dark:text-slate-400">Yükleniyor...</p>

    <div v-else class="overflow-x-auto rounded-lg border border-slate-200 dark:border-slate-800">
      <table class="w-full text-left text-sm">
        <thead class="bg-slate-100 text-slate-600 dark:bg-slate-800 dark:text-slate-300">
          <tr>
            <th class="px-4 py-2">Kullanıcı adı</th>
            <th class="px-4 py-2">Rol</th>
            <th class="px-4 py-2">Durum</th>
            <th class="px-4 py-2"></th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="u in kullanicilar" :key="u.id" class="border-t border-slate-200 dark:border-slate-800">
            <td class="px-4 py-2 font-medium text-slate-900 dark:text-white">{{ u.username }}</td>
            <td class="px-4 py-2">{{ u.role }}</td>
            <td class="px-4 py-2">
              <span
                class="rounded-full px-2 py-0.5 text-xs font-medium"
                :class="u.status === 'active' ? 'bg-emerald-100 text-emerald-800 dark:bg-emerald-900/40 dark:text-emerald-300' : 'bg-slate-200 text-slate-600 dark:bg-slate-800 dark:text-slate-400'"
              >
                {{ u.status }}
              </span>
            </td>
            <td class="px-4 py-2">
              <div class="flex items-center gap-2">
                <button
                  @click="sifreSifirla(u)"
                  :disabled="islemDurumu[u.id]?.sifirlaniyor"
                  class="rounded-md bg-slate-100 px-3 py-1 text-xs hover:bg-slate-200 disabled:opacity-50 dark:bg-slate-800 dark:hover:bg-slate-700"
                >
                  Şifreyi Sıfırla
                </button>
                <button
                  v-if="!(u.id === auth.user?.id && u.status === 'active')"
                  @click="durumDegistir(u)"
                  class="rounded-md bg-slate-100 px-3 py-1 text-xs hover:bg-slate-200 dark:bg-slate-800 dark:hover:bg-slate-700"
                >
                  {{ u.status === 'active' ? 'Pasife Al' : 'Aktif Et' }}
                </button>
                <button
                  v-if="u.status === 'inactive' && u.id !== auth.user?.id"
                  @click="kullaniciSil(u)"
                  :disabled="islemDurumu[u.id]?.siliniyor"
                  class="rounded-md bg-red-50 px-3 py-1 text-xs text-red-700 hover:bg-red-100 disabled:opacity-50 dark:bg-red-900/30 dark:text-red-300 dark:hover:bg-red-900/50"
                >
                  Sil
                </button>
              </div>
              <p v-if="islemDurumu[u.id]?.hata" class="mt-1 text-xs text-red-600 dark:text-red-400">{{ islemDurumu[u.id].hata }}</p>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>
