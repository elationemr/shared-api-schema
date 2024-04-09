from fastapi import APIRouter, Depends, HTTPException, status

from app.data.patients import PatientNotFoundError
from app.models.error_response import ErrorResponse
from app.models.patient.models import PatientDetails
from app.models.patient.responses import PatientListResponse, PatientResponse
from app.services.patient_service import PatientService

router = APIRouter()


@router.get("/patients", response_model=PatientListResponse)
async def get_patient(
    patient_service: PatientService = Depends(),
) -> PatientListResponse:
    response = PatientListResponse(response=patient_service.get_patients())
    return response


@router.get(
    "/patients/{id}",
    responses={
        status.HTTP_404_NOT_FOUND: {"model": ErrorResponse},
        status.HTTP_200_OK: {"model": PatientDetails},
    },
)
async def get_patient_by_id(
    id: str, patient_service: PatientService = Depends()
) -> PatientResponse:
    try:
        patient = patient_service.get_patient_by_id(id)
    except PatientNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Patient not found"
        ) from e

    response = PatientResponse(response=patient)
    return response


@router.post("/patients")
async def create_patient(
    patient: PatientDetails, patient_service: PatientService = Depends()
) -> PatientResponse:
    response = PatientResponse(response=patient_service.create_patient(patient))
    return response
