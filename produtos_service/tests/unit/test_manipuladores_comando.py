from unittest.mock import Mock
import pytest

from camada_servico.manipuladores_comando import (
    manipular_adicionar_produto,
    manipular_atualizar_preco_produto,
    manipular_excluir_produto,
    manipular_atualizar_produto
)
from domain.comandos import (
    AdicionarProdutoComando,
    AtualizarPrecoProdutoComando,
    RemoverProdutoComando,
    AtualizarProdutoComando
)
from domain.eventos import ProdutoAdicionadoEvento, ProdutoRemovidoEvento, ProdutoAtualizadoEvento, PrecoProdutoAtualizadoEvento
from domain.modelo import Produto

def test_manipular_adicionar_produto():
    # Simular dependências
    repositorio_mock = Mock()
    barramento_mock = Mock()

    # Criar comando para o manipulador
    comando = AdicionarProdutoComando(
        id="prod1",
        nome="Produto 1",
        descricao="Descrição do Produto 1",
        preco=50.0,
        quantidade_estoque=100
    )

    # Chamar o manipulador com os mocks
    produto = manipular_adicionar_produto(comando, repositorio_mock, barramento_mock)

    # Asserções para verificar comportamento esperado
    repositorio_mock.salvar_produto.assert_called_once_with(produto)
    barramento_mock.publicar_produto.assert_called_once()
    assert produto.id == "prod1"
    assert produto.nome == "Produto 1"
    assert produto.descricao == "Descrição do Produto 1"
    assert produto.preco == 50.0
    assert produto.quantidade_estoque == 100

def test_manipular_atualizar_preco_produto():
    # Simular dependências
    servico_mock = Mock()
    produto_simulado = Produto(nome="Produto 1", descricao="Descrição do Produto 1", preco=50.0, quantidade_estoque=100, id="prod1")
    servico_mock.repositorio.obter_produto_por_id.return_value = produto_simulado

    # Criar comando para o manipulador
    comando = AtualizarPrecoProdutoComando(
        id="prod1",
        novo_preco=75.0
    )

    # Chamar o manipulador com o mock
    manipular_atualizar_preco_produto(comando, servico_mock)

    # Asserções para verificar comportamento esperado
    servico_mock.repositorio.salvar_produto.assert_called_once_with(produto_simulado)
    servico_mock.barramento_eventos.publicar.assert_called_once()
    assert produto_simulado.preco == 75.0

def test_manipular_excluir_produto():
    # Simular dependências
    repositorio_mock = Mock()
    barramento_mock = Mock()

    # Criar comando para o manipulador
    comando = RemoverProdutoComando(id="prod1")

    # Chamar o manipulador com os mocks
    manipular_excluir_produto(comando, repositorio_mock, barramento_mock)

    # Asserções para verificar comportamento esperado
    repositorio_mock.excluir_produto.assert_called_once_with("prod1")
    barramento_mock.publicar_produto.assert_called_once()

def test_manipular_atualizar_produto():
    # Simular dependências
    repositorio_mock = Mock()
    barramento_mock = Mock()

    # Criar comando para o manipulador
    comando = AtualizarProdutoComando(
        id="prod1",
        nome="Produto 1 Atualizado",
        descricao="Nova Descrição",
        preco=60.0,
        quantidade_estoque=150
    )

    # Chamar o manipulador com os mocks
    produto = manipular_atualizar_produto(comando, repositorio_mock, barramento_mock)

    # Asserções para verificar comportamento esperado
    repositorio_mock.salvar_produto.assert_called_once_with(produto)
    barramento_mock.publicar_produto.assert_called_once()
    assert produto.id == "prod1"
    assert produto.nome == "Produto 1 Atualizado"
    assert produto.descricao == "Nova Descrição"
    assert produto.preco == 60.0
    assert produto.quantidade_estoque == 150