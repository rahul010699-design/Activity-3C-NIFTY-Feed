FROM python:3.12-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY alerter/ ./alerter/

EXPOSE 8001

CMD ["python", "alerter/main.py"]
