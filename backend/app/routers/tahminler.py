from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import ml_model
from app.database import get_db
from app.deps import get_current_user
from app.models import ArizaParca, IsEmri, IsEmriDurum, Makine, Tahmin, TahminDurum, User
from app.priority import compute_oncelik, stok_katsayisi
from app.schemas import IsEmriOut, TahminCreateIn, TahminOut

router = APIRouter(prefix="/tahminler", tags=["tahminler"])


def _to_out(tahmin: Tahmin, db: Session | None = None) -> TahminOut:
    onerilen_aksiyon = parca_kodu = parca_adi = None
    stok_adet = None
    if db is not None:
        ariza_parca = db.query(ArizaParca).filter(ArizaParca.ariza_tipi == tahmin.ariza_tipi).first()
        if ariza_parca is not None:
            onerilen_aksiyon = ariza_parca.onerilen_aksiyon
            parca_kodu = ariza_parca.parca_kodu
            if ariza_parca.stok is not None:
                parca_adi = ariza_parca.stok.ad
                stok_adet = ariza_parca.stok.adet

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
        karar_veren_user_id=tahmin.karar_veren_user_id,
        karar_tarihi=tahmin.karar_tarihi,
        onerilen_aksiyon=onerilen_aksiyon,
        parca_kodu=parca_kodu,
        parca_adi=parca_adi,
        stok_adet=stok_adet,
    )


def _get_pending_tahmin(tahmin_id: int, db: Session) -> Tahmin:
    tahmin = db.get(Tahmin, tahmin_id)
    if tahmin is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tahmin bulunamadi")
    if tahmin.durum != TahminDurum.bekliyor:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Bu tahmin zaten karara baglanmis (durum: {tahmin.durum.value})",
        )
    return tahmin


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
    return _to_out(tahmin, db)


@router.post("/{tahmin_id}/onayla", response_model=IsEmriOut)
def onayla(
    tahmin_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    tahmin = _get_pending_tahmin(tahmin_id, db)

    ariza_parca = db.query(ArizaParca).filter(ArizaParca.ariza_tipi == tahmin.ariza_tipi).first()
    if ariza_parca is None:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"{tahmin.ariza_tipi.value} icin tanimli bir parca/aksiyon eslemesi yok",
        )

    now = datetime.now(timezone.utc)
    tahmin.durum = TahminDurum.onaylandi
    tahmin.karar_veren_user_id = current_user.id
    tahmin.karar_tarihi = now

    is_emri = IsEmri(
        tahmin_id=tahmin.id,
        makine_id=tahmin.makine_id,
        aksiyon=ariza_parca.onerilen_aksiyon,
        parca_kodu=ariza_parca.parca_kodu,
        oncelik=tahmin.oncelik,
        durum=IsEmriDurum.bekliyor,
        onaylayan_user_id=current_user.id,
    )
    db.add(is_emri)
    db.commit()
    db.refresh(is_emri)

    return IsEmriOut(
        id=is_emri.id,
        tahmin_id=is_emri.tahmin_id,
        makine_id=is_emri.makine_id,
        makine_kodu=tahmin.makine.makine_kodu,
        aksiyon=is_emri.aksiyon,
        parca_kodu=is_emri.parca_kodu,
        oncelik=is_emri.oncelik,
        durum=is_emri.durum,
        onaylayan_user_id=is_emri.onaylayan_user_id,
        created_at=is_emri.created_at,
    )


@router.post("/{tahmin_id}/reddet", response_model=TahminOut)
def reddet(
    tahmin_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    tahmin = _get_pending_tahmin(tahmin_id, db)

    tahmin.durum = TahminDurum.reddedildi
    tahmin.karar_veren_user_id = current_user.id
    tahmin.karar_tarihi = datetime.now(timezone.utc)
    db.commit()
    db.refresh(tahmin)

    return _to_out(tahmin, db)
