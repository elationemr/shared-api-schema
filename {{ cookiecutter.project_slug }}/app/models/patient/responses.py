from typing import List

from pydantic import BaseModel

from app.models.patient.models import PatientDetails


class PatientListResponse(BaseModel):
    response: List[PatientDetails]


class PatientResponse(BaseModel):
    response: PatientDetails
