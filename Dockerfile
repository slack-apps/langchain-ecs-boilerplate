FROM --platform=linux/x86_64 python:3.9-bullseye

WORKDIR /app

RUN curl -sSL https://install.python-poetry.org | python -
ENV PATH="/root/.local/bin:$PATH"

COPY poetry.lock pyproject.toml ./

RUN poetry config virtualenvs.create false && \
    poetry install --only main --no-interaction --no-ansi --no-root

COPY src .

EXPOSE 80

ENTRYPOINT ["python", "main.py"]