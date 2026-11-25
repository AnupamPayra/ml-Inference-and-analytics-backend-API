from fastapi import Depends, FastAPI, APIRouter
from sqlmodel import Session
from app.database.database import get_session
from app.models.models import PredictionLogResponse
from app.models.scheema import PredictionLog

from exception import PredictionNotFound

route = APIRouter(prefix="/dev", tags=["Developer management"])


@route.get("/prediction/{id}", response_model=PredictionLogResponse)
def prediction_info(
    id: int,
    session: Session = Depends(get_session)
):
    predicted_data = session.get(PredictionLog, id)
    if not predicted_data:
        raise PredictionNotFound
    
    return predicted_data