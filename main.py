import threading
from flask import json
from entry_points.app_flask import app
from domain.eventos import PedidoCriadoEvento, ProdutoAdicionadoEvento
from adapters.repositorio_mongo import RepositorioConsultaMongoDB
from camada_servico.manipuladores_evento import manipulador_pedido_criado
from camada_servico.manipuladores_consulta import consumir_evento_produto_adicionado
from camada_servico.barramento_mensagens import BarramentoMensagens

repositorio_mongodb = RepositorioConsultaMongoDB()


# Configuração do barramento
barramento_mensagens = BarramentoMensagens()
barramento_mensagens.configurar_exchange("eventos_pedidos")

def iniciar_consumidor():
    barramento_mensagens = BarramentoMensagens()
    barramento_mensagens.consumir(
        fila="eventos_produtos",
        callback=lambda ch,method,properties,body: consumir_evento_produto_adicionado(
            ProdutoAdicionadoEvento(**json.loads(body)),
            repositorio_mongodb
        )
    )

    barramento_mensagens.consumir(
        fila="eventos_pedidos",  # Nome da fila correspondente ao evento
        callback=lambda ch, method, properties, body: manipulador_pedido_criado(
            PedidoCriadoEvento(**json.loads(body))
        )
    )

# Inicializar o consumidor em uma thread separada
consumidor_thread = threading.Thread(target=iniciar_consumidor, daemon=True)
consumidor_thread.start()



if __name__ == "__main__":
    # Configuração adicional, se necessário
    app.run(host="0.0.0.0", port=5000, debug=True)