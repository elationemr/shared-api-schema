from typing import Any

from el8.ext.fastapi import default


def pytest_sessionstart(session: Any) -> None:
    """
    Called after the Session object has been created and
    before performing collection and entering the run test loop.
    """

    # Disabling the local dev auth token generation for unit-tests
    def return_empty_token(*args, **kwargs):  # type: ignore
        return None

    default.try_get_local_dev_auth_token = return_empty_token
