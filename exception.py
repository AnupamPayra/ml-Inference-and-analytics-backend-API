from fastapi import Request
from sqlmodel import SQLModel
from fastapi.responses import JSONResponse


class PredictionNotFound(Exception):
    def __init__(self, id):
        self.id = id

def prediction_not_found(request: Request, exc : PredictionNotFound):
    return JSONResponse(
        status_code=404,
        content={
            "message": "Check prediction id before entered",
            "id": exc.id
        }
    )
