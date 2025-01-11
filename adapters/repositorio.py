from adapters.orm import SessionLocal, Pedido as ORMPedido, ItemPedido as ORMItemPedido, Produto as ORMProduto
from domain.modelo import Pedido, ItemPedido, Produto


class RepositorioPedido:
    def __init__(self):
        self.session = SessionLocal()

    def salvar_pedido(self, pedido: Pedido):
        """
        Converte um objeto de domínio em uma entidade ORM e salva no banco.
        """
        try:
            orm_pedido = ORMPedido(
                id_pedido=pedido.id_pedido,
                id_cliente=pedido.id_cliente,
                status=pedido.status
            )
            self.session.add(orm_pedido)

            for item in pedido.itens:
                orm_item = ORMItemPedido(
                    id_pedido=pedido.id_pedido,
                    id_produto=item.id_produto,
                    quantidade=item.quantidade,
                    preco=item.preco
                )
                self.session.add(orm_item)

            self.session.commit()
        except Exception as e:
            self.session.rollback()
            raise e

    def salvar(self, entidade):
        """
        Salva ou atualiza uma entidade no banco de dados.
        """
        try:
            self.session.merge(entidade)
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            raise e

    def obter_pedido_por_id(self, id_pedido: str) -> Pedido:
        """
        Busca um pedido no banco e retorna como objeto de domínio.
        """
        orm_pedido = self.session.query(ORMPedido).filter_by(id_pedido=id_pedido).first()
        if not orm_pedido:
            return None

        itens = [
            ItemPedido(
                id_produto=orm_item.id_produto,
                quantidade=orm_item.quantidade,
                preco=orm_item.preco
            )
            for orm_item in orm_pedido.itens
        ]

        return Pedido(
            id_pedido=orm_pedido.id_pedido,
            id_cliente=orm_pedido.id_cliente,
            itens=itens,
            status=orm_pedido.status
        )

    def listar_todos_pedidos(self):
        """
        Retorna todos os pedidos no banco.
        """
        orm_pedidos = self.session.query(ORMPedido).all()
        pedidos = []
        for orm_pedido in orm_pedidos:
            itens = [
                ItemPedido(
                    id_produto=orm_item.id_produto,
                    quantidade=orm_item.quantidade,
                    preco=orm_item.preco
                )
                for orm_item in orm_pedido.itens
            ]
            pedidos.append(
                Pedido(
                    id_pedido=orm_pedido.id_pedido,
                    id_cliente=orm_pedido.id_cliente,
                    itens=itens,
                    status=orm_pedido.status
                )
            )
        return pedidos

    def excluir_pedido(self, id_pedido: str):
        """
        Exclui um pedido do banco pelo ID.
        """
        try:
            orm_pedido = self.session.query(ORMPedido).filter_by(id_pedido=id_pedido).first()
            if orm_pedido:
                self.session.delete(orm_pedido)
                self.session.commit()
        except Exception as e:
            self.session.rollback()
            raise e


class RepositorioProduto:
    def __init__(self):
        self.session = SessionLocal()

    def salvar_produto(self, produto: Produto):
        """
        Salva ou atualiza um produto no banco de dados.
        """
        try:
            orm_produto = ORMProduto(
                id_produto=produto.id_produto,
                nome=produto.nome,
                descricao=produto.descricao,
                preco=produto.preco,
                quantidade_estoque=produto.quantidade_estoque
            )
            self.session.merge(orm_produto)
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            raise e


    def obter_produto_por_id(self, id_produto: str) -> Produto:
        """
        Retorna um produto pelo ID.
        """
        orm_produto = self.session.query(ORMProduto).filter_by(id_produto=id_produto).first()
        if not orm_produto:
            return None

        return Produto(
            id_produto=orm_produto.id_produto,
            nome=orm_produto.nome,
            descricao=orm_produto.descricao,
            preco=orm_produto.preco,
            quantidade_estoque=orm_produto.quantidade_estoque
        )

    def listar_todos_produtos(self):
        """
        Lista todos os produtos no banco de dados.
        """
        orm_produtos = self.session.query(ORMProduto).all()
        return [
            Produto(
                id_produto=orm_produto.id_produto,
                nome=orm_produto.nome,
                descricao=orm_produto.descricao,
                preco=orm_produto.preco,
                quantidade_estoque=orm_produto.quantidade_estoque
            )
            for orm_produto in orm_produtos
        ]

    def excluir_produto(self, id_produto: str):
        """
        Exclui um produto pelo ID.
        """
        try:
            orm_produto = self.session.query(ORMProduto).filter_by(id_produto=id_produto).first()
            if orm_produto:
                self.session.delete(orm_produto)
                self.session.commit()
        except Exception as e:
            self.session.rollback()
            raise e
