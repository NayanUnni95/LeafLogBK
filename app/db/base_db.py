from datetime import datetime

from sqlalchemy import TIMESTAMP, Column
from sqlmodel import SQLModel, Field, Relationship

from app.util.date_util import DateUtil
from app.util.util import IDGenerator

class CustomBaseModel(SQLModel):
    id: str = Field(primary_key=True, nullable=False, index=True, max_length=36,
                    default_factory=IDGenerator.generate_unique_id)


class BaseCreatorModel(CustomBaseModel):
    created_by: str = Field(nullable=False, max_length=36, foreign_key="user.id")
    created_at: datetime = Field(
        sa_column=Column(TIMESTAMP(timezone=True), nullable=False, default=DateUtil.get_current_time)
    )
    creator = Relationship(sa_relationship_kwargs={"primaryjoin": "User.id==BaseCreatorModel.created_by"})

    def set_audit_fields(self, user_id: str):
        self.created_by = user_id
        self.created_at = DateUtil.get_current_time()


class BaseUpdaterModel(BaseCreatorModel):
    updated_by: str = Field(nullable=False, max_length=36, foreign_key="user.id")
    updated_at: datetime = Field(
        sa_column=Column(TIMESTAMP(timezone=True), nullable=False, default=DateUtil.get_current_time)
    )
    updater = Relationship(sa_relationship_kwargs={"primaryjoin": "User.id==BaseCreatorModel.created_by"})

    def set_audit_fields(self, user_id: str):
        if not self.created_at:
            self.created_at = DateUtil.get_current_time()
        if not self.created_by:
            self.created_by = user_id
        self.updated_by = user_id
        self.updated_at = DateUtil.get_current_time()