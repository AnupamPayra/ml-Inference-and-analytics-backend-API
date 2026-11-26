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

class ModelNotFound(Exception):
    def __init__(self, id):
        self.id = id

def model_not_found(request: Request, exc : ModelNotFound):
    return JSONResponse(
        status_code=404,
        content={
            "message": "The model number isn't valid",
            "id": f"Check your model id {exc.id} again"
        }
    )


class DeveloperNotFound(Exception):
    def __init__(self, id):
        self.id = id

def developer_not_found(request: Request, exc : DeveloperNotFound):
    return JSONResponse(
        status_code=404,
        content={
            "message": "You are not authorized to check sensitive infoemation",
            "id": f"Check your id {exc.id} again"
        }
    )

class UnauthorizedAccess(Exception):
    def __init__(self, id, developer_name, model_name):
        self.id = id
        self.developer_name = developer_name
        self.model_name = model_name

def unauthorized_access_handler(request: Request, exc : UnauthorizedAccess):
    return JSONResponse(
        status_code=403,
        content={
            "message": f"You are not authorized to Make any changes with the model {exc.model_name}",
            "id": f"Check your id {exc.id} again",
            "solution": f"this {exc.model_name} can be modified by {exc.developer_name}"
        }
    )
