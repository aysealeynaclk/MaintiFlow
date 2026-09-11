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

const dict = {
  tr: {
    // Navbar / genel
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
    yukleniyor: 'Yükleniyor...',
    kayitYok: 'Kayıt yok.',

    // Ortak tablo sutunlari
    colMakine: 'Makine',
    colArizaTipi: 'Arıza Tipi',
    colRisk: 'Risk',
    colOncelik: 'Öncelik',
    colDurum: 'Durum',
    colTarih: 'Tarih',
    colAksiyon: 'Aksiyon',
    colParca: 'Parça',
    colKarar: 'Karar',
    colKararVeren: 'Karar Veren',
    colKod: 'Kod',
    colAd: 'Ad',
    colTip: 'Tip',
    colKritiklik: 'Kritiklik (1-5)',
    colParcaKodu: 'Parça Kodu',
    colAdet: 'Adet',
    colTedarikGun: 'Tedarik (gün)',

    // Ortak sayfalama
    toplam: 'Toplam',
    kayit: 'kayıt',
    oncekiSayfa: '‹ Önceki',
    sonrakiSayfa: 'Sonraki ›',
    sayfa: 'Sayfa',

    // Durum etiketleri
    durumBekliyor: 'Bekliyor',
    durumOnaylandi: 'Onaylandı',
    durumReddedildi: 'Reddedildi',
    durumBekleyenler: 'Bekleyenler',
    durumOnaylananlar: 'Onaylananlar',
    durumReddedilenler: 'Reddedilenler',
    durumTumu: 'Tümü',
    durumTamamlandi: 'Tamamlandı',
    durumIptal: 'İptal',
    tamamla: 'Tamamlandı',
    iptalEt: 'İptal Et',

    // Risk Listesi
    riskAramaPlaceholder: 'Makine ara (ör. M-01)',

    // Detay (kart/modal)
    tahminDetayi: 'Tahmin Detayı',
    tahminGerekcesi: 'Tahmin Gerekçesi',
    onerilenAksiyon: 'Önerilen Aksiyon',
    gerekliParca: 'Gerekli parça',
    stokta: 'Stokta',
    adet: 'adet',
    onayla: 'Onayla',
    reddet: 'Reddet',

    // Is Emirleri
    isEmriYok: 'Henüz onaylanmış bir iş emri yok.',

    // Admin - Makineler / Stok
    makineYonetimi: 'Makine Yönetimi',
    stokYonetimi: 'Stok Yönetimi',
    kaydet: 'Kaydet',

    // Login
    kullaniciAdi: 'Kullanıcı adı',
    sifre: 'Şifre',
    girisYap: 'Giriş Yap',
    girisYapiliyor: 'Giriş yapılıyor...',

    // Profil
    profilBilgileri: 'Profil Bilgileri',
    yeniSifreOpsiyonel: 'Yeni şifre (opsiyonel)',
    yeniSifreTekrar: 'Yeni şifre (tekrar)',
    mevcutSifreOnay: 'Mevcut şifre (onay için gerekli)',
    goster: 'Göster',
    gizle: 'Gizle',
    kaydediliyor: 'Kaydediliyor...',
    rol: 'Rol',

    // Admin - Kullanicilar
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
    pasifeAl: 'Pasife Al',
    aktifEt: 'Aktif Et',
    sil: 'Sil',
    adminKorunuyor: 'admin hesabı korunuyor',
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
    yukleniyor: 'Loading...',
    kayitYok: 'No records.',

    colMakine: 'Machine',
    colArizaTipi: 'Failure Type',
    colRisk: 'Risk',
    colOncelik: 'Priority',
    colDurum: 'Status',
    colTarih: 'Date',
    colAksiyon: 'Action',
    colParca: 'Part',
    colKarar: 'Decision',
    colKararVeren: 'Decided By',
    colKod: 'Code',
    colAd: 'Name',
    colTip: 'Type',
    colKritiklik: 'Criticality (1-5)',
    colParcaKodu: 'Part Code',
    colAdet: 'Qty',
    colTedarikGun: 'Lead Time (days)',

    toplam: 'Total',
    kayit: 'records',
    oncekiSayfa: '‹ Previous',
    sonrakiSayfa: 'Next ›',
    sayfa: 'Page',

    durumBekliyor: 'Pending',
    durumOnaylandi: 'Approved',
    durumReddedildi: 'Rejected',
    durumBekleyenler: 'Pending',
    durumOnaylananlar: 'Approved',
    durumReddedilenler: 'Rejected',
    durumTumu: 'All',
    durumTamamlandi: 'Completed',
    durumIptal: 'Cancelled',
    tamamla: 'Complete',
    iptalEt: 'Cancel',

    riskAramaPlaceholder: 'Search machine (e.g. M-01)',

    tahminDetayi: 'Prediction Detail',
    tahminGerekcesi: 'Prediction Reasoning',
    onerilenAksiyon: 'Recommended Action',
    gerekliParca: 'Required part',
    stokta: 'In stock',
    adet: 'units',
    onayla: 'Approve',
    reddet: 'Reject',

    isEmriYok: 'No approved work orders yet.',

    makineYonetimi: 'Machine Management',
    stokYonetimi: 'Stock Management',
    kaydet: 'Save',

    kullaniciAdi: 'Username',
    sifre: 'Password',
    girisYap: 'Log In',
    girisYapiliyor: 'Logging in...',

    profilBilgileri: 'Profile Info',
    yeniSifreOpsiyonel: 'New password (optional)',
    yeniSifreTekrar: 'New password (repeat)',
    mevcutSifreOnay: 'Current password (required to confirm)',
    goster: 'Show',
    gizle: 'Hide',
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
    pasifeAl: 'Deactivate',
    aktifEt: 'Activate',
    sil: 'Delete',
    adminKorunuyor: 'admin account protected',
  },
}

export function t(key) {
  return dict[i18n.locale]?.[key] ?? dict.tr[key] ?? key
}
