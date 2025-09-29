# Python 3.13 slim version for a minimal footprint
FROM python:3.13-slim

# Create the app directory
RUN mkdir /app

# Set working directory for all subsequent commands
WORKDIR /app

# Prevents Python from writing pyc files to disk
ENV PYTHONDONTWRITEBYTECODE=1
# Ensures Python output is sent straight to terminal without buffering
ENV PYTHONUNBUFFERED=1

# Install system dependencies:
# libpq-dev: Required for psycopg2 (PostgreSQL adapter)
# gcc: Required for compiling some Python packages
# curl and ca-certificates for uv
RUN apt-get update \
  && apt-get -y install libpq-dev gcc curl ca-certificates

# Install uv
# The installer requires curl (and certificates) to download the release archive
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates

# Download the latest installer
ADD https://astral.sh/uv/install.sh /uv-installer.sh

# Run the installer then remove it
RUN sh /uv-installer.sh && rm /uv-installer.sh

# Ensure the installed binary is on the `PATH`
ENV PATH="/root/.local/bin/:$PATH"

# Copy uv lock file first to leverage Docker cache
COPY uv.lock .
COPY pyproject.toml .

# Install project dependencies
RUN uv sync --locked

# Copy the Django project to container
COPY . .

# Expose the Django port
EXPOSE 8004

# Make entrypoint script executable
RUN chmod +x /app/entrypoint.prod.sh

# Set the entrypoint script as the default command
# This will run migrations, collect static files, and start Gunicorn
CMD ["/app/entrypoint.prod.sh"]
