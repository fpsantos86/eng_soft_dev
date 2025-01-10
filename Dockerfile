# Use uma imagem base do Python
FROM python:3.9-slim

# Configure diretório de trabalho
WORKDIR /app

# Copie os arquivos do seu projeto para o container
COPY . /app

# Instale as dependências do Python
RUN pip install --no-cache-dir -r requirements.txt

# Exponha a porta onde o Flask irá rodar
EXPOSE 7000

# Comando padrão (pode ser sobrescrito pelo docker-compose)
CMD ["sh", "-c", "python main.py & python camada_servico/consumidor_eventos.py"]

