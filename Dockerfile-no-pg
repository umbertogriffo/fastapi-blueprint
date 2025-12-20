FROM python:3.10-slim AS builder

# Update image
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Set working directory and environment variables
WORKDIR /usr/app/

# Install the project without the the source code (only dependencies)
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-install-project --no-dev --compile-bytecode

# Install the project's source packages
COPY pyproject.toml uv.lock src/ /usr/app/src/

# Use alpine for the final image to reduce the total size
FROM python:3.10-alpine

# Set environment variables
# PYTHONDONTWRITEBYTECODE - Ensures that python compiler does not create .pyc file for the python source files within your production environment.
# PYTHONUNBUFFERED - Enables the python interpreter to immediately write out logs and outputs to the console.
# Configure PATH for executables, packages are in the /usr/app/.venv folder
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    LOGLEVEL="INFO" \
    PATH="/usr/app/.venv/bin:$PATH" \
    HOME="/home/appuser"

# Create a non-root user and group to improve the security of the container by
# isolating processes from the host system, mitigating privilege escalation risks,
# and aligning with the Principle of Least Privilege.
RUN addgroup --system appuser && adduser --system appuser --ingroup appuser

# Install curl for health checks and other dependencies
RUN apk add --no-cache curl libgcc libstdc++ gcompat && \
    rm -rf /var/lib/apt/lists/*

# Copy the installed environment from builder
# Change ownership of the working directory to the non-root user.
# This ensures that the default user within the container running the app is non root user.
COPY --from=builder --chown=appuser:appuser /usr/app/ /usr/app/

# Set working directory
WORKDIR /usr/app/

# Create a home directory for appuser and set HOME environment variable
RUN mkdir -p /home/appuser/.aws \
    && chown -R appuser:appuser /home/appuser

# Switch to the non-root user
USER appuser

CMD ["python", "src/main.py"]
