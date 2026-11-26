from pydantic import EmailStr
from sqlalchemy import JSON
from sqlmodel import SQLModel, Field, Column, Relationship
from datetime import datetime, timezone
from enum import Enum

class StatusOptions(str, Enum):
    SUCCESS = "success"
    ERROR = "error"

class PredictionFeature(SQLModel): # It is the pydantic validation for Prediction feature
    pass # I am not intialize yet, wait for model creation, after model creation then I will create feild for it. bcz at that I have a clear idea what kind of feild is required ?

class PredictionLogValidation(SQLModel):
    model_id: int
    features: PredictionFeature
    predicted_output: str
    status: StatusOptions
    latency: float

class PredictionLogResponse(SQLModel):
    log_id: int 
    model_id: int
    features: PredictionFeature
    predicted_output: str
    status: StatusOptions
    latency: float
    predicted_at: datetime


class DeveloperInfoValidation(SQLModel):
    name: str
    phone_no: str = Field(min_length=10, max_length=10)
    position: str
    email: EmailStr


# Ml model validation models -
class ModelRegistration(SQLModel): #represents a trained model version / experiment run
    model_name: str
    Version: str
    used_algorithm: str
    evaluation_metrics: dict[str, float]
    active_flag: bool # Is this version currently serving ?

class ModelResponse(SQLModel): #represents a trained model version / experiment run
    model_id: int
    developer_id: int
    model_name: str
    Version: str
    used_algorithm: str
    evaluation_metrics: dict 
    active_flag: bool # Is this version currently serving ?
    created_date: datetime 
    updated_at: datetime

class ModelUpdateValidation(SQLModel): #represents a trained model version / experiment run
    model_id: int
    model_name: str| None = None
    Version: str | None = None
    used_algorithm: str | None = None
    evaluation_metrics: dict | None = None
    active_flag: bool | None = None# Is this version currently serving ?

