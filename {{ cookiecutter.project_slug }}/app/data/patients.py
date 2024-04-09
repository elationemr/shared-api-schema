from collections import defaultdict

from fastapi import Depends

from app.models.patient.models import PatientDetails
from app.utils.hippospace import get_current_hippospace

patients_by_hippospace: dict[str, list[PatientDetails]] = defaultdict(
    lambda: [
        PatientDetails(id="wanda", name="Wanda", sex="F", age=43, city="Seattle"),
        PatientDetails(id="storm", name="Storm", sex="F", age=34, city="New York"),
        PatientDetails(id="hulk", name="Hulk", sex="M", age=21, city="Houston"),
        PatientDetails(id="thanos", name="Thanos", sex="M", age=49, city="Los Angeles"),
    ]
)


class PatientNotFoundError(Exception):
    pass


class PatientRepository:
    def __init__(self, hippospace: str = Depends(get_current_hippospace)) -> None:
        self.hippospace = hippospace

    def get_all(self) -> list[PatientDetails]:
        """
        Get a list of all stored patient records
        """
        return patients_by_hippospace[self.hippospace].copy()

    def get_by_id(self, id: str) -> PatientDetails:
        """
        Get a patient record by its ID. Raises PatientNotFoundError if
        the patient is not found.

        Returns:
            The patient record or None
        """
        try:
            result = next(
                p for p in patients_by_hippospace[self.hippospace] if p.id == id
            )
        except StopIteration as e:
            raise PatientNotFoundError() from e

        return result

    def add_patient(self, patient: PatientDetails) -> None:
        """
        Add a new patient record to the list
        """
        patients_by_hippospace[self.hippospace].append(patient.model_copy())
