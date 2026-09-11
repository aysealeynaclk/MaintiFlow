# MaintiFlow

Sensör verisinden arıza riski üreten, bu riski SHAP ile gerekçelendiren ve makine kritikliği + stok durumuna göre önceliklendirilmiş iş emrine dönüştüren uçtan uca bir bakım karar destek sistemi.

AI4I 2020 Predictive Maintenance veri seti üzerinde eğitilmiş bir Random Forest modeli, FastAPI backend'i ve Vue 3 frontend'i ile tam bir web uygulamasına bağlandı.

## Akış

```
Sensör verisi → Model (risk + arıza tipi) → Öncelik hesaplama (risk × kritiklik × stok)
→ İş emri taslağı → Kullanıcı onayı → İş emirleri listesi
```

## Mimari

- **Model:** Python, scikit-learn (Random Forest), SHAP — `notebooks/` içinde Jupyter notebook'lar
- **Backend:** FastAPI, PostgreSQL (SQLAlchemy ORM + Alembic migration), JWT + bcrypt auth
- **Frontend:** Vue 3 + Vite + Tailwind CSS v4, TR/EN dil desteği, açık/koyu tema

## Proje Yapısı

```
data/           ai4i2020.csv (ham veri), processed.csv (işlenmiş veri)
notebooks/      01_eda, 02_feature_engineering, 03_model_training, 04_shap_explainability
models/         model.pkl ve eğitim/analiz çıktısı grafikler
backend/        FastAPI uygulaması, Alembic migration'ları, seed.py, replay.py
frontend/       Vue 3 + Vite uygulaması
```

## Model

1. **01_eda.ipynb** — Veri keşfi: sınıf dengesizliği (%3,4 arıza oranı), sensör dağılımları, ürün kalitesi (L/M/H) ile arıza ilişkisi.
2. **02_feature_engineering.ipynb** — Sentetik `machine_id`/`timestamp`, türetilmiş `temp_diff`/`power_w`/`tool_wear_critical` özellikleri, `failure_type` etiketi (TWF/HDF/PWF/OSF/NoFailure; RNF ayrı tutulur çünkü sensörlerden bağımsız rastgele oluşur).
3. **03_model_training.ipynb** — Stratified split, `RandomForestClassifier` (balanced ağırlıklara ek olarak TWF sınıfına 10x ekstra ağırlık), accuracy yerine PR-AUC ve eşik bazlı precision/recall ile değerlendirme.
4. **04_shap_explainability.ipynb** — SHAP `TreeExplainer` ile her tahmin için ilk 3 sensör gerekçesi.

**Sonuçlar:** PR-AUC 0,876; eşik=0,60'ta precision 0,536 / recall 0,881. TWF sınıfı (46 örnek) için `tool_wear_critical` özelliği + ek ağırlık ile recall %0'dan %44'e çıkarıldı — precision hâlâ düşük (~%9), çünkü veri seti bu sınıfı kritik bantta kasıtlı olarak rastgele tetikliyor; bu, feature engineering ile tamamen çözülebilecek bir sınır değil.

## Kurulum

### Model / notebook'lar

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

cp .env.example .env   # DATABASE_URL ve SECRET_KEY'i kendi değerlerinizle doldurun
```

Veritabanını hazırlayın:

```bash
alembic upgrade head
python3 seed.py   # 20 makine, yedek parça, arıza-parça eşlemesi ve bir admin kullanıcı oluşturur
```

Sunucuyu başlatın:

```bash
uvicorn app.main:app --reload
```

API dokümantasyonu: http://localhost:8000/docs

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Uygulama: http://localhost:5173

### Demo veri akışı

```bash
cd backend
python3 replay.py --password <admin_sifresi> --sleep 0.3 --limit 200
```

Veri setini zaman damgası sırasıyla API'ye besler; risk uyarıları anlık olarak Risk Listesi'nde görünür (sayfa 3 saniyede bir kendini yeniler). Aynı işlem admin panelindeki **Loglar** sayfasından bir düğmeyle de tetiklenebilir.

## Kullanıcı Akışı

1. **Giriş** — kullanıcı adı + şifre, JWT token alınır.
2. **Risk Listesi** — bekleyen riskler öncelik sırasına göre listelenir; makine koduna göre arama, sütun başlıklarına göre sıralama ve sayfalama var.
3. **Detay** — bir satıra tıklanınca kart açılır: tahmini tetikleyen ilk 3 sensör değeri, önerilen aksiyon, gerekli parça ve stok durumu; **Onayla**/**Reddet** butonları.
4. **İş Emirleri** — onaylanan kayıtlar burada listelenir; **Tamamlandı**/**İptal Et** ile sonuçlandırılabilir.
5. **Admin Paneli** — makine kritikliği ve stok yönetimi, tüm kararların logu (kim, ne zaman), kullanıcı yönetimi (oluşturma, şifre sıfırlama, pasife alma/silme, kullanıcı bazlı aktivite istatistiği).

## Roller

- **user:** Risk Listesi, Detay Ekranı, İş Emirleri ve kendi profiline erişir.
- **admin:** Ek olarak Admin Paneli'ne (Makineler, Stok, Loglar, Kullanıcılar) erişir. Admin hesapları hiçbir şekilde pasife alınamaz.

## Güvenlik

- Şifreler bcrypt ile hash'lenir, düz metin hiç saklanmaz.
- JWT tabanlı oturum (8 saat geçerlilik).
- Admin sayfaları sunucu tarafında rol kontrolüyle korunur — arayüzde bir düğmeyi gizlemek yeterli sayılmaz.
- Her onay/red/tamamlama işlemi hangi kullanıcı tarafından yapıldığı bilgisiyle birlikte kaydedilir.
- `.env` dosyaları (veritabanı şifresi, JWT secret) repoya dahil edilmez (`.gitignore`).

## Sınırlılıklar

- Otomatik test paketi (pytest vb.) yok — her uç nokta manuel/uçtan uca test edildi.
- Deploy edilmedi, yerel geliştirme ortamında çalışıyor.
- Replay script'i elle veya admin panelinden tetikleniyor, sürekli çalışan bir arka plan servisi değil.
