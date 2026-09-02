# MaintiFlow

Kestirimci bakım (predictive maintenance) için makine öğrenmesi tabanlı arıza riski tahmin ve açıklanabilirlik projesi. AI4I 2020 Predictive Maintenance veri seti üzerinde eğitilmiş bir model, her tahmin için SHAP ile "neden riskli" gerekçesi üretir.

Planlanan tam sistem: FastAPI backend + Vue frontend + PostgreSQL (henüz başlanmadı). Şu an proje ML/model tarafında.

## Proje Yapısı

```
data/           ai4i2020.csv (ham veri), processed.csv (işlenmiş veri)
notebooks/      01_eda, 02_feature_engineering, 03_model_training, 04_shap_explainability
models/         model.pkl ve eğitim/analiz çıktısı grafikler
```

## Kurulum

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Notebook Sırası

1. **01_eda.ipynb** — Veri keşfi: sınıf dengesizliği, sensör dağılımları, ürün kalitesi (L/M/H) ile arıza ilişkisi.
2. **02_feature_engineering.ipynb** — Sentetik `machine_id`/`timestamp`, türetilmiş `temp_diff`/`power_w` özellikleri, `failure_type` etiketi (TWF/HDF/PWF/OSF/NoFailure; RNF ayrı tutulur çünkü sensörlerden bağımsız rastgele oluşur).
3. **03_model_training.ipynb** — Stratified split, `RandomForestClassifier(class_weight='balanced')`, accuracy yerine PR-AUC ve eşik bazlı precision/recall ile değerlendirme.
4. **04_shap_explainability.ipynb** — SHAP `TreeExplainer` ile her tahmin için ilk 3 sensör gerekçesi.

## Bilinen Durum

- HDF/PWF arıza tipleri model tarafından iyi öğreniliyor; **TWF az örnek + kasıtlı rastgelelik nedeniyle henüz öğrenilemiyor** — sıradaki adım bunun için özellik/ağırlık iyileştirmesi.
- Backend, veritabanı ve frontend tarafına henüz başlanmadı.
