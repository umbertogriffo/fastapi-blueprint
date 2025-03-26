# FastAPI Blueprint

[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit)](https://github.com/pre-commit/pre-commit)
[![Code style: Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

A minimal FastAPI blueprint to start a project from scratch.

Features:
 - 🛠️ configuration in a single file pyproject.toml
 - 📦 uv as package manager
 - 💅 ruff for linting and formatting
 - 🧪 pytest
 - 🧹 Makefile with code quality checks
 - 🐳 Optimized and secure Docker Image

## Prerequisites

* Python 3.10+
* uv 0.6.10+

### Install uv

Install `uv` with the official installer by following
this [link](https://docs.astral.sh/uv/getting-started/installation/).

## Installation

To set it up and run:
```shell
uv sync
```

Then:
```shell
python app/main.py
```

## Docker

Build the Docker image with:
```
docker build --no-cache -t fastapi-app:latest .
```

Run the Docker container locally with:
```
docker run --rm -p 8080:8080 -v $(pwd)/.env:/usr/app/.env fastapi-app:latest
```

Run the service container by calling the following command from within the project folder:
```commandline
docker compose up -d --build
```
> [!NOTE]
> or for docker version < 20.10.0:
```commandline
docker-compose up -d --build
```

To stop it:
```commandline
docker compose down
```

## Example of requests

```shell
curl -X GET \
  "http://127.0.0.1:8080/health"
```

```shell
curl -X GET \
  "http://127.0.0.1:8080/users/" \
  | jq '.'
```

## Resources
- [Using uv with FastAPI](https://docs.astral.sh/uv/guides/integration/fastapi/#using-uv-with-fastapi)
- [Deployments Concepts](https://fastapi.tiangolo.com/deployment/concepts/)
