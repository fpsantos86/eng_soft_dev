from unittest.mock import Mock
from domain.consultas import ConsultarDetalhesPedido, ListarPedidosCliente
from camada_servico.manipuladores_consulta import manipular_consultar_detalhes_pedido, manipular_listar_pedidos_cliente

def test_manipular_consultar_detalhes_pedido():
    repositorio = Mock()
    repositorio.obter.return_value = Mock(
        id_pedido="pedido1", id_cliente="cliente1", status="Pendente", itens=[Mock(id="prod1", quantidade=2)]
    )
    consulta = ConsultarDetalhesPedido(id_pedido="pedido1")

    resultado = manipular_consultar_detalhes_pedido(consulta, repositorio)

    assert resultado == {
        "id_pedido": "pedido1",
        "id_cliente": "cliente1",
        "status": "Pendente",
        "itens": [{"id": "prod1", "quantidade": 2}],
    }

def test_manipular_listar_pedidos_cliente():
    repositorio = Mock()
    repositorio.listar_por_cliente.return_value = [
        Mock(id_pedido="pedido1", status="Pendente", itens=[Mock()]),
        Mock(id_pedido="pedido2", status="Concluído", itens=[Mock(), Mock()]),
    ]
    consulta = ListarPedidosCliente(id_cliente="cliente1")

    resultado = manipular_listar_pedidos_cliente(consulta, repositorio)

    assert resultado == [
        {"id_pedido": "pedido1", "status": "Pendente", "quantidade_itens": 1},
        {"id_pedido": "pedido2", "status": "Concluído", "quantidade_itens": 2},
    ]
