# Usar uma imagem oficial e estável do Python
FROM python:3.10-slim

# Definir o diretório de trabalho dentro do contentor
WORKDIR /app

# Instalar pacotes de sistema para o Tesseract, Locale e dependências de imagem (Pillow)
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    tesseract-ocr-por \
    libjpeg-dev \
    zlib1g-dev \
    libpq-dev \
    locales \
    git \
    gcc \
    tcl-dev \
    tk-dev

# Configurar o locale pt_BR.UTF-8 de forma robusta
RUN echo "pt_BR.UTF-8 UTF-8" > /etc/locale.gen && \
    locale-gen
ENV LANG=pt_BR.UTF-8
ENV LANGUAGE=pt_BR:en
ENV LC_ALL=pt_BR.UTF-8

# Copiar o ficheiro de requisitos e instalar as bibliotecas
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copiar o resto do seu código para dentro do contentor
COPY . .

# Expor a porta que a sua aplicação irá usar
EXPOSE 5000

# Comando para iniciar a sua aplicação quando o contentor arrancar
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]