FROM --platform=linux/x86_64 public.ecr.aws/docker/library/python:3.9.16-slim AS base

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1 \
    PYSETUP_PATH="/opt/pysetup" \
    VENV_PATH="/opt/pysetup/.venv"

ENV PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"

FROM base as build

RUN apt-get update && \
    apt-get install --no-install-recommends -y curl && \
    curl -sSL https://install.python-poetry.org | python -

WORKDIR $PYSETUP_PATH
COPY poetry.lock pyproject.toml ./
RUN poetry install --only main --no-ansi --no-root

FROM base as production

COPY --from=build $VENV_PATH $VENV_PATH

RUN chmod +x ${VENV_PATH}/bin/activate && ${VENV_PATH}/bin/activate

COPY src src

EXPOSE 80

ENTRYPOINT ["python", "src/main.py"]
