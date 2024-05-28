FROM --platform=linux/amd64 python:3.8-slim as build

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY scrape.py .

CMD ["python", "scrape.py"]
