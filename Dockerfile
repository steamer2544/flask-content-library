FROM python:3.9-buster

WORKDIR /app

RUN apt-get update && \
    apt-get install -y build-essential sqlite3 && \
    rm -rf /var/lib/apt/lists/*

RUN apt update && apt install -y sqlite3

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
