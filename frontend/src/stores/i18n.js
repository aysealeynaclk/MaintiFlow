import { reactive, watchEffect } from 'vue'

const stored = localStorage.getItem('maintiflow_locale')

export const i18n = reactive({
  locale: stored || 'tr',
  setLocale(l) {
    this.locale = l
  },
})

watchEffect(() => {
  localStorage.setItem('maintiflow_locale', i18n.locale)
})

// Not: su an sadece ust menu, profil ve kullanici yonetimi sayfalari
// cevriliyor - uygulamanin geri kalani henuz TR-only.
const dict = {
  tr: {
    riskListesi: 'Risk Listesi',
    isEmirleri: 'İş Emirleri',
    makineler: 'Makineler',
    stok: 'Stok',
    loglar: 'Loglar',
    kullanicilar: 'Kullanıcılar',
    profilim: 'Profilim',
    cikisYap: 'Çıkış Yap',
    gorunum: 'Görünüm',
    dil: 'Dil',
    acik: 'Açık',
    koyu: 'Koyu',
    profilBilgileri: 'Profil Bilgileri',
    kullaniciAdi: 'Kullanıcı adı',
    yeniSifreOpsiyonel: 'Yeni şifre (opsiyonel)',
    yeniSifreTekrar: 'Yeni şifre (tekrar)',
    mevcutSifreOnay: 'Mevcut şifre (onay için gerekli)',
    goster: 'Göster',
    gizle: 'Gizle',
    kaydet: 'Kaydet',
    kaydediliyor: 'Kaydediliyor...',
    rol: 'Rol',
    kullaniciYonetimi: 'Kullanıcı Yönetimi',
    yeniKullanici: 'Yeni Kullanıcı',
    kullaniciOlustur: 'Kullanıcı Oluştur',
    tumDurumlar: 'Tüm durumlar',
    aktif: 'Aktif',
    pasif: 'Pasif',
    araPlaceholder: 'Kullanıcı adına göre ara',
    kullaniciBaslik: 'KULLANICI',
    durumBaslik: 'DURUM',
    kayitTarihiBaslik: 'KAYIT TARİHİ',
    islemlerBaslik: 'İŞLEMLER',
    sifre: 'Şifre',
    pasifeAl: 'Pasife Al',
    aktifEt: 'Aktif Et',
    sil: 'Sil',
    adminKorunuyor: 'admin hesabı korunuyor',
    toplam: 'Toplam',
    kayit: 'kayıt',
    oncekiSayfa: '‹ Önceki',
    sonrakiSayfa: 'Sonraki ›',
    sayfa: 'Sayfa',
  },
  en: {
    riskListesi: 'Risk List',
    isEmirleri: 'Work Orders',
    makineler: 'Machines',
    stok: 'Stock',
    loglar: 'Logs',
    kullanicilar: 'Users',
    profilim: 'My Profile',
    cikisYap: 'Log Out',
    gorunum: 'Appearance',
    dil: 'Language',
    acik: 'Light',
    koyu: 'Dark',
    profilBilgileri: 'Profile Info',
    kullaniciAdi: 'Username',
    yeniSifreOpsiyonel: 'New password (optional)',
    yeniSifreTekrar: 'New password (repeat)',
    mevcutSifreOnay: 'Current password (required to confirm)',
    goster: 'Show',
    gizle: 'Hide',
    kaydet: 'Save',
    kaydediliyor: 'Saving...',
    rol: 'Role',
    kullaniciYonetimi: 'User Management',
    yeniKullanici: 'New User',
    kullaniciOlustur: 'Create User',
    tumDurumlar: 'All statuses',
    aktif: 'Active',
    pasif: 'Inactive',
    araPlaceholder: 'Search by username',
    kullaniciBaslik: 'USER',
    durumBaslik: 'STATUS',
    kayitTarihiBaslik: 'REGISTERED',
    islemlerBaslik: 'ACTIONS',
    sifre: 'Password',
    pasifeAl: 'Deactivate',
    aktifEt: 'Activate',
    sil: 'Delete',
    adminKorunuyor: 'admin account protected',
    toplam: 'Total',
    kayit: 'records',
    oncekiSayfa: '‹ Previous',
    sonrakiSayfa: 'Next ›',
    sayfa: 'Page',
  },
}

export function t(key) {
  return dict[i18n.locale]?.[key] ?? dict.tr[key] ?? key
}
