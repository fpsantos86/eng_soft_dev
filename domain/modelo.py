class Produto:
    def __init__(self, id_produto, nome, descricao, preco, quantidade_estoque):
        self.id_produto = id_produto
        self.nome = nome
        self.descricao = descricao
        self.preco = preco
        self.quantidade_estoque = quantidade_estoque

    def atualizar_preco(self, novo_preco):
        if novo_preco <= 0:
            raise ValueError("O preço deve ser maior que zero.")
        preco_antigo = self.preco
        self.preco = novo_preco
        return preco_antigo, novo_preco

    def reduzir_estoque(self, quantidade):
        if self.quantidade_estoque < quantidade:
            raise ValueError("Quantidade em estoque insuficiente.")
        self.quantidade_estoque -= quantidade

class ItemPedido:
    """
    Representa um item dentro de um pedido.
    """
    def __init__(self, id_produto: str, quantidade: int, preco: float):
        self.id_produto = id_produto
        self.quantidade = quantidade
        self.preco = preco  # Adiciona o preço ao item

    def __repr__(self):
        return f"ItemPedido(id_produto={self.id_produto}, quantidade={self.quantidade}, preco={self.preco})"

class Pedido:
    """
    Representa um pedido feito por um cliente.
    """
    def __init__(self, id_pedido: str, id_cliente: str, itens: list[ItemPedido], status: str = "Pendente"):
        self.id_pedido = id_pedido
        self.id_cliente = id_cliente
        self.itens = itens  # Lista de objetos ItemPedido
        self.status = status

    def atualizar_status(self, novo_status: str):
        """
        Atualiza o status do pedido.
        """
        status_anterior = self.status
        self.status = novo_status
        return status_anterior, novo_status

    def calcular_total(self) -> float:
        """
        Calcula o valor total do pedido com base nos itens.
        """
        return sum(item.quantidade * item.preco for item in self.itens)

    def cancelar(self):
        """
        Cancela o pedido, caso ele não esteja concluído.
        """
        if self.status == "Concluído":
            raise ValueError("Não é possível cancelar um pedido já concluído.")
        self.status = "Cancelado"

    def __repr__(self):
        return (f"Pedido(id_pedido={self.id_pedido}, id_cliente={self.id_cliente}, "
                f"status={self.status}, itens={self.itens})")