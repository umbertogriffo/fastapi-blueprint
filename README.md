# FastAPI Blueprint

[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit)](https://github.com/pre-commit/pre-commit)
[![Code style: Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)

A minimal FastAPI blueprint to start a project from scratch.

Application Features:
 - ⚙️ Configurable with BaseSettings of Pydantic
 - 📄 Structured Logging
 - 🔒 API endpoints secured with API key authentication
 - 🛡️ Centralized error handling with custom exceptions and detailed logging

Repo Features:
 - 🛠️ configuration in a single file pyproject.toml
 - 📦 uv as package manager
 - 💅 ruff for linting and formatting
 - 🧪 pytest
 - 🧹 Makefile
 - 🐳 Optimized and secure Docker Image (~107MB)
 - 🚀 Docker compose configuration for local development

## Table of contents

- [FastAPI Blueprint](#fastapi-blueprint)
  - [Prerequisites](#prerequisites)
    - [Install uv](#install-uv)
  - [Bootstrap Environment](#bootstrap-environment)
    - [How to use the make file](#how-to-use-the-make-file)
    - [Run the application](#run-the-application)
  - [Docker](#docker)
  - [Example of requests](#example-of-requests)
  - [Resources](#resources)

## Prerequisites

* Python 3.10+
* uv 0.6.10+

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
python app/main.py
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
