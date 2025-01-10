import os
from pymongo import MongoClient

IS_DOCKER = os.getenv("IS_DOCKER", "false").lower() == "true"
# Variáveis de conexão (use seu .env ou substitua os valores diretamente)
MONGO_HOST = "localhost"
MONGO_PORT = int(os.getenv("MONGO_PORT", "37017" if not IS_DOCKER else "27017"))
MONGO_USER = "admin"  # Altere se necessário
MONGO_PASSWORD = "admin123"  # Altere se necessário
MONGO_DB_NAME = "cqrs_db"
MONGO_COLLECTION_NAME = "produtos"

# Conexão com o MongoDB
uri = f"mongodb://{MONGO_USER}:{MONGO_PASSWORD}@{MONGO_HOST}:{MONGO_PORT}/?authSource=admin"
client = MongoClient(uri)

# Criar banco de dados e collection
db = client[MONGO_DB_NAME]
collection = db[MONGO_COLLECTION_NAME]

#Inserir um documento de exemplo para garantir que tudo está funcionando
documento_exemplo = {
    "id_produto": "12345",
    "nome": "Produto Exemplo",
    "descricao": "Descrição do produto exemplo",
    "preco": 99.99,
    "quantidade_estoque": 10
}
collection.insert_one(documento_exemplo)

print(f"Banco de dados '{MONGO_DB_NAME}' e coleção '{MONGO_COLLECTION_NAME}' criados com sucesso!")
print(f"Documento inserido: {documento_exemplo}")

collection.delete_one({'id_produto':"12345"})
print(f"Documento excluido: {documento_exemplo}")