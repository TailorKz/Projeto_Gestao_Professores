FROM python:3.10-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    tesseract-ocr-por \
    libjpeg-dev \
    libpng-dev \
    libtiff5 \
    zlib1g-dev \
    libpq-dev \
    locales \
    git \
    gcc \
    tcl-dev \
    tk-dev && \
    rm -rf /var/lib/apt/lists/*

# Configuração de locale mais universal
ENV LANG=C.UTF-8
ENV LC_ALL=C.UTF-8

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Verificar se o tesseract está instalado
RUN which tesseract && tesseract --version

EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
