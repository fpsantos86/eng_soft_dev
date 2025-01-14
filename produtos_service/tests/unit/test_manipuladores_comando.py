from unittest.mock import Mock

from camada_servico.manipuladores_comando import manipular_atualizar_status_pedido, manipular_criar_pedido
from domain.comandos import AtualizarStatusPedidoComando, CriarPedidoComando
from domain.eventos import PedidoCriadoEvento, StatusPedidoAtualizadoEvento
from domain.modelo import ItemPedido, Pedido

def test_manipular_criar_pedido():
    # Simular dependências
    servico_mock = Mock()
    barramento_mock = Mock()

    # Criar itens simulados
    itens = [ItemPedido(id="prod1", quantidade=2, preco=50.0)]
    pedido_simulado = Pedido(id_pedido="pedido1", id_cliente="cliente1", itens=itens)

    # Configurar o mock para retornar o pedido simulado
    servico_mock.criar_pedido.return_value = pedido_simulado

    # Criar comando para o manipulador
    comando = CriarPedidoComando(
        id_pedido="pedido1",
        id_cliente="cliente1",
        itens=[{"id": "prod1", "quantidade": 2}]
    )

    # Chamar o manipulador com os mocks
    manipular_criar_pedido(comando, servico_mock, barramento_mock)

    # Asserções para verificar comportamento esperado
    servico_mock.criar_pedido.assert_called_once_with("pedido1", "cliente1", comando.itens)
    barramento_mock.publicar.assert_called_once()

def test_manipular_atualizar_status_pedido():
    # Simular dependências
    servico_mock = Mock()

    # Configurar o mock para retornar um pedido
    pedido_simulado = Pedido(id_pedido="pedido1", id_cliente="cliente1", itens=[], status="Pendente")
    servico_mock.repositorio.obter.return_value = pedido_simulado

    # Criar comando para o manipulador
    comando = AtualizarStatusPedidoComando(
        id_pedido="pedido1",
        novo_status="Concluído"
    )

    # Chamar o manipulador com o mock
    manipular_atualizar_status_pedido(comando, servico_mock)

    # Asserções para verificar comportamento esperado
    servico_mock.atualizar_status.assert_called_once_with(
        id_pedido="pedido1",
        novo_status="Concluído"
    )