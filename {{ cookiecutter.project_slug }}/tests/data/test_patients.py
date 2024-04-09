from typing import Generator

import pytest

from app.data.patients import (
    PatientNotFoundError,
    PatientRepository,
    patients_by_hippospace,
)
from app.models.patient.models import PatientDetails


@pytest.fixture(autouse=True)
def mock_patients() -> Generator:
    global patients_by_hippospace
    old_patients = patients_by_hippospace
    patients_by_hippospace = old_patients.copy()
    yield patients_by_hippospace
    patients_by_hippospace = old_patients


@pytest.fixture
def sut() -> PatientRepository:
    return PatientRepository("fake-hippospace")


def test_get_all(sut: PatientRepository) -> None:
    result = sut.get_all()
    assert len(result) == len(patients_by_hippospace["fake-hippospace"])
    assert result == patients_by_hippospace["fake-hippospace"]


def test_get_by_id(sut: PatientRepository) -> None:
    result = sut.get_by_id("wanda")
    assert result is not None
    assert result.name == "Wanda"


def test_get_by_id_raises_when_not_found(sut: PatientRepository) -> None:
    with pytest.raises(PatientNotFoundError):
        sut.get_by_id("non-existent")


def test_add_patient(sut: PatientRepository) -> None:
    with pytest.raises(PatientNotFoundError):
        sut.get_by_id("fake-patient")

    sut.add_patient(
        PatientDetails(
            id="fake-patient", name="Fake", sex="T", age=99, city="Neverland"
        )
    )

    result = sut.get_by_id("fake-patient")
    assert result is not None
    assert result.name == "Fake"
    assert result.sex == "T"
    assert result.age == 99
    assert result.city == "Neverland"


def test_add_patient_adds_to_the_hippospace(sut: PatientRepository) -> None:
    sut.add_patient(
        PatientDetails(
            id="fake-patient", name="Fake", sex="T", age=99, city="Neverland"
        )
    )
    result = sut.get_by_id("fake-patient")
    assert result is not None

    sut_another_hippospace = PatientRepository("another-hippospace")
    with pytest.raises(PatientNotFoundError):
        sut_another_hippospace.get_by_id("fake-patient")
