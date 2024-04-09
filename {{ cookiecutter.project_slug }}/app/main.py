import os

from el8.ext.fastapi.auth import RequireAuthentication, unauthenticated
from el8.ext.fastapi.default import init_default
from fastapi import FastAPI, Response, Security
from fastapi.responses import RedirectResponse

from app.routers import health_routers, patient_routers
from app.utils import settings

if os.environ.get("DATADOG_ENABLED", False):
    from ddtrace import patch

    patch(fastapi=True)

app = FastAPI()
init_default(
    app,
    environment=settings.ENVIRONMENT,
    # These settings are only applicable to the local development environment.
    swagger_ui_dev_token_scopes=["test"],
    swagger_ui_dev_token_practice_ids=[],
)

# Require authentication for all endpoints except those marked @unauthenticated
app.router.dependencies.append(Security(RequireAuthentication()))


# Redirect to /docs by default
@unauthenticated(app.router)
@app.get("/", include_in_schema=False)
async def get_root() -> Response:
    return RedirectResponse("/docs")


app.include_router(health_routers.router, tags=["health"])
app.include_router(patient_routers.router)
