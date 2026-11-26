from fastapi import FastAPI, APIRouter
from app.database.database import create_table, get_session
from contextlib import asynccontextmanager
from app.routes.user import route as user_route
from app.routes.developer import route as dev_route
from app.routes.ml_model import route as ml_router

from exception import (PredictionNotFound, prediction_not_found)
from exception import (DeveloperNotFound, developer_not_found)
from exception import (ModelNotFound, model_not_found)
from exception import (UnauthorizedAccess, unauthorized_access_handler)

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_table()
    yield


app = FastAPI(
    title="Ml-api",
    description="creating ml api",
    lifespan=lifespan
)

app.include_router(user_route)
app.include_router(dev_route)
app.include_router(ml_router)

app.add_exception_handler(PredictionNotFound, prediction_not_found)
app.add_exception_handler(DeveloperNotFound, developer_not_found)
app.add_exception_handler(ModelNotFound, model_not_found)
app.add_exception_handler(UnauthorizedAccess, unauthorized_access_handler)

@app.get("/")
def root():
    return {
        "message": "Wellcome"
    }