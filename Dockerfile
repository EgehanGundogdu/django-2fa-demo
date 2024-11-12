FROM python:3.12.3-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /usr/src/app

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
       gcc \
       libpq-dev \
       build-essential \
       python3-dev \
    && rm -rf /var/lib/apt/lists/*


COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY ./src .



