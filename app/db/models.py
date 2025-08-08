from datetime import datetime
from typing import  List

from sqlalchemy import Column, TIMESTAMP, JSON
from sqlmodel import Field, Relationship

from app.db.base_db import CustomBaseModel, BaseCreatorModel, BaseUpdaterModel
from app.util.date_util import DateUtil


class User(CustomBaseModel, table=True):
    __tablename__ = 'user'
    name: str = Field(nullable=True, max_length=100)
    password: str = Field(nullable=True, max_length=100)
    email: str = Field(nullable=False, max_length=200)
    role: str = Field(nullable=True, max_length=15)
    otp: int = Field(nullable=True, max_length=6)
    created_at: datetime = Field(
        sa_column=Column(TIMESTAMP(timezone=True), nullable=False, default=DateUtil.get_current_time))