FROM debian:bookworm

# Set working directory
WORKDIR /app

# Copy your application code into the container
COPY . .

# Install OS-level dependencies
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-dev \
    build-essential \
    gcc \
    libffi-dev \
    libgpiod-dev \
    libgpiod2 \
    python3-libgpiod \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip3 install --no-cache-dir -r requirements.txt --break-system-packages

# Expose a port if your app listens (adjust as needed)
EXPOSE 8000

