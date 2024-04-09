import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_create_new_patient(http_client: AsyncClient) -> None:
    # Create a new patient
    new_patient = {
        "id": "new_patient",
        "name": "New Patient",
        "sex": "M",
        "age": 99,
        "city": "Nonexistent",
    }
    response = await http_client.post("/patients", json=new_patient)
    assert response.status_code == 200
    response_data = response.json().get("response")
    assert response_data == new_patient

    # Get the new patient by id
    response = await http_client.get(f"/patients/{new_patient['id']}")
    assert response.status_code == 200
    response_data = response.json().get("response")
    assert response_data == new_patient

    # Get the list of patients and ensure the new patient is present
    response = await http_client.get("/patients")
    assert response.status_code == 200
    response_data = response.json().get("response")
    assert isinstance(response_data, list)
    assert new_patient in response_data
