# syntax=docker/dockerfile:1.4
FROM python:3.12-slim

ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        build-essential \
        ocrmypdf \
        poppler-utils \
        tesseract-ocr \
        tesseract-ocr-kor \
        fonts-noto-cjk \
        swig \
        libqpdf-dev \
        libxml2-dev \
        libxslt1-dev \
        libffi-dev \
        libjpeg-dev \
        zlib1g-dev && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN swig -version

WORKDIR /app

COPY pyproject.toml README.md requirements.txt ./
COPY src ./src
COPY configs ./configs
COPY scripts ./scripts

RUN pip install --upgrade pip && pip install -e .

ENTRYPOINT ["pdf-translate"]
CMD ["--config", "configs/config.yaml"]
