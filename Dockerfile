FROM python:3.10-slim

# Create a non-root user and group to improve the security of the container
RUN addgroup --system appuser && adduser --system appuser --ingroup appuser

# Update image
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*
# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Set working directory
WORKDIR /usr/app/
ENV LOGLEVEL="INFO"

# Install the project without the the source code (only dependencies)
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-install-project --no-dev --compile-bytecode

# Copy the application into the container
ADD pyproject.toml uv.lock src/ ./src/

# Create a home directory for appuser and set HOME environment variable
RUN mkdir -p /home/appuser/.aws && chown -R appuser:appuser /home/appuser
ENV HOME=/home/appuser

# Change ownership of the working directory to the non-root user
RUN chown -R appuser:appuser /usr/app/

# Switch to the non-root user
USER appuser

CMD ["uv", "run", "python", "src/main.py"]
