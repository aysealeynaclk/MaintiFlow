import math

from app.models import Stok


def stok_katsayisi(stok: Stok | None) -> float:
    """Parca stokta yoksa tedarik suresi devreye girdigi icin katsayi artar."""
    if stok is None:
        return 1.0
    return 1.5 if stok.adet <= 0 else 1.0


def compute_oncelik(risk_orani: float, kritiklik: int, katsayi: float) -> int:
    """Oncelik = risk x kritiklik x katsayi, 1-5 araligina normalize edilir.

    Max deger 1.0 * 5 * 1.5 = 7.5 oldugu icin 1.5'lik dilimlere bolup
    1-5 arasi tam sayiya yuvarliyoruz.
    """
    raw = risk_orani * kritiklik * katsayi
    return min(5, max(1, math.ceil(raw / 1.5)))
