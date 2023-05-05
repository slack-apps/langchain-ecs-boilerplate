# Welcome to your CDK Python project!

```shell
python3 -m venv .venv
source .venv/bin/activate
poetry install --no-root
```

```shell
python src/main.py
```

## docker

```shell
docker-compose up --build
```

```shell
docker-compose exec python bash
poetry install --no-root --only main
python src/main.py
```