def manipulador_pedido_criado(evento):
    print(f"Pedido criado com sucesso! ID: {evento.id_pedido}, Cliente: {evento.id_cliente}")
