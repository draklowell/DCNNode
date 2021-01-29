FROM python:3.8-slim-buster

ENV PYTHONDONTWRITEBYTECODE=1

ENV PYTHONUNBUFFERED=1

COPY requirements.txt .
RUN python -m pip install -r requirements.txt

WORKDIR /app
COPY . /app

RUN apt update -y
RUN apt install libcap2-bin -y
RUN setcap cap_net_bind_service=+ep /usr/local/bin/python3.8

RUN useradd appuser && chown -R appuser /app
USER appuser


CMD ["python", "main.py"]
