import pika
import json
import time
import logging
from pymongo import MongoClient
from config import RABBITMQ_HOST, RABBITMQ_PORT, RABBITMQ_USER, RABBITMQ_PASSWORD
from config import MONGO_HOST, MONGO_PORT, MONGO_DB_NAME, MONGO_USER, MONGO_PASSWORD, MONGO_COLLECTION_NAME

# Configuração do logging para exibir mensagens no stdout
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Conexão com o MongoDB
client = MongoClient(f"mongodb://{MONGO_USER}:{MONGO_PASSWORD}@{MONGO_HOST}:{MONGO_PORT}/?authSource=admin")
db = client[MONGO_DB_NAME]
collection = db[MONGO_COLLECTION_NAME]

def iniciar_consumidor_produtos():
    while True:  # Loop para retry infinito até o RabbitMQ estar disponível
        try:
            logger.info("Tentando conectar ao RabbitMQ...")
            connection = pika.BlockingConnection(pika.ConnectionParameters(
                host=RABBITMQ_HOST,
                port=RABBITMQ_PORT,
                credentials=pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASSWORD)
            ))

            channel = connection.channel()

            # Declarar a fila
            channel.queue_declare(queue='eventos_produtos', durable=True)

            def callback(ch, method, properties, body):
                logger.info(f"Recebida mensagem: {body}")
                # Converte o corpo da mensagem de JSON para dicionário
                mensagem = json.loads(body)

                # Gravação no MongoDB
                try:
                    collection.insert_one(mensagem)
                    logger.info(f"Registro inserido no MongoDB: {mensagem}")
                except Exception as e:
                    logger.error(f"Erro ao inserir no MongoDB: {e}")

            channel.basic_consume(queue='eventos_produtos', on_message_callback=callback, auto_ack=True)

            logger.info("Conexão bem-sucedida com o RabbitMQ. Esperando mensagens. Para sair, pressione CTRL+C.")
            channel.start_consuming()

        except pika.exceptions.AMQPConnectionError as e:
            logger.error(f"Erro ao conectar ao RabbitMQ: {e}")
            logger.info("Tentando novamente em 5 segundos...")
            time.sleep(5)
        except Exception as e:
            logger.critical(f"Erro inesperado: {e}")
            break  # Interrompe o loop em caso de erro inesperado

if __name__ == "__main__":
    iniciar_consumidor_produtos()
