#!/bin/bash

echo "Executando setup do PostgreSQL..."
python /app/scripts/setup_postgres.py

echo "Executando setup do MongoDB..."
python /app/scripts/setup_mongodb.py

echo "Setup concluído. Iniciando aplicação principal..."
python /app/main.py

echo "Executando setup do MongoDB..."
python /app/camada_servico/consumidor_eventos.py