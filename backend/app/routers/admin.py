from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.deps import require_admin
from app.models import Makine, Stok, Tahmin, User, UserStatus
from app.schemas import (
    LogOut,
    MakineOut,
    MakineUpdateIn,
    PasswordUpdateIn,
    StatusUpdateIn,
    StokOut,
    StokUpdateIn,
    UserCreateIn,
    UserOut,
)
from app.security import hash_password

router = APIRouter(prefix="/admin", tags=["admin"], dependencies=[Depends(require_admin)])


# --- Makine yonetimi ---


@router.get("/makineler", response_model=list[MakineOut])
def list_makineler(db: Session = Depends(get_db)):
    return db.query(Makine).order_by(Makine.makine_kodu).all()


@router.patch("/makineler/{makine_id}", response_model=MakineOut)
def update_makine(makine_id: int, payload: MakineUpdateIn, db: Session = Depends(get_db)):
    makine = db.get(Makine, makine_id)
    if makine is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Makine bulunamadi")
    if not (1 <= payload.kritiklik <= 5):
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Kritiklik 1-5 arasinda olmali")
    makine.kritiklik = payload.kritiklik
    db.commit()
    db.refresh(makine)
    return makine


# --- Stok yonetimi ---


@router.get("/stok", response_model=list[StokOut])
def list_stok(db: Session = Depends(get_db)):
    return db.query(Stok).order_by(Stok.parca_kodu).all()


@router.patch("/stok/{stok_id}", response_model=StokOut)
def update_stok(stok_id: int, payload: StokUpdateIn, db: Session = Depends(get_db)):
    stok = db.get(Stok, stok_id)
    if stok is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Stok kaydi bulunamadi")
    if payload.adet is not None:
        stok.adet = payload.adet
    if payload.tedarik_gun is not None:
        stok.tedarik_gun = payload.tedarik_gun
    db.commit()
    db.refresh(stok)
    return stok


# --- Log goruntuleme ---


@router.get("/loglar", response_model=list[LogOut])
def list_loglar(db: Session = Depends(get_db)):
    tahminler = db.query(Tahmin).order_by(Tahmin.created_at.desc()).all()
    out = []
    for t in tahminler:
        karar_veren = db.get(User, t.karar_veren_user_id) if t.karar_veren_user_id else None
        out.append(
            LogOut(
                id=t.id,
                makine_kodu=t.makine.makine_kodu,
                risk_orani=t.risk_orani,
                ariza_tipi=t.ariza_tipi.value,
                oncelik=t.oncelik,
                durum=t.durum,
                created_at=t.created_at,
                karar_veren_username=karar_veren.username if karar_veren else None,
                karar_tarihi=t.karar_tarihi,
            )
        )
    return out


# --- Kullanici yonetimi ---


@router.get("/kullanicilar", response_model=list[UserOut])
def list_kullanicilar(db: Session = Depends(get_db)):
    return db.query(User).order_by(User.username).all()


@router.post("/kullanicilar", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def create_kullanici(payload: UserCreateIn, db: Session = Depends(get_db)):
    if db.query(User).filter(User.username == payload.username).first() is not None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Bu kullanici adi zaten kullaniliyor")

    user = User(
        username=payload.username,
        password_hash=hash_password(payload.password),
        role=payload.role,
        status=UserStatus.active,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.patch("/kullanicilar/{user_id}/sifre", response_model=UserOut)
def update_sifre(user_id: int, payload: PasswordUpdateIn, db: Session = Depends(get_db)):
    user = db.get(User, user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Kullanici bulunamadi")
    user.password_hash = hash_password(payload.password)
    db.commit()
    db.refresh(user)
    return user


@router.patch("/kullanicilar/{user_id}/durum", response_model=UserOut)
def update_durum(
    user_id: int,
    payload: StatusUpdateIn,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    user = db.get(User, user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Kullanici bulunamadi")
    if user.id == current_user.id and payload.status == UserStatus.inactive:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Kendi hesabinizi pasife alamazsiniz")
    user.status = payload.status
    db.commit()
    db.refresh(user)
    return user
