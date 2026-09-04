"""Demo amacli replay script.

data/processed.csv'deki satirlari zaman damgasi sirasiyla, gercek zamanli
bir sensor akisi gibi POST /tahminler endpoint'ine besler. Ekranin canli
akis hissi vermesi icin satirlar arasinda kucuk bir bekleme koyar.

Kullanim:
    python3 replay.py --sleep 0.2 --limit 200
"""

import argparse
import sys
from pathlib import Path

import pandas as pd
import requests

sys.path.insert(0, str(Path(__file__).resolve().parent))
from app.database import SessionLocal  # noqa: E402
from app.models import Makine  # noqa: E402

DATA_PATH = Path(__file__).resolve().parents[1] / "data" / "processed.csv"


def build_makine_id_map() -> dict[int, int]:
    db = SessionLocal()
    try:
        makineler = db.query(Makine).all()
        return {int(m.makine_kodu.split("-")[1]): m.id for m in makineler}
    finally:
        db.close()


def login(base_url: str, username: str, password: str) -> str:
    resp = requests.post(f"{base_url}/auth/login", data={"username": username, "password": password})
    resp.raise_for_status()
    return resp.json()["access_token"]


def main():
    parser = argparse.ArgumentParser(description="AI4I verisini API'ye canli akis gibi besler")
    parser.add_argument("--host", default="http://127.0.0.1:8000")
    parser.add_argument("--username", default="admin")
    parser.add_argument("--password", required=True)
    parser.add_argument("--sleep", type=float, default=0.1, help="Satirlar arasi bekleme (sn)")
    parser.add_argument("--limit", type=int, default=None, help="Islenecek maksimum satir sayisi")
    args = parser.parse_args()

    import time

    token = login(args.host, args.username, args.password)
    headers = {"Authorization": f"Bearer {token}"}

    makine_id_map = build_makine_id_map()

    df = pd.read_csv(DATA_PATH).sort_values("timestamp")
    if args.limit:
        df = df.head(args.limit)

    toplam, uyari = 0, 0
    for _, row in df.iterrows():
        makine_id = makine_id_map.get(int(row["machine_id"]))
        if makine_id is None:
            continue

        sensor = {
            "air_temperature": row["Air temperature [K]"],
            "process_temperature": row["Process temperature [K]"],
            "rotational_speed": row["Rotational speed [rpm]"],
            "torque": row["Torque [Nm]"],
            "tool_wear": row["Tool wear [min]"],
            "tip": row["Type"],
        }

        resp = requests.post(
            f"{args.host}/tahminler", json={"makine_id": makine_id, "sensor": sensor}, headers=headers
        )
        toplam += 1

        if resp.ok:
            body = resp.json()
            if body.get("risk_uyarisi") is False:
                print(f"[{toplam}] {row['timestamp']} M-{int(row['machine_id']):02d} -> risk yok")
            else:
                uyari += 1
                print(
                    f"[{toplam}] {row['timestamp']} M-{int(row['machine_id']):02d} -> "
                    f"RISK UYARISI ariza_tipi={body['ariza_tipi']} risk={body['risk_orani']:.2f} "
                    f"oncelik={body['oncelik']}"
                )
        else:
            print(f"[{toplam}] HATA {resp.status_code}: {resp.text}")

        time.sleep(args.sleep)

    print(f"\nBitti. Toplam {toplam} satir islendi, {uyari} risk uyarisi olusturuldu.")


if __name__ == "__main__":
    main()
