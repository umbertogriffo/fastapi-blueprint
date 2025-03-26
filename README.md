# FastAPI Blueprint

A minimal FastAPI blueprint to start a project from scratch.

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

docker run --rm -v -p 8080:8080 fastapi-app:latest

## Example of requests

```shell
curl -X GET \
  "http://127.0.0.1:8080/users/" \
  | jq '.'
```

## Resources
- [Using uv with FastAPI](https://docs.astral.sh/uv/guides/integration/fastapi/#using-uv-with-fastapi)
