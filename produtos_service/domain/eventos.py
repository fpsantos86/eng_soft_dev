from dataclasses import dataclass
from typing import List

@dataclass
class ProdutoAdicionadoEvento:
    def __init__(self, id_produto, nome, descricao, preco, quantidade_estoque):
        self.id_produto = id_produto
        self.nome = nome
        self.descricao = descricao
        self.preco = preco
        self.quantidade_estoque = quantidade_estoque
    
    def to_dict(self):
        return {
            "id_produto": self.id_produto,
            "nome": self.nome,
            "descricao": self.descricao,
            "preco": self.preco,
            "quantidade_estoque": self.quantidade_estoque,
        }

@dataclass
class PrecoProdutoAtualizadoEvento:
    id_produto: str
    preco_antigo: float
    preco_novo: float

@dataclass
class ProdutoRemovidoEvento:
    id_produto: str
    
    
@dataclass
class PedidoCriadoEvento:
    """
    Evento disparado quando um pedido é criado.
    """
    id_pedido: str
    id_cliente: str
    itens: List[dict]  # Lista de itens no formato {"id_produto": str, "quantidade": int}

    def __repr__(self):
        return (
            f"PedidoCriadoEvento("
            f"id_pedido={self.id_pedido}, id_cliente={self.id_cliente}, itens={self.itens})"
        )    

@dataclass
class PrecoProdutoAtualizado:
    def __init__(self, id_produto, novo_preco):
        self.id_produto = id_produto
        self.novo_preco = novo_preco

    def to_dict(self):
        return {
            "id_produto": self.id_produto,
            "novo_preco": self.novo_preco
        }

@dataclass
class StatusPedidoAtualizadoEvento:
    """
    Evento disparado quando o status de um pedido é atualizado.
    """
    id_pedido: str
    status_anterior: str
    status_atual: str