from typing import List

from fastapi import Depends

from app.data.patients import PatientRepository
from app.models.patient.models import PatientDetails


class PatientService:
    patient_repository: PatientRepository

    def __init__(
        self,
        patient_repository: PatientRepository = Depends(),
    ) -> None:
        self.patient_repository = patient_repository

    def get_patients(self) -> List[PatientDetails]:
        """
        Get a list of all stored patient records
        """
        return self.patient_repository.get_all()

    def get_patient_by_id(self, id: str) -> PatientDetails:
        """
        Get a patient record by its ID. Raises PatientNotFoundError
        if the patient record does not exist.

        Returns:
            The patient record or None
        """
        return self.patient_repository.get_by_id(id)

    def create_patient(self, patient: PatientDetails) -> PatientDetails:
        """
        Create a new patient record. If the id is not provided it will
        be generated based on patient's name.

        Returns:
            The newly added patient record.
        """
        new_patient = patient.model_copy()
        if not new_patient.id:
            new_patient.id = new_patient.name.lower().replace(" ", "_")
        self.patient_repository.add_patient(new_patient)
        return new_patient
