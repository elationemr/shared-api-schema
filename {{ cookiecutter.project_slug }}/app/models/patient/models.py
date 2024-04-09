from typing import Optional

from pydantic import BaseModel


class PatientDetails(BaseModel):
    id: Optional[str]
    name: str
    sex: str
    age: int
    city: str
