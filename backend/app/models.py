import enum
from datetime import datetime

from sqlalchemy import (
    JSON,
    CheckConstraint,
    DateTime,
    Enum,
    Float,
    ForeignKey,
    Integer,
    String,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class UserRole(str, enum.Enum):
    admin = "admin"
    user = "user"


class UserStatus(str, enum.Enum):
    active = "active"
    inactive = "inactive"


class FailureType(str, enum.Enum):
    TWF = "TWF"
    HDF = "HDF"
    PWF = "PWF"
    OSF = "OSF"


class TahminDurum(str, enum.Enum):
    bekliyor = "bekliyor"
    onaylandi = "onaylandi"
    reddedildi = "reddedildi"


class IsEmriDurum(str, enum.Enum):
    bekliyor = "bekliyor"
    tamamlandi = "tamamlandi"
    iptal = "iptal"


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, index=True)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[UserRole] = mapped_column(Enum(UserRole), nullable=False, default=UserRole.user)
    status: Mapped[UserStatus] = mapped_column(Enum(UserStatus), nullable=False, default=UserStatus.active)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class Makine(Base):
    __tablename__ = "makineler"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    makine_kodu: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, index=True)
    ad: Mapped[str] = mapped_column(String(100), nullable=False)
    tip: Mapped[str] = mapped_column(String(10), nullable=False)
    kritiklik: Mapped[int] = mapped_column(Integer, nullable=False)

    __table_args__ = (CheckConstraint("kritiklik BETWEEN 1 AND 5", name="ck_makine_kritiklik_range"),)

    tahminler: Mapped[list["Tahmin"]] = relationship(back_populates="makine")


class Stok(Base):
    __tablename__ = "stok"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    parca_kodu: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, index=True)
    ad: Mapped[str] = mapped_column(String(100), nullable=False)
    adet: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    tedarik_gun: Mapped[int] = mapped_column(Integer, nullable=False)


class ArizaParca(Base):
    __tablename__ = "ariza_parca"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    ariza_tipi: Mapped[FailureType] = mapped_column(Enum(FailureType), nullable=False, index=True)
    parca_kodu: Mapped[str] = mapped_column(String(50), ForeignKey("stok.parca_kodu"), nullable=False)
    onerilen_aksiyon: Mapped[str] = mapped_column(String(255), nullable=False)

    stok: Mapped["Stok"] = relationship()


class Tahmin(Base):
    __tablename__ = "tahminler"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    makine_id: Mapped[int] = mapped_column(Integer, ForeignKey("makineler.id"), nullable=False, index=True)
    risk_orani: Mapped[float] = mapped_column(Float, nullable=False)
    ariza_tipi: Mapped[FailureType] = mapped_column(Enum(FailureType), nullable=False)
    gerekce: Mapped[dict] = mapped_column(JSON, nullable=False)
    oncelik: Mapped[int] = mapped_column(Integer, nullable=False)
    durum: Mapped[TahminDurum] = mapped_column(Enum(TahminDurum), nullable=False, default=TahminDurum.bekliyor)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    karar_veren_user_id: Mapped[int | None] = mapped_column(Integer, ForeignKey("users.id"), nullable=True)
    karar_tarihi: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    __table_args__ = (CheckConstraint("oncelik BETWEEN 1 AND 5", name="ck_tahmin_oncelik_range"),)

    makine: Mapped["Makine"] = relationship(back_populates="tahminler")
    is_emri: Mapped["IsEmri"] = relationship(back_populates="tahmin", uselist=False)


class IsEmri(Base):
    __tablename__ = "is_emirleri"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    tahmin_id: Mapped[int] = mapped_column(Integer, ForeignKey("tahminler.id"), unique=True, nullable=False)
    makine_id: Mapped[int] = mapped_column(Integer, ForeignKey("makineler.id"), nullable=False, index=True)
    aksiyon: Mapped[str] = mapped_column(String(255), nullable=False)
    parca_kodu: Mapped[str] = mapped_column(String(50), ForeignKey("stok.parca_kodu"), nullable=False)
    oncelik: Mapped[int] = mapped_column(Integer, nullable=False)
    durum: Mapped[IsEmriDurum] = mapped_column(Enum(IsEmriDurum), nullable=False, default=IsEmriDurum.bekliyor)
    onaylayan_user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    __table_args__ = (CheckConstraint("oncelik BETWEEN 1 AND 5", name="ck_is_emri_oncelik_range"),)

    tahmin: Mapped["Tahmin"] = relationship(back_populates="is_emri")
