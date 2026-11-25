from sqlmodel import SQLModel, Field, Relationship, Column
from sqlalchemy import JSON
from app.models.models import StatusOptions, PredictionFeature
from datetime import datetime

class ModelRun(SQLModel, table=True): #represents a trained model version / experiment run
    model_id: int | None = Field(default=None, primary_key=True)
    model_name: str
    Version: str
    used_algorithm: str
    evaluation_metrics: str
    active_flag: bool # Is this version currently serving ?
    created_date: datetime = Field(default_factory=datetime.now)
    prediction_logs: list["PredictionLog"] = Relationship(back_populates="model")


class PredictionLog:
    log_id: int | None = Field(default=None, primary_key=True)
    model_id: int = Field(foreign_key="modelrun.model_id")
    features: PredictionFeature = Field(sa_column=Column(JSON))
    predicted_output: str
    status: StatusOptions = Field(default=StatusOptions.SUCCESS)
    latency: float
    pridicted_at: datetime = Field(default_factory=datetime.now)
    model: "ModelRun" = Relationship(back_populates="prediction_logs")