from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import ml_model
from app.database import get_db
from app.deps import get_current_user
from app.models import ArizaParca, Makine, Tahmin, TahminDurum, User
from app.priority import compute_oncelik, stok_katsayisi
from app.schemas import TahminCreateIn, TahminOut

router = APIRouter(prefix="/tahminler", tags=["tahminler"])


def _to_out(tahmin: Tahmin) -> TahminOut:
    return TahminOut(
        id=tahmin.id,
        makine_id=tahmin.makine_id,
        makine_kodu=tahmin.makine.makine_kodu,
        risk_orani=tahmin.risk_orani,
        ariza_tipi=tahmin.ariza_tipi.value,
        gerekce=tahmin.gerekce,
        oncelik=tahmin.oncelik,
        durum=tahmin.durum,
        created_at=tahmin.created_at,
    )


@router.post("", status_code=status.HTTP_201_CREATED)
def create_tahmin(
    payload: TahminCreateIn,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    makine = db.get(Makine, payload.makine_id)
    if makine is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Makine bulunamadi")

    result = ml_model.predict(payload.sensor.model_dump())

    if not result["risk_uyarisi"]:
        return {
            "risk_uyarisi": False,
            "risk_orani": result["risk_orani"],
            "mesaj": "Risk esiginin altinda, kayit olusturulmadi",
        }

    ariza_parca = db.query(ArizaParca).filter(ArizaParca.ariza_tipi == result["ariza_tipi"]).first()
    katsayi = stok_katsayisi(ariza_parca.stok if ariza_parca else None)
    oncelik = compute_oncelik(result["risk_orani"], makine.kritiklik, katsayi)

    tahmin = Tahmin(
        makine_id=makine.id,
        risk_orani=result["risk_orani"],
        ariza_tipi=result["ariza_tipi"],
        gerekce=result["gerekce"],
        oncelik=oncelik,
        durum=TahminDurum.bekliyor,
    )
    db.add(tahmin)
    db.commit()
    db.refresh(tahmin)

    return _to_out(tahmin)


@router.get("", response_model=list[TahminOut])
def list_tahminler(
    durum: TahminDurum | None = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    query = db.query(Tahmin)
    if durum is not None:
        query = query.filter(Tahmin.durum == durum)
    tahminler = query.order_by(Tahmin.oncelik.desc(), Tahmin.risk_orani.desc()).all()
    return [_to_out(t) for t in tahminler]


@router.get("/{tahmin_id}", response_model=TahminOut)
def get_tahmin(
    tahmin_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    tahmin = db.get(Tahmin, tahmin_id)
    if tahmin is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tahmin bulunamadi")
    return _to_out(tahmin)
