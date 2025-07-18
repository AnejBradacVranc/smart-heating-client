FROM arm64v8/python:3.10

WORKDIR /app

COPY . .

RUN apt-get update && apt-get install -y \
    gcc \
    build-essential \
    python3-dev \
    libffi-dev \
    libgpiod2 \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000
