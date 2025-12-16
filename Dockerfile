FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY backend backend
COPY templates templates

ENV PYTHONPATH=/app
ENV FLASK_ENV=production

EXPOSE 8000

CMD ["python", "-m", "backend.app"]