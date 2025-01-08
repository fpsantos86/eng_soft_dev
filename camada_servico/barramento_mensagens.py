import pika
import json
from config import RABBITMQ_URL

class BarramentoMensagens:
    def __init__(self):
        self.connection = pika.BlockingConnection(pika.URLParameters(RABBITMQ_URL))
        self.channel = self.connection.channel()

    def configurar_exchange(self, exchange_name):
        """
        Configura um exchange no RabbitMQ.
        """
        self.channel.exchange_declare(exchange=exchange_name, exchange_type="fanout")

    def publicar(self, exchange_name, evento):
        """
        Publica um evento no RabbitMQ.
        """
        #evento = {"id_produto": "12345", "nome": "Produto Teste", "descricao": "Teste de Publicação"}
        event =  evento.__dict__
        self.channel.basic_publish(
            exchange=exchange_name,
            routing_key=exchange_name,
            body=json.dumps(event),
            properties=pika.BasicProperties(content_type="application/json")
        )

    def consumir(self, fila, callback):
        """
        Consome mensagens de uma fila e executa um callback para cada mensagem.
        """
        # Declara uma fila para garantir que ela exista
        self.channel.queue_declare(queue=fila, durable=True)

        # Vincula a fila ao exchange
        self.channel.queue_bind(exchange="eventos_pedidos", queue=fila)

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
