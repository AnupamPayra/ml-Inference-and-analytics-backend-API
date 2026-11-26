from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlmodel import Session
from app.database.database import get_session
from app.models.models import PredictionLogValidation
from app.models.scheema import PredictionLog

route = APIRouter(prefix="/user", tags=["User management"])


@route.post("/prediction")
def make_prediction(
    data: PredictionLogValidation,
    session: Session = Depends(get_session)
    ):
    final_data = PredictionLog(**data.model_dump())
    session.add(final_data)
    session.commit()
    session.refresh(final_data)
    return JSONResponse(
        status_code=201,
        content={
            "message": "Your prediction is now under process - wait for few seconds "
        }
    )

