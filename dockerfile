FROM python:3.14-slim-bookworm

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Download the latest installer
ADD https://astral.sh/uv/install.sh /uv-installer.sh

# Run the installer then remove it
RUN sh /uv-installer.sh && rm /uv-installer.sh

# Ensure the installed binary is on the `PATH` and use environment
ENV PATH="/root/.local/bin/:$PATH"
ENV PATH="/app/.venv/bin:$PATH"

# Copy project files

COPY pyproject.toml README.md app.py uv.lock ./
COPY backend backend/
COPY frontend frontend/

# Install Python dependencies
RUN uv sync --frozen

# Expose port
EXPOSE 8000

# Run the application using `uv run`
CMD ["python", "app.py"]