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
        "itens": [{"id": item.id, "quantidade": item.quantidade} for item in pedido.itens],
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
    if "_id" in obj:
        obj["_id"] = str(obj["_id"])
    return obj
def manipular_consultar_detalhes_produto(consulta: ConsultarDetalhesProduto, repositorio: RepositorioConsultaMongoDB):
   
    produto = repositorio.obter_por_id(consulta.id)

    if not produto:
        raise ValueError(f"Produto com ID {consulta.id} não encontrado.")

    produtoDto = {
        "id": produto.get("id"),
        "nome": produto.get("nome"),
        "descricao": produto.get("descricao"),
        "preco": produto.get("preco"),
        "quantidade_estoque": produto.get("quantidade_estoque")
    }
    
    return produtoDto
