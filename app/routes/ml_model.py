from datetime import date, datetime, timezone

from sqlmodel import SQLModel, Field, Session
from fastapi import Depends, APIRouter
from app.database.database import get_session
from app.models.models import ModelRegistration, ModelResponse, ModelUpdateValidation
from app.models.scheema import DeveloperInfo, ModelRun
from exception import DeveloperNotFound, ModelNotFound, UnauthorizedAccess


route = APIRouter(prefix="/ml_models", tags=["ML-model management"])


@route.post("/new/{developer_id}", response_model=ModelResponse)
def model_registration(
    developer_id: int,
    data: ModelRegistration,
    session: Session = Depends(get_session)
):
        developer_data = session.get(DeveloperInfo, developer_id)
        if not developer_data:
                raise DeveloperNotFound(id=developer_id)
        model_data = ModelRun(**data.model_dump())
        model_data.developer_id=developer_id
        session.add(model_data)
        session.commit()
        session.refresh(model_data)

        return model_data


@route.patch("/update/{developer_id}", response_model=ModelResponse)
def model_updation(
       developer_id: int,
        data: ModelUpdateValidation,
        session: Session = Depends(get_session)
):
        developer_data = session.get(DeveloperInfo, developer_id)
        if not developer_data:
            raise DeveloperNotFound(id=developer_id)

        updated_model_data = data.model_dump(exclude_unset=True)
        model_data = session.get(ModelRun, data.model_id)
        if not model_data:
               raise ModelNotFound(id=data.model_id)

        model_owner = model_data.developer.name
        if developer_id != model_data.developer_id:
               raise UnauthorizedAccess(id=developer_id, model_name=model_data.model_name, developer_name=model_owner)
        for key, value in updated_model_data.items():
               setattr(model_data, key, value)


        
        model_data.updated_at = datetime.now(timezone.utc)
        session.add(model_data)
        session.commit()
        session.refresh(model_data)
        return model_data
