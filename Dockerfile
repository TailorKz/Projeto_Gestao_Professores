# Usar uma imagem oficial e estável do Python
FROM python:3.10-slim

# Definir o diretório de trabalho dentro do contentor
WORKDIR /app

# Copiar o ficheiro de requisitos e instalar as bibliotecas
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copiar o resto do seu código para dentro do contentor
COPY . .

# Expor a porta que a sua aplicação irá usar
EXPOSE 5000

# Comando para iniciar a sua aplicação quando o contentor arrancar
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]