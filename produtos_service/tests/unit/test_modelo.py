import pytest
from domain.modelo import Produto

def test_criar_produto():
    produto = Produto(nome="Produto 1", descricao="Descrição do Produto 1", preco=50.0, quantidade_estoque=100, id="prod1")
    assert produto.id == "prod1"
    assert produto.nome == "Produto 1"
    assert produto.descricao == "Descrição do Produto 1"
    assert produto.preco == 50.0
    assert produto.quantidade_estoque == 100

def test_atualizar_preco():
    produto = Produto(nome="Produto 1", descricao="Descrição do Produto 1", preco=50.0, quantidade_estoque=100, id="prod1")
    preco_antigo, preco_novo = produto.atualizar_preco(75.0)
    assert preco_antigo == 50.0
    assert preco_novo == 75.0
    assert produto.preco == 75.0

def test_reduzir_estoque():
    produto = Produto(nome="Produto 1", descricao="Descrição do Produto 1", preco=50.0, quantidade_estoque=100, id="prod1")
    produto.reduzir_estoque(20)
    assert produto.quantidade_estoque == 80

def test_reduzir_estoque_insuficiente():
    produto = Produto(nome="Produto 1", descricao="Descrição do Produto 1", preco=50.0, quantidade_estoque=10, id="prod1")
    with pytest.raises(ValueError, match="Quantidade em estoque insuficiente."):
        produto.reduzir_estoque(20)

def test_atualizar_detalhes():
    produto = Produto(nome="Produto 1", descricao="Descrição do Produto 1", preco=50.0, quantidade_estoque=100, id="prod1")
    produto.atualizar_detalhes(nome="Produto 1 Atualizado", descricao="Nova Descrição", preco=60.0, quantidade_estoque=150)
    assert produto.nome == "Produto 1 Atualizado"
    assert produto.descricao == "Nova Descrição"
    assert produto.preco == 60.0
    assert produto.quantidade_estoque == 150
