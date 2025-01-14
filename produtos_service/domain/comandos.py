from dataclasses import dataclass
from typing import List, Dict
import uuid

class AdicionarProdutoComando:
    def __init__(self, nome, descricao, preco, quantidade_estoque, id=None):
        self.id = id or str(uuid.uuid4())
        self.nome = nome
        self.descricao = descricao
        self.preco = preco
        self.quantidade_estoque = quantidade_estoque

@dataclass
class AtualizarPrecoProdutoComando:
    id: str
    novo_preco: float

@dataclass
class RemoverProdutoComando:
    id: str

@dataclass
class AtualizarProdutoComando:
    id: str
    nome: str
    descricao: str
    preco: float
    quantidade_estoque: int

@dataclass
class CriarPedidoComando:
    """
    Comando para criar um novo pedido.
    """
    id_pedido: str
    id_cliente: str
    itens: List[Dict[str, int]]  # Lista de itens no formato {"id": str, "quantidade": int}

@dataclass
class AtualizarStatusPedidoComando:
    """
    Comando para atualizar o status de um pedido.
    """
    id_pedido: str
    novo_status: str