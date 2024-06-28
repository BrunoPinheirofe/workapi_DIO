from datetime import datetime
from typing import Annotated

from pydantic import UUID4, BaseModel, Field


class BaseSchemas(BaseModel):
    class Config:
        extra = "forbid"
        from_atributes = True


class OutMixin(BaseSchemas):
    id: Annotated[UUID4, Field(description="Indentificador")]
    create_at: Annotated[datetime, Field(description="Data de criação")]
