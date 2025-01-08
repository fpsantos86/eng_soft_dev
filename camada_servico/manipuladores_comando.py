from adapters.repositorio import RepositorioPedido, RepositorioProduto
from domain.comandos import AdicionarProdutoComando, AtualizarPrecoProdutoComando
from domain.comandos import CriarPedidoComando, AtualizarStatusPedidoComando
from domain.eventos import PedidoCriadoEvento, ProdutoAdicionadoEvento
from domain.modelo import Produto
from camada_servico.servicos import ServicoProduto, ServicoPedido
from camada_servico.barramento_mensagens import BarramentoMensagens



def manipular_adicionar_produto(comando: AdicionarProdutoComando, repositorio: RepositorioProduto, barramento: BarramentoMensagens):
    """
    Manipula o comando para adicionar um novo produto.
    """
    produto = Produto(
        id_produto=comando.id_produto,
        nome=comando.nome,
        descricao=comando.descricao,
        preco=comando.preco,
        quantidade_estoque=comando.quantidade_estoque,
    )
    repositorio.salvar_produto(produto)
    
    # Criar o evento
    evento = ProdutoAdicionadoEvento(
        id_produto=produto.id_produto,
        nome=produto.nome,
        descricao =produto.descricao,
        preco=produto.preco,
        quantidade_estoque=produto.quantidade_estoque
    )

    
    # Publicar o evento no barramento
    barramento.publicar("eventos_produtos", evento)


def manipular_atualizar_preco_produto(comando: AtualizarPrecoProdutoComando, servico: ServicoProduto):
    """
    Manipula o comando para atualizar o preço de um produto.
    """
    servico.atualizar_preco(comando.id_produto, comando.novo_preco)


def manipular_criar_pedido(
    comando: CriarPedidoComando, 
    servico: ServicoPedido, 
    barramento: BarramentoMensagens
):
    """
    Manipula o comando para criar um novo pedido.
    """
    pedido = servico.criar_pedido(comando.id_pedido, comando.id_cliente, comando.itens)
    
    # Criar o evento relacionado ao pedido
    evento = PedidoCriadoEvento(
        id_pedido=pedido.id_pedido,
        id_cliente=pedido.id_cliente,
        itens=[
            {"id_produto": item.id_produto, "quantidade": item.quantidade} 
            for item in pedido.itens
        ]
    )
    
    # Publicar o evento no barramento
    barramento.publicar("eventos_pedidos", evento)


def manipular_atualizar_status_pedido(
    comando: AtualizarStatusPedidoComando, 
    servico: ServicoPedido
):
    """
    Manipula o comando para atualizar o status de um pedido.
    """
    servico.atualizar_status(
        id_pedido=comando.id_pedido,
        novo_status=comando.novo_status
    )
