from dataclasses import dataclass

@dataclass
class ConsultarDetalhesProduto:
    id_produto: str

@dataclass
class ListarProdutos:
    categoria: str = None  # Filtrar por categoria (opcional)

@dataclass
class ConsultarDetalhesPedido:
    """
    Consulta para obter os detalhes de um pedido específico.
    """
    id_pedido: str


@dataclass
class ListarPedidosCliente:
    """
    Consulta para listar todos os pedidos de um cliente.
    """
    id_cliente: str
    
@dataclass
class ConsultarDetalhesProduto:
    """
    Representa uma consulta para obter detalhes de um produto.
    """
    id_produto: str
    