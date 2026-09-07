from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.deps import get_current_user
from app.models import IsEmri, IsEmriDurum, User
from app.schemas import IsEmriOut

router = APIRouter(prefix="/is-emirleri", tags=["is-emirleri"])


def _to_out(is_emri: IsEmri) -> IsEmriOut:
    return IsEmriOut(
        id=is_emri.id,
        tahmin_id=is_emri.tahmin_id,
        makine_id=is_emri.makine_id,
        makine_kodu=is_emri.tahmin.makine.makine_kodu,
        aksiyon=is_emri.aksiyon,
        parca_kodu=is_emri.parca_kodu,
        oncelik=is_emri.oncelik,
        durum=is_emri.durum,
        onaylayan_user_id=is_emri.onaylayan_user_id,
        created_at=is_emri.created_at,
    )


@router.get("", response_model=list[IsEmriOut])
def list_is_emirleri(
    durum: IsEmriDurum | None = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    query = db.query(IsEmri)
    if durum is not None:
        query = query.filter(IsEmri.durum == durum)
    is_emirleri = query.order_by(IsEmri.created_at.desc()).all()
    return [_to_out(i) for i in is_emirleri]
