from pydantic import BaseModel, ConfigDict

class PersonBasicOut(BaseModel):
    PersonID: int
    pfname: str
    plname: str
    fullname: str
    model_config = ConfigDict(from_attributes=True)