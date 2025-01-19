FROM python:3.9-slim

WORKDIR /app

COPY ./requirements.txt ./
RUN pip install -r requirements.txt

# Copiar todos os arquivos do projeto
COPY . .

ENV PYTHONPATH=/app

# Tornar o script bash executável
RUN chmod +x /app/entrypoint.sh

# Usar o script como ponto de entrada
CMD ["/app/entrypoint.sh"]
