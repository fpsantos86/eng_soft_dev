from dataclasses import dataclass
from typing import List, Dict

@dataclass
class AdicionarProdutoComando:
    id_produto: str
    nome: str
    descricao: str
    preco: float
    quantidade_estoque: int

@dataclass
class AtualizarPrecoProdutoComando:
    id_produto: str
    novo_preco: float

@dataclass
class RemoverProdutoComando:
    id_produto: str



@dataclass
class CriarPedidoComando:
    """
    Comando para criar um novo pedido.
    """
    id_pedido: str
    id_cliente: str
    itens: List[Dict[str, int]]  # Lista de itens no formato {"id_produto": str, "quantidade": int}

@dataclass
class AtualizarStatusPedidoComando:
    """
    Comando para atualizar o status de um pedido.
    """
    id_pedido: str
    novo_status: str