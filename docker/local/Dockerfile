FROM python:3.9-bullseye

WORKDIR /app

RUN curl -sSL https://install.python-poetry.org | python -
ENV PATH="/root/.local/bin:$PATH"

RUN poetry config virtualenvs.create false
