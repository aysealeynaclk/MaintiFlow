from fastapi import APIRouter, Depends

from app import ml_model
from app.deps import get_current_user
from app.models import User
from app.schemas import PredictionOut, SensorReadingIn

router = APIRouter(prefix="/predictions", tags=["predictions"])


@router.post("/predict", response_model=PredictionOut)
def predict(sensor: SensorReadingIn, current_user: User = Depends(get_current_user)):
    result = ml_model.predict(sensor.model_dump())
    return result
