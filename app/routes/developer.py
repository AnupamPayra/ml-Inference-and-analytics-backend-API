from operator import le

from fastapi import Depends, FastAPI, APIRouter, Query
from fastapi.responses import JSONResponse
from sqlmodel import select
from sqlmodel import Session
from app.database.database import get_session
from app.models.models import PredictionLogResponse, DeveloperInfoValidation
from app.models.scheema import PredictionLog, DeveloperInfo

from exception import PredictionNotFound
from exception import DeveloperNotFound

route = APIRouter(prefix="/dev", tags=["Developer management"])

@route.post("/login")
def new_developer(data: DeveloperInfoValidation, session: Session = Depends(get_session)):
    developer_data = DeveloperInfo(**data.model_dump())
    session.add(developer_data)
    session.commit()
    session.refresh(developer_data)
    return JSONResponse(
        status_code=201,
        content={
            "developer_id": developer_data.developer_id,
            "developer_name": developer_data.name,
            "email": developer_data.email,
            "phone": developer_data.phone_no,
            "position": developer_data.position
        }
    )

@route.get("/prediction/{id}", response_model=PredictionLogResponse)
def prediction_info(
    id: int,
    developer_id: int,
    session: Session = Depends(get_session)
):
    developer_data = session.get(DeveloperInfo, developer_id)
    if not developer_data:
        raise DeveloperNotFound(developer_id)
    
    predicted_data = session.get(PredictionLog, id)
    if not predicted_data:
        raise PredictionNotFound(id)
    
    return predicted_data

@route.get("/prediction_log/{developer_id}", response_model=list[PredictionLogResponse])
def get_all_prediction_detail(
    developer_id: int,
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=10, ge=1, le=20),
    session: Session = Depends(get_session)
):
    if not session.get(DeveloperInfo, developer_id):
        raise DeveloperNotFound(developer_id)
    
    query = select(PredictionLog)
    query = query.offset(skip).limit(limit)

    logs_data = session.exec(query).all()

    return logs_data