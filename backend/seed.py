"""MAKINELER, STOK, ARIZA_PARCA ve bir admin kullanicisini seed eder.

Kritiklik (1-5), her makinenin islenmis veri setindeki (data/processed.csv)
gecmis ariza sayisina gore quintile'a bolunerek turetilir - daha cok arizali
makine daha kritik kabul edilir. Tip, o makinenin en sik gorulen Type
degeridir (senteik machine_id atamasi round-robin oldugu icin bir makine
birden fazla Type icerebiliyor, bu bilinen bir sinirlama).
"""

import getpass
import os
import sys
from pathlib import Path

import pandas as pd

from app.database import Base, SessionLocal, engine
from app.models import ArizaParca, Makine, Stok, User, UserRole, UserStatus
from app.security import hash_password

DATA_PATH = Path(__file__).resolve().parents[1] / "data" / "processed.csv"

ARIZA_PARCA_DATA = [
    ("TWF", "PRC-TOOL-01", "Kesici takim/freze ucunu degistir"),
    ("HDF", "PRC-COOL-01", "Sogutma fanini kontrol et, gerekirse degistir"),
    ("PWF", "PRC-DRV-01", "Motor surucusunu/inverteri kontrol et"),
    ("OSF", "PRC-SHAFT-01", "Sahat/kaplin yukunu kontrol et, gerekirse degistir"),
]

STOK_DATA = [
    ("PRC-TOOL-01", "Kesici Takim (Freze Ucu)", 12, 3),
    ("PRC-COOL-01", "Sogutma Fani", 5, 7),
    ("PRC-DRV-01", "Motor Suruculu/Inverter Karti", 2, 14),
    ("PRC-SHAFT-01", "Aktarma Sahati/Kaplin", 4, 10),
]


def build_makineler(df: pd.DataFrame) -> list[Makine]:
    fail_counts = df.groupby("machine_id")["Machine failure"].sum()
    kritiklik_by_machine = pd.qcut(fail_counts.rank(method="first"), 5, labels=[1, 2, 3, 4, 5]).astype(int)
    tip_by_machine = df.groupby("machine_id")["Type"].agg(lambda s: s.mode().iloc[0])

    makineler = []
    for machine_id in sorted(df["machine_id"].unique()):
        makineler.append(
            Makine(
                makine_kodu=f"M-{machine_id:02d}",
                ad=f"Makine {machine_id:02d}",
                tip=tip_by_machine.loc[machine_id],
                kritiklik=int(kritiklik_by_machine.loc[machine_id]),
            )
        )
    return makineler


def main():
    Base.metadata.create_all(bind=engine)
    df = pd.read_csv(DATA_PATH)

    db = SessionLocal()
    try:
        if db.query(Makine).count() > 0:
            print("MAKINELER zaten dolu, seed atlaniyor.")
            return

        db.add_all(build_makineler(df))

        for parca_kodu, ad, adet, tedarik_gun in STOK_DATA:
            db.add(Stok(parca_kodu=parca_kodu, ad=ad, adet=adet, tedarik_gun=tedarik_gun))
        db.flush()

        for ariza_tipi, parca_kodu, aksiyon in ARIZA_PARCA_DATA:
            db.add(ArizaParca(ariza_tipi=ariza_tipi, parca_kodu=parca_kodu, onerilen_aksiyon=aksiyon))

        if db.query(User).filter_by(username="admin").first() is None:
            admin_password = os.environ.get("ADMIN_PASSWORD")
            if not admin_password:
                if sys.stdin.isatty():
                    admin_password = getpass.getpass("Admin kullanicisi icin sifre belirleyin: ")
                else:
                    admin_password = sys.stdin.readline().strip()
            db.add(
                User(
                    username="admin",
                    password_hash=hash_password(admin_password),
                    role=UserRole.admin,
                    status=UserStatus.active,
                )
            )

        db.commit()
        print("Seed tamamlandi: 20 makine, 4 parca, 4 ariza-parca eslemesi, 1 admin kullanici.")
    finally:
        db.close()


if __name__ == "__main__":
    main()
