from typing import List

from app.models.patient.models import PatientDetails

fake_patients: List[PatientDetails] = [
    PatientDetails(id="fake-id-1", name="Fake1", sex="F", age=156, city="fake-city-1"),
    PatientDetails(id="fake-id-2", name="Fake2", sex="M", age=2, city="fake-city-2"),
]
