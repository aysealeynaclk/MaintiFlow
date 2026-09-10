from datetime import datetime
from typing import Literal

from pydantic import BaseModel

from app.models import IsEmriDurum, TahminDurum, UserRole, UserStatus


class LoginRequest(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserOut(BaseModel):
    id: int
    username: str
    role: UserRole
    status: UserStatus

    class Config:
        from_attributes = True


class SensorReadingIn(BaseModel):
    air_temperature: float
    process_temperature: float
    rotational_speed: float
    torque: float
    tool_wear: float
    tip: Literal["L", "M", "H"]


class ReasonOut(BaseModel):
    feature: str
    value: float
    shap_contribution: float


class PredictionOut(BaseModel):
    risk_orani: float
    ariza_tipi: str
    risk_uyarisi: bool
    gerekce: list[ReasonOut]


class TahminCreateIn(BaseModel):
    makine_id: int
    sensor: SensorReadingIn


class TahminOut(BaseModel):
    id: int
    makine_id: int
    makine_kodu: str
    risk_orani: float
    ariza_tipi: str
    gerekce: list[ReasonOut]
    oncelik: int
    durum: TahminDurum
    created_at: datetime
    karar_veren_user_id: int | None = None
    karar_tarihi: datetime | None = None
    onerilen_aksiyon: str | None = None
    parca_kodu: str | None = None
    parca_adi: str | None = None
    stok_adet: int | None = None


class TahminListResponse(BaseModel):
    items: list[TahminOut]
    total: int
    page: int
    page_size: int


class IsEmriOut(BaseModel):
    id: int
    tahmin_id: int
    makine_id: int
    makine_kodu: str
    aksiyon: str
    parca_kodu: str
    oncelik: int
    durum: IsEmriDurum
    onaylayan_user_id: int
    created_at: datetime


class MakineOut(BaseModel):
    id: int
    makine_kodu: str
    ad: str
    tip: str
    kritiklik: int

    class Config:
        from_attributes = True


class MakineUpdateIn(BaseModel):
    kritiklik: int


class StokOut(BaseModel):
    id: int
    parca_kodu: str
    ad: str
    adet: int
    tedarik_gun: int

    class Config:
        from_attributes = True


class StokUpdateIn(BaseModel):
    adet: int | None = None
    tedarik_gun: int | None = None


class LogOut(BaseModel):
    id: int
    makine_kodu: str
    risk_orani: float
    ariza_tipi: str
    oncelik: int
    durum: TahminDurum
    created_at: datetime
    karar_veren_username: str | None = None
    karar_tarihi: datetime | None = None


class UserCreateIn(BaseModel):
    username: str
    password: str
    role: UserRole = UserRole.user


class StatusUpdateIn(BaseModel):
    status: UserStatus


class PasswordResetOut(BaseModel):
    yeni_sifre: str


class MeUpdateIn(BaseModel):
    current_password: str
    new_username: str | None = None
    new_password: str | None = None
