from sqlalchemy import JSON
from sqlmodel import SQLModel, Field, Column, Relationship
from datetime import datetime
from enum import Enum

class StatusOptions(str, Enum):
    SUCCESS = "success",
    ERROR = "error"

class PredictionFeature(SQLModel): # It is the pydantic validation for Prediction feature
    pass

class PredictionLogValidation(SQLModel):
    log_id: int | None 
    model_id: int
    features: PredictionFeature = Field(sa_column=Column(JSON))
    predicted_output: str
    status: StatusOptions | None = None
    latency: float

class PredictionLogResponse(SQLModel):
    log_id: int | None
    model_id: int
    features: PredictionFeature = Field(sa_column=Column(JSON))
    predicted_output: str
    status: StatusOptions | None = None
    latency: float
    pridicted_at: datetime