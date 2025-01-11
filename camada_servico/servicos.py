from adapters.repositorio import RepositorioPedido, RepositorioProduto
from config import RABBITMQ_URL
from camada_servico.barramento_mensagens import BarramentoMensagens
from domain.modelo import Pedido
from domain.eventos import PrecoProdutoAtualizadoEvento
from domain.eventos import PedidoCriadoEvento,StatusPedidoAtualizadoEvento

class ServicoProduto:
    def __init__(self, repositorio: RepositorioProduto, barramento_eventos:BarramentoMensagens):
        self.repositorio = repositorio
        self.barramento_eventos = barramento_eventos

    def atualizar_preco(self, id_produto, novo_preco):
        produto = self.repositorio.obter_produto_por_id(id_produto)
        if not produto:
            raise ValueError(f"Produto com ID {id_produto} não encontrado.")
        
        preco_antigo, preco_atualizado = produto.atualizar_preco(novo_preco)
        self.repositorio.salvar_produto(produto)

        # Publicar evento
        evento = PrecoProdutoAtualizadoEvento(
            id_produto=id_produto, preco_antigo=preco_antigo, preco_novo=preco_atualizado
        )
        self.barramento_eventos.publicar(evento)



class ServicoPedido:
    def __init__(self, repositorio: RepositorioPedido, barramento_eventos:BarramentoMensagens):
        self.repositorio = repositorio
        self.barramento_eventos = barramento_eventos

    def criar_pedido(self, id_pedido, id_cliente, itens):
        """
        Lógica para criar um novo pedido.
        """
        pedido = Pedido(id_pedido=id_pedido, id_cliente=id_cliente, itens=itens)
        self.repositorio.salvar_pedido(pedido)

        # Dispara evento de criação do pedido
        evento = PedidoCriadoEvento(id_pedido=id_pedido, id_cliente=id_cliente, itens=itens)
        self.barramento_eventos.publicar(evento)

    def atualizar_status(self, id_pedido, novo_status):
        """
        Lógica para atualizar o status de um pedido.
        """
        pedido = self.repositorio.obter_pedido_por_id(id_pedido)
        if not pedido:
            raise ValueError(f"Pedido com ID {id_pedido} não encontrado.")
        
        status_anterior, status_atual = pedido.atualizar_status(novo_status)
        self.repositorio.salvar_pedido(pedido)

        # Dispara evento de atualização de status
        evento = StatusPedidoAtualizadoEvento(
            id_pedido=id_pedido,
            status_anterior=status_anterior,
            status_atual=status_atual
        )
        self.barramento_eventos.publicar(evento)