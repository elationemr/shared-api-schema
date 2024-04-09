from typing import Any
from unittest.mock import create_autospec

import pytest

from app.data.patients import PatientRepository
from app.services.patient_service import PatientService
from tests.utils.fake_data import fake_patients


@pytest.fixture
def mock_patient_repository() -> None:
    mock = create_autospec(PatientRepository)
    return mock


def test_get_patients(mock_patient_repository: Any) -> None:
    mock_patient_repository.get_all.return_value = fake_patients
    sut = PatientService(mock_patient_repository)
    result = sut.get_patients()
    assert result == fake_patients


def test_get_patient_by_id(mock_patient_repository: Any) -> None:
    mock_patient_repository.get_by_id.return_value = fake_patients[1]
    sut = PatientService(mock_patient_repository)
    result = sut.get_patient_by_id("fake-id")
    assert result == fake_patients[1]
    mock_patient_repository.get_by_id.assert_called_with("fake-id")


def test_create_patient(mock_patient_repository: Any) -> None:
    sut = PatientService(mock_patient_repository)
    sut.create_patient(fake_patients[0])
    mock_patient_repository.add_patient.assert_called_with(fake_patients[0])


def test_create_patient_with_generated_id(mock_patient_repository: Any) -> None:
    input = fake_patients[1].model_copy()
    input.id = None
    sut = PatientService(mock_patient_repository)
    sut.create_patient(input)
    expected = input.model_copy()
    expected.id = "fake2"
    mock_patient_repository.add_patient.assert_called_with(expected)
