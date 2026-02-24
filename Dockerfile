FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ .

ENV HOST=0.0.0.0
ENV PORT=8080
ENV LOG_LEVEL=INFO

CMD ["python", "-m", "main"]