# ==========================
# 1️⃣ Base Image (Build Stage)
# ==========================
FROM python:3.10-slim AS builder

# Set work directory
WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends build-essential

# Copy dependency files first (leverage Docker cache)
COPY requirements.txt .
COPY requirements-dev.txt .

# Install only prod dependencies here (dev handled separately in CI/CD)
RUN pip install --no-cache-dir -r requirements.txt

# Copy app source
COPY app ./app

# ==========================
# 2️⃣ Final Image (Run Stage)
# ==========================
FROM python:3.10-slim

# Create non-root user
RUN useradd -m fastapiuser

WORKDIR /app

# Copy from builder stage
COPY --from=builder /usr/local/lib/python3.10/site-packages /usr/local/lib/python3.10/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin
COPY --from=builder /app /app


# Set environment variables
ENV PORT=8080
ENV PYTHONUNBUFFERED=1

# Switch to non-root user
USER fastapiuser

# Expose FastAPI port
EXPOSE 8080

# Run FastAPI app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
