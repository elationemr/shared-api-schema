class HealthException(Exception):
    def __init__(self, detail: str, *args: object) -> None:
        self._detail = detail
        super().__init__(*args)

    @property
    def detail(self) -> str:
        return self._detail


class HealthService:
    """
    Validates state of the service if it is ready to serve requests.
    """

    def get_live(self) -> bool:
        """
        Validate if the service is up and running. It may not be fully
        ready to serve requests yet. Always returns True.
        """
        return True

    def get_ready(self) -> bool:
        """
        Validate if the service is fully initialized and is ready to serve requests.
        Throws an exception if the service is not ready. Always returns True
        upon success.
        """
        # Add app initialization validation logic here and
        # only return True when the application is ready to serve
        # requests. If the application is not ready, raise a HealthException.
        return True
