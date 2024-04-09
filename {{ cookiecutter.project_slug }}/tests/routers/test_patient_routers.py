from typing import Generator
from unittest.mock import MagicMock, create_autospec

import pytest
from fastapi.testclient import TestClient
from pydantic import TypeAdapter

from app.data.patients import PatientNotFoundError
from app.main import app
from app.models.patient.models import PatientDetails
from app.services.patient_service import PatientService
from tests.utils.fake_data import fake_patients


@pytest.fixture()
def mock_patient_service() -> Generator:
    patient_service = create_autospec(PatientService)
    app.dependency_overrides[PatientService] = lambda: patient_service
    yield patient_service
    del app.dependency_overrides[PatientService]


def test_get_patients(
    mock_patient_service: MagicMock, authenticated_test_client: TestClient
) -> None:
    mock_patient_service.get_patients.return_value = fake_patients
    response = authenticated_test_client.get("/patients")
    assert response.status_code == 200
    assert response.json() == {
        "response": TypeAdapter(list[PatientDetails]).dump_python(fake_patients)
    }


def test_get_patient_by_id(
    mock_patient_service: MagicMock, authenticated_test_client: TestClient
) -> None:
    mock_patient_service.get_patient_by_id.return_value = fake_patients[0]
    response = authenticated_test_client.get("/patients/fake-id")
    assert response.status_code == 200
    assert response.json() == {
        "response": TypeAdapter(PatientDetails).dump_python(fake_patients[0])
    }
    mock_patient_service.get_patient_by_id.assert_called_with("fake-id")


def test_get_patient_by_id_returns_404(
    mock_patient_service: MagicMock, authenticated_test_client: TestClient
) -> None:
    mock_patient_service.get_patient_by_id.side_effect = PatientNotFoundError()
    response = authenticated_test_client.get("/patients/fake-id")
    assert response.status_code == 404
    assert response.json() == {"detail": "Patient not found"}


def test_create_patient(
    mock_patient_service: MagicMock, authenticated_test_client: TestClient
) -> None:
    mock_patient_service.create_patient.return_value = fake_patients[1]
    response = authenticated_test_client.post(
        "/patients", json=fake_patients[1].model_dump()
    )
    assert response.status_code == 200
    assert response.json() == {
        "response": TypeAdapter(PatientDetails).dump_python(fake_patients[1])
    }
    mock_patient_service.create_patient.assert_called_with(fake_patients[1])
