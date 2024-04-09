from app.services.health_service import HealthService


def test_get_ready() -> None:
    sut = HealthService()
    resp = sut.get_ready()
    assert resp is True


def test_get_live() -> None:
    sut = HealthService()
    resp = sut.get_live()
    assert resp is True
