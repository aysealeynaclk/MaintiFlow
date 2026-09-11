"""Admin panelinden tetiklenen replay - replay.py ile ayni mantik ama
HTTP uzerinden kendi kendini cagirmak yerine dogrudan servis fonksiyonlarini
kullanir, arka planda bir thread icinde calisir.
"""

import threading
import time
from pathlib import Path

import pandas as pd

from app import ml_model
from app.database import SessionLocal
from app.models import ArizaParca, Makine, Tahmin, TahminDurum
from app.priority import compute_oncelik, stok_katsayisi

DATA_PATH = Path(__file__).resolve().parents[2] / "data" / "processed.csv"

_durum = {"calisiyor": False, "islenen": 0, "toplam": 0, "uyari": 0}
_kilit = threading.Lock()


def durum_getir() -> dict:
    return dict(_durum)


def _replay_calistir(sleep_saniye: float, limit: int | None):
    db = SessionLocal()
    try:
        makineler = {int(m.makine_kodu.split("-")[1]): m.id for m in db.query(Makine).all()}
        df = pd.read_csv(DATA_PATH).sort_values("timestamp")
        if limit:
            df = df.head(limit)

        _durum["toplam"] = len(df)
        _durum["islenen"] = 0
        _durum["uyari"] = 0

        for _, row in df.iterrows():
            makine_id = makineler.get(int(row["machine_id"]))
            if makine_id is not None:
                sensor = {
                    "air_temperature": row["Air temperature [K]"],
                    "process_temperature": row["Process temperature [K]"],
                    "rotational_speed": row["Rotational speed [rpm]"],
                    "torque": row["Torque [Nm]"],
                    "tool_wear": row["Tool wear [min]"],
                    "tip": row["Type"],
                }
                result = ml_model.predict(sensor)

                if result["risk_uyarisi"]:
                    ariza_parca = (
                        db.query(ArizaParca).filter(ArizaParca.ariza_tipi == result["ariza_tipi"]).first()
                    )
                    katsayi = stok_katsayisi(ariza_parca.stok if ariza_parca else None)
                    makine = db.get(Makine, makine_id)
                    oncelik = compute_oncelik(result["risk_orani"], makine.kritiklik, katsayi)
                    db.add(
                        Tahmin(
                            makine_id=makine_id,
                            risk_orani=result["risk_orani"],
                            ariza_tipi=result["ariza_tipi"],
                            gerekce=result["gerekce"],
                            oncelik=oncelik,
                            durum=TahminDurum.bekliyor,
                        )
                    )
                    db.commit()
                    _durum["uyari"] += 1

            _durum["islenen"] += 1
            time.sleep(sleep_saniye)
    finally:
        db.close()
        with _kilit:
            _durum["calisiyor"] = False


def replay_baslat(sleep_saniye: float, limit: int | None) -> bool:
    with _kilit:
        if _durum["calisiyor"]:
            return False
        _durum["calisiyor"] = True

    thread = threading.Thread(target=_replay_calistir, args=(sleep_saniye, limit), daemon=True)
    thread.start()
    return True
