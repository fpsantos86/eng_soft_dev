import pika
import json
from config import RABBITMQ_URL

class BarramentoMensagens:
    def __init__(self):
        self.connection = pika.BlockingConnection(pika.URLParameters(RABBITMQ_URL))
        self.channel = self.connection.channel()

    def configurar_exchange(self, exchange_name, exchange_type="direct"):
        """
        Declara um exchange no RabbitMQ.
        """
        self.channel.exchange_declare(exchange=exchange_name, exchange_type=exchange_type, durable=True)
    
    def configurar_fila(self, exchange_name, fila, routing_key):
        """
        Declara e configura uma fila vinculada a um exchange no RabbitMQ.
        """
        self.channel.queue_declare(queue=fila, durable=True)
        self.channel.queue_bind(exchange=exchange_name, queue=fila, routing_key=routing_key)
    
    def publicar_produto(self, exchange_name, routing_key, evento):
        """
        Publica um evento no RabbitMQ em uma exchange com a routing_key.
        """
        event = evento if isinstance(evento, dict) else evento.__dict__
        self.channel.basic_publish(
            exchange=exchange_name,
            routing_key=routing_key,
            body=json.dumps(event),
            properties=pika.BasicProperties(content_type="application/json")
        )

    def publicar(self, evento):
        """
        Publica um evento no RabbitMQ.
        """
        exchange_name = "eventos"
        routing_key = "evento_key"
        event = evento if isinstance(evento, dict) else evento.__dict__
        self.channel.basic_publish(
            exchange=exchange_name,
            routing_key=routing_key,
            body=json.dumps(event),
            properties=pika.BasicProperties(content_type="application/json")
        )

    def consumir(self, exchange_name, fila, routing_key, callback):
        """
        Consome mensagens de uma fila vinculada a uma routing_key específica.
        """
        # Declara a fila para garantir que ela exista
        self.channel.queue_declare(queue=fila, durable=True)

        # Vincula a fila ao exchange com a routing_key
        self.channel.queue_bind(exchange=exchange_name, queue=fila, routing_key=routing_key)

        # Define o consumidor com um callback
        def processar_mensagem(ch, method, properties, body):
            mensagem = json.loads(body)
            callback(mensagem)
            ch.basic_ack(delivery_tag=method.delivery_tag)

        self.channel.basic_consume(queue=fila, on_message_callback=processar_mensagem)


        
    def iniciar_consumo(self):
        """
        Inicia o loop de consumo.
        """
        print("Esperando mensagens. Pressione CTRL+C para sair.")
        self.channel.start_consuming()
    def fechar_conexao(self):
        """
        Fecha a conexão com o RabbitMQ.
        """
        self.connection.close()
