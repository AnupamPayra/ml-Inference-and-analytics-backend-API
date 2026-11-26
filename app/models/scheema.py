from pydantic import EmailStr
from sqlmodel import SQLModel, Field, Relationship, Column
from sqlalchemy import JSON
from app.models.models import StatusOptions, PredictionFeature
from datetime import datetime, timezone

class ModelRun(SQLModel, table=True): #represents a trained model version / experiment run
    model_id: int | None = Field(default=None, primary_key=True)
    developer_id: int = Field(foreign_key="developerinfo.developer_id")
    model_name: str
    Version: str
    used_algorithm: str
    evaluation_metrics: dict = Field(default_factory=dict, sa_column=Column(JSON))
    active_flag: bool # Is this version currently serving ?
    created_date: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    prediction_logs: list["PredictionLog"] = Relationship(back_populates="model")
    developer: "DeveloperInfo" = Relationship(back_populates="models")


class PredictionLog(SQLModel, table=True):
    log_id: int | None = Field(default=None, primary_key=True)
    model_id: int = Field(foreign_key="modelrun.model_id")
    features: PredictionFeature = Field(sa_column=Column(JSON))
    predicted_output: str
    status: StatusOptions = Field(default=StatusOptions.SUCCESS)
    latency: float
    predicted_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    model: "ModelRun" = Relationship(back_populates="prediction_logs")

class DeveloperInfo(SQLModel, table=True):
    developer_id: int | None = Field(default=None, primary_key=True)
    name: str
    phone_no: str = Field(min_length=10, max_length=10)
    email: EmailStr = Field(unique=True)
    position: str
    models: list["ModelRun"] = Relationship(back_populates="developer")