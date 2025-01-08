import pika

def iniciar_consumidor():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    # Declare sua fila
    channel.queue_declare(queue='eventos_pedidos')

    def callback(ch, method, properties, body):
        print(f"Recebida mensagem: {body}")
        # Processar a mensagem aqui

    channel.basic_consume(queue='eventos_pedidos', on_message_callback=callback, auto_ack=True)

    print("Esperando mensagens. Para sair, pressione CTRL+C.")
    channel.start_consuming()
