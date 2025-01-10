import pika
import json
from pymongo import MongoClient
from config import RABBITMQ_HOST, RABBITMQ_PORT, RABBITMQ_USER, RABBITMQ_PASSWORD
from config import MONGO_HOST, MONGO_PORT, MONGO_DB_NAME,MONGO_USER, MONGO_PASSWORD, MONGO_COLLECTION_NAME

# Conexão com o MongoDB
client = MongoClient(f"mongodb://{MONGO_USER}:{MONGO_PASSWORD}@{MONGO_HOST}:{MONGO_PORT}/?authSource=admin")
db = client[MONGO_DB_NAME]
collection = db[MONGO_COLLECTION_NAME]

def iniciar_consumidor_produtos():
    connection = pika.BlockingConnection(pika.ConnectionParameters( 
            host=RABBITMQ_HOST,
            port=RABBITMQ_PORT,
            credentials=pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASSWORD)
        )
    )
    
    channel = connection.channel()

    # Declarar a fila
    channel.queue_declare(queue='eventos_produtos', durable=True)

    def callback(ch, method, properties, body):
        print(f"Recebida mensagem: {body}")
        # Converte o corpo da mensagem de JSON para dicionário
        mensagem = json.loads(body)

        # Gravação no MongoDB
        try:
            collection.insert_one(mensagem)
            print(f"Registro inserido no MongoDB: {mensagem}")
        except Exception as e:
            print(f"Erro ao inserir no MongoDB: {e}")

    channel.basic_consume(queue='eventos_produtos', on_message_callback=callback, auto_ack=True)

    print("Esperando mensagens. Para sair, pressione CTRL+C.")
    channel.start_consuming()

if __name__ == "__main__":
    iniciar_consumidor_produtos()
