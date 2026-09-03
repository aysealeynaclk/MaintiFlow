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
2. **02_feature_engineering.ipynb** — Sentetik `machine_id`/`timestamp`, türetilmiş `temp_diff`/`power_w`/`tool_wear_critical` özellikleri, `failure_type` etiketi (TWF/HDF/PWF/OSF/NoFailure; RNF ayrı tutulur çünkü sensörlerden bağımsız rastgele oluşur).
3. **03_model_training.ipynb** — Stratified split, `RandomForestClassifier` (balanced ağırlıklara ek olarak TWF sınıfına 10x ekstra ağırlık), accuracy yerine PR-AUC ve eşik bazlı precision/recall ile değerlendirme.
4. **04_shap_explainability.ipynb** — SHAP `TreeExplainer` ile her tahmin için ilk 3 sensör gerekçesi.

## Bilinen Durum

- HDF/PWF/OSF arıza tipleri model tarafından iyi öğreniliyor.
- **TWF** için `tool_wear_critical` (Tool wear ≥ 200 dk bandı) özelliği ve sınıfa 10x ek ağırlık eklendi: recall 0 → 0.44'e çıktı, ancak precision düşük kalıyor (~0.09). Bu, veri setinin TWF'i kritik bantta kasıtlı olarak rastgele tetiklemesinden kaynaklanıyor — feature engineering ile tamamen çözülebilecek bir sınır değil. Bu değişiklik ikili risk skorunu da etkiledi: PR-AUC 0.894 → 0.876, eşik=0.60'da precision 0.818 → 0.536, recall 0.806 → 0.881 (detay: 03_model_training.ipynb).
- Backend, veritabanı ve frontend tarafına henüz başlanmadı.
