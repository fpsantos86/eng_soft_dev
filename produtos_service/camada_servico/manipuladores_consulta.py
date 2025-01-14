from adapters.repositorio import RepositorioPedido
from adapters.repositorio_mongo import RepositorioConsultaMongoDB
from domain.consultas import ConsultarDetalhesPedido, ConsultarDetalhesProduto, ListarPedidosCliente
from domain.eventos import ProdutoAdicionadoEvento

def manipular_consultar_detalhes_pedido(consulta: ConsultarDetalhesPedido, repositorio):
    pedido = repositorio.obter(consulta.id_pedido)
    if not pedido:
        raise ValueError(f"Pedido com ID {consulta.id_pedido} não encontrado.")
    return {
        "id_pedido": pedido.id_pedido,
        "id_cliente": pedido.id_cliente,
        "status": pedido.status,
        "itens": [{"id_produto": item.id_produto, "quantidade": item.quantidade} for item in pedido.itens],
    }

def manipular_listar_pedidos_cliente(consulta: ListarPedidosCliente, repositorio: RepositorioPedido):
    pedidos = repositorio.listar_por_cliente(consulta.id_cliente)
    return [
        {
            "id_pedido": pedido.id_pedido,
            "status": pedido.status,
            "quantidade_itens": len(pedido.itens),
        }
        for pedido in pedidos
    ]
def serializar_mongo_objeto(obj):
    """Converte o campo _id de ObjectId para string."""
    if "_id" in obj:
        obj["_id"] = str(obj["_id"])
    return obj
def manipular_consultar_detalhes_produto(consulta: ConsultarDetalhesProduto, repositorio: RepositorioConsultaMongoDB):
    """
    Manipulador para consultar os detalhes de um produto.
    :param consulta: Instância de ConsultarDetalhesProduto contendo os dados da consulta.
    :param repositorio: Objeto do repositório que fornece os dados.
    :return: Dicionário contendo os detalhes do produto.
    """
    produto = repositorio.obter_por_id(consulta.id_produto)

    if not produto:
        raise ValueError(f"Produto com ID {consulta.id_produto} não encontrado.")

    produtoDto = {
        "id_produto": produto.get("id_produto"),
        "nome": produto.get("nome"),
        "descricao": produto.get("descricao"),
        "preco": produto.get("preco"),
        "quantidade_estoque": produto.get("quantidade_estoque")
    }
    
    return produtoDto

    
def consumir_evento_produto_adicionado(evento: ProdutoAdicionadoEvento, repositorio_mongo: RepositorioConsultaMongoDB):
    """
    Consome o evento de produto adicionado e grava no MongoDB.
    """
    produto = {
        "id_produto": evento.id_produto,
        "nome": evento.nome,
        "descricao": evento.descricao,
        "preco": evento.preco,
        "quantidade_estoque": evento.quantidade_estoque,
    }
    repositorio_mongo.salvar(produto)