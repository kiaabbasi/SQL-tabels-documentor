from pydantic import BaseModel, ConfigDict
from typing import Optional

class UmStructureOut(BaseModel):
    StructID2: int
    StructTitle: str
    model_config = ConfigDict(from_attributes=True)
