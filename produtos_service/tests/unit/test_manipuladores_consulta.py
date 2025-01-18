from unittest.mock import Mock
from domain.consultas import ConsultarDetalhesProduto
from camada_servico.manipuladores_consulta import manipular_consultar_detalhes_produto

def test_manipular_consultar_detalhes_produto():
    repositorio = Mock()
    repositorio.obter_por_id.return_value = {
        "id": "prod1",
        "nome": "Produto 1",
        "descricao": "Descrição do Produto 1",
        "preco": 50.0,
        "quantidade_estoque": 100
    }
    consulta = ConsultarDetalhesProduto(id="prod1")

    resultado = manipular_consultar_detalhes_produto(consulta, repositorio)

    assert resultado == {
        "id": "prod1",
        "nome": "Produto 1",
        "descricao": "Descrição do Produto 1",
        "preco": 50.0,
        "quantidade_estoque": 100
    }
