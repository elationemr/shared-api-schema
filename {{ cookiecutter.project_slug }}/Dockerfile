FROM 570488747013.dkr.ecr.us-west-2.amazonaws.com/elation/service/python:3.10-build AS python-deps

# Install python dependencies in ~/.venv
RUN poetry config virtualenvs.create true \
  && poetry config virtualenvs.in-project true

COPY pyproject.toml .
COPY poetry.lock .
RUN --mount=type=secret,id=CODEARTIFACT_AUTH_TOKEN \
  POETRY_HTTP_BASIC_EL8_PASSWORD=$(cat /run/secrets/CODEARTIFACT_AUTH_TOKEN) \
  poetry install --only main

# A stage for unit-tests
FROM python-deps as tests

COPY . .

# Install dev dependencies
RUN --mount=type=secret,id=CODEARTIFACT_AUTH_TOKEN \
  POETRY_HTTP_BASIC_EL8_PASSWORD=$(cat /run/secrets/CODEARTIFACT_AUTH_TOKEN) \
  poetry install

# Running the rest under non-privileged user
USER app

# Run unit-tests, linting, and typing
RUN poetry run pytest tests --cov app --cov-report xml --cov-report term --cov-fail-under=85 && \
  poetry run flake8 . && \
  poetry run mypy . && \
  poetry run isort --check-only .

# Prepare the runtime image
FROM 570488747013.dkr.ecr.us-west-2.amazonaws.com/elation/service/python:3.10 as runtime

# Force building the "tests" stage and keep the coverage data for future use
COPY --from=tests /home/app/coverage.xml .

# Copy virtual env from python-deps stage
COPY --from=python-deps /home/app/.venv /home/app/.venv
ENV PATH="/home/app/.venv/bin:$PATH"

# Create and switch to a new user
USER app

# Install application into container
COPY ./app ./app

# Run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
