FROM python:3.10-slim

# Create a non-root user and group to improve the security of the container by
# isolating processes from the host system, mitigating privilege escalation risks,
# and aligning with the Principle of Least Privilege.
RUN addgroup --system appuser && adduser --system appuser --ingroup appuser

# Update image
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*
# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Set working directory
WORKDIR /usr/app/
ENV LOGLEVEL="INFO"
# Ensures that python compiler does not create .pyc file for the python source files within your production environment.
ENV PYTHONDONTWRITEBYTECODE 1
# Enables the python interpreter to immediately write out logs and outputs to the console.
ENV PYTHONUNBUFFERED 1

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

# Change ownership of the working directory to the non-root user.
# This ensures that the default user within the container running the app is non root user.
RUN chown -R appuser:appuser /usr/app/

# Switch to the non-root user
USER appuser

CMD ["uv", "run", "python", "src/main.py"]
