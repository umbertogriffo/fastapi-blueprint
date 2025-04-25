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
ENV LOGLEVEL="INFO"
# Ensures that python compiler does not create .pyc file for the python source files within your production environment.
ENV PYTHONDONTWRITEBYTECODE 1
# Enables the python interpreter to immediately write out logs and outputs to the console.
ENV PYTHONUNBUFFERED 1

# Create a non-root user and group to improve the security of the container by
# isolating processes from the host system, mitigating privilege escalation risks,
# and aligning with the Principle of Least Privilege.
RUN addgroup --system appuser && adduser --system appuser --ingroup appuser

# Install curl for health checks and other dependencies
RUN apk add --no-cache curl libgcc libstdc++ gcompat

# Copy the installed environment from builder
COPY --from=builder --chown=appuser:appuser /usr/app/ /usr/app/

# Set working directory
WORKDIR /usr/app/

# Configure PATH for executables, packages are in the /usr/app/.venv folder
ENV PATH="/usr/app/.venv/bin:$PATH"

# Create a home directory for appuser and set HOME environment variable
RUN mkdir -p /home/appuser/.aws \
    && chown -R appuser:appuser /home/appuser
ENV HOME=/home/appuser

# Change ownership of the working directory to the non-root user.
# This ensures that the default user within the container running the app is non root user.
RUN chown -R appuser:appuser /usr/app/

# Switch to the non-root user
USER appuser

CMD ["python", "src/main.py"]
