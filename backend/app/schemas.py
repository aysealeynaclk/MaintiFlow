from typing import Literal

from pydantic import BaseModel

from app.models import UserRole


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
