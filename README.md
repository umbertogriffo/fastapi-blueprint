<p align="center"> <img src="https://github.com/umbertogriffo/fastapi-blueprint/blob/main/images/fast-api-blueprint-img.png" alt="FastAPI Blueprint" /></p>

[![CI](https://github.com/umbertogriffo/fastapi-blueprint/workflows/CI/badge.svg)](https://github.com/umbertogriffo/fastapi-blueprint/actions/workflows/ci.yaml)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit)](https://github.com/pre-commit/pre-commit)
[![Code style: Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

A minimal FastAPI blueprint to start a project from scratch.

Application Features:
 - ⚙️ Configurable with BaseSettings of Pydantic
 - 📄 Structured Logging
 - 🔒 API endpoints secured with API key authentication
 - 🛡️ Centralized error handling with custom exceptions and detailed logging
 - 💾 SQLite (Default) or PostgreSQL as the SQL database.

Repo Features:
 - 🛠️ configuration in a single file pyproject.toml
 - 📦 uv as package manager
 - 💅 ruff for linting and formatting
 - 🧪 pytest
 - 🧹 Makefile
 - 🐳 Optimized and secure Docker Image (~150MB, ~107MB without PostgreSQL client libraries)
 - 🚀 Docker compose configuration for local development
 - 🏭 CI (continuous integration) based on GitHub Actions

## Table of contents

- [Prerequisites](#prerequisites)
  - [Install uv](#install-uv)
- [Bootstrap Environment](#bootstrap-environment)
  - [How to use the make file](#how-to-use-the-make-file)
  - [Environment](#environment)
  - [Run the application](#run-the-application)
  - [Run the application with Docker Compose](#run-the-application-with-docker-compose)
- [Docker](#docker)
- [Generate Database Migrations](#generate-database-migrations)
- [Example of requests](#example-of-requests)
- [Resources](#resources)

## Prerequisites

* Python 3.10+
* uv 0.8.17+
* PoatgreSQL 18.1+ (if you want to use PostgreSQL as database)

### Install uv

Install `uv` with the official installer by following
this [link](https://docs.astral.sh/uv/getting-started/installation/).

## Bootstrap Environment

To easily install the dependencies we created a make file.

### How to use the make file

> [!IMPORTANT]
> Run `Setup` as your init command (or after `Clean`).

* Check: ```make check```
    * Use it to check that `which pip3` and `which python3` points to the right path.
* Setup: ```make setup```
    * Creates an environment and installs all dependencies.
* Tidy up the code: ```make tidy```
    * Run Ruff check and format.
* Clean: ```make clean```
    * Removes the environment and all cached files.
* Test: ```make test```
    * Runs all tests.
    * Using [pytest](https://pypi.org/project/pytest/)

### Environment

Copy .𝐞𝐧𝐯.𝐞𝐱𝐚𝐦𝐩𝐥𝐞 → .𝐞𝐧𝐯 and fill it in.

### Run the application

```shell
cd src
# Run the application
python main.py
```

The blueprint also gives the possibility to use `SQLModel` (SQLAlchemy) with support for `SQLite` and `PostgreSQL`.

If you want to use a `SQLite` backed database, make sure to set the `DATABASE_URL=sqlite:///database.db` variable in the .𝐞𝐧𝐯 file.

then run:
```shell
# perform the SQLite migrations
cd src && migrate-db
# or directly with alembic
# uv run alembic --config src/alembic.ini upgrade head

# Run the application
uv run python src/main.py
```

While if you want to use a `PostgreSQL` backed database set `DATABASE_URL=postgresql://develop:develop_secret@localhost:5432/develop` variable in the .𝐞𝐧𝐯 file.

then run:
```shell
# Let's spin up a Postgres instance with the migrated dataset with Docker Compose
dc db up -d
# Run the application
uv run python src/main.py
```

The code `migrate-db` can be found in [migration_cli.py](src/utils/cli/migration.py).
The code `dc` can be found in [docker_compose_cli.py](src/utils/cli/docker_compose.py).

### Run the application with Docker Compose

> [!NOTE]
> To run the service with PostgreSQL backed database set `DATABASE_URL=postgresql://develop:develop_secret@db:5432/develop`
> in .𝐞𝐧𝐯, setting db instead of localhost otherwise the service-api and migration can't reach the database container.

The `dc` CLI utility to run Docker Compose with specific profiles is available to start the application.

Run the following command for more information:

```bash
dc
```

With this CLI you can start the application in different modes, such as:

- `db` which only runs the `PostgreSQL` locally
- `all` which starts the entire application stack

For example, to start the entire application stack with building the images, run:

```bash
dc all up --build -d
```

To stop the application and remove the containers, run

```bash
dc all down
```

You can also skip the CLI util and run the service containers by calling the following command from within the project folder:
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

## Docker

> [!NOTE]
> Dockerfile contains a multi-stage build that uses `--compile-bytecode` to compile the packages.

Build the Docker image with:
```
docker build --no-cache -t fastapi-app:latest .
```

Run the Docker container locally with:
```
docker run --rm -p 8080:8080 -v $(pwd)/.env:/usr/app/.env fastapi-app:latest
```

## Generate Database Migrations

To generate new migration after adding fields to [SQLModel](src/models.py):

```bash
uv run alembic --config src/alembic.ini revision --autogenerate -m "your text"
```

## Example of requests

```shell
curl -X GET \
  "http://127.0.0.1:8080/health"
```

```shell
curl -X GET \
  "http://127.0.0.1:8080/users/" \
  -H 'Authorization: your-secret-api-key-here' \
  | jq '.'
```

```shell
curl -X GET \
  "http://127.0.0.1:8080/users/me" \
  -H 'Authorization: your-secret-api-key-here' \
  | jq '.'
```

```shell
curl -X POST \
  "http://127.0.0.1:8080/users/check" \
  -H 'Authorization: your-secret-api-key-here' \
  -H 'Content-Type: application/json' \
  -d '{"name": "admin"}' \
  | jq '.'
```

## Resources
- [Using uv with FastAPI](https://docs.astral.sh/uv/guides/integration/fastapi/#using-uv-with-fastapi)
- [Deployments Concepts](https://fastapi.tiangolo.com/deployment/concepts/)
- [How to secure APIs built with FastAPI: A complete guide](https://escape.tech/blog/how-to-secure-fastapi-api/)
- [Alembic](https://alembic.sqlalchemy.org/en/latest/front.html#installation)
