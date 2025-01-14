from unittest.mock import Mock
from camada_servico.servicos import ServicoPedido, ServicoProduto
from domain.eventos import PedidoCriadoEvento, StatusPedidoAtualizadoEvento, PrecoProdutoAtualizadoEvento
from domain.modelo import Pedido, Produto, ItemPedido

def test_criar_pedido():
    # Configurar mocks
    repositorio_mock = Mock()
    barramento_mock = Mock()
    servico = ServicoPedido(repositorio_mock, barramento_mock)

    itens = [ItemPedido(id="prod1", quantidade=2, preco=10.0)]
    servico.criar_pedido("pedido1", "cliente1", itens)

    repositorio_mock.salvar_pedido.assert_called_once()
    barramento_mock.publicar.assert_called_once_with(
        PedidoCriadoEvento(id_pedido="pedido1", id_cliente="cliente1", itens=itens)
    )

def test_atualizar_status():
    pedido = Pedido(id_pedido="pedido1", id_cliente="cliente1", itens=[], status="Pendente")
    repositorio_mock = Mock()
    repositorio_mock.obter_pedido_por_id.return_value = pedido
    barramento_mock = Mock()
    servico = ServicoPedido(repositorio_mock, barramento_mock)

    servico.atualizar_status("pedido1", "Concluído")

    repositorio_mock.salvar_pedido.assert_called_once_with(pedido)
    barramento_mock.publicar.assert_called_once_with(
        StatusPedidoAtualizadoEvento(
            id_pedido="pedido1",
            status_anterior="Pendente",
            status_atual="Concluído"
        )
    )

def test_atualizar_preco():
    produto = Produto(
        id="prod1",
        nome="Produto 1",
        descricao="Descrição do Produto 1",
        preco=20.0,
        quantidade_estoque=10
    )
    repositorio_mock = Mock()
    repositorio_mock.obter_produto_por_id.return_value = produto
    barramento_mock = Mock()
    servico = ServicoProduto(repositorio_mock, barramento_mock)

    servico.atualizar_preco("prod1", 30.0)

    repositorio_mock.salvar_produto.assert_called_once_with(produto)
    barramento_mock.publicar.assert_called_once_with(
        PrecoProdutoAtualizadoEvento(
            id="prod1",
            preco_antigo=20.0,
            preco_novo=30.0
        )
    )
