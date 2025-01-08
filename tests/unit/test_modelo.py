import pytest
from domain.modelo import Pedido, ItemPedido

def test_criar_pedido():
    itens = [ItemPedido(id_produto="prod1", quantidade=2, preco=50.0)]
    pedido = Pedido(id_pedido="pedido1", id_cliente="cliente1", itens=itens)
    assert pedido.id_pedido == "pedido1"
    assert pedido.id_cliente == "cliente1"
    assert pedido.status == "Pendente"
    assert len(pedido.itens) == 1
    assert pedido.calcular_total() == 100.0  # Verifica o cálculo do total do pedido

def test_atualizar_status():
    pedido = Pedido(id_pedido="pedido1", id_cliente="cliente1", itens=[])
    status_anterior, status_novo = pedido.atualizar_status("Concluído")
    assert status_anterior == "Pendente"
    assert status_novo == "Concluído"
    assert pedido.status == "Concluído"

def test_cancelar_pedido():
    pedido = Pedido(id_pedido="pedido1", id_cliente="cliente1", itens=[])
    pedido.cancelar()
    assert pedido.status == "Cancelado"

def test_cancelar_pedido_concluido():
    pedido = Pedido(id_pedido="pedido1", id_cliente="cliente1", itens=[], status="Concluído")
    with pytest.raises(ValueError, match="Não é possível cancelar um pedido já concluído."):
        pedido.cancelar()

def test_calcular_total_pedido():
    itens = [
        ItemPedido(id_produto="prod1", quantidade=2, preco=50.0),
        ItemPedido(id_produto="prod2", quantidade=1, preco=100.0),
    ]
    pedido = Pedido(id_pedido="pedido1", id_cliente="cliente1", itens=itens)
    assert pedido.calcular_total() == 200.0  # Verifica o total correto
