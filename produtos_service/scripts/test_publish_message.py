from camada_servico.barramento_mensagens import BarramentoMensagens


barramento = BarramentoMensagens()
barramento.configurar_exchange("eventos_pedidos")

evento = {"id": "12345", "nome": "Produto Teste", "descricao": "Teste de Publicação"}
barramento.publicar("eventos_pedidos", evento)

print("Evento publicado no RabbitMQ.")
