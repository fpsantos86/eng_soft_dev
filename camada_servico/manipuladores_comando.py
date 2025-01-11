from adapters.repositorio import RepositorioPedido, RepositorioProduto
from domain.comandos import AdicionarProdutoComando, AtualizarPrecoProdutoComando
from domain.comandos import CriarPedidoComando, AtualizarStatusPedidoComando, AtualizarProdutoComando
from domain.eventos import PedidoCriadoEvento, ProdutoAdicionadoEvento
from domain.modelo import Produto
from camada_servico.servicos import ServicoProduto, ServicoPedido
from camada_servico.barramento_mensagens import BarramentoMensagens

from domain.comandos import AtualizarPrecoProdutoComando
from domain.eventos import PrecoProdutoAtualizado
from domain.eventos import PrecoProdutoAtualizadoEvento


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
    barramento.publicar_produto("eventos_produtos", "produto_key",evento)


def manipular_atualizar_preco_produto(comando: AtualizarPrecoProdutoComando, servico: ServicoProduto):
    """
    Manipula o comando de atualização de preço do produto.
    """
    # Atualiza o preço do produto no repositório
    produto = servico.repositorio.obter_produto_por_id(comando.id_produto)
    if (produto):
        preco_antigo, preco_atualizado = produto.atualizar_preco(comando.novo_preco)
        servico.repositorio.salvar_produto(produto)
        
        # Cria um evento de preço atualizado
        evento = PrecoProdutoAtualizadoEvento(
            id_produto=comando.id_produto,
            preco_antigo=preco_antigo,
            preco_novo=preco_atualizado
        )
        
        # Publica o evento no barramento de mensagens
        servico.barramento_eventos.publicar(evento)
    else:
        raise ValueError(f"Produto com ID {comando.id_produto} não encontrado.")


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


def manipular_atualizar_produto(comando: AtualizarProdutoComando, servico: ServicoProduto):
    """
    Manipula o comando de atualização de todos os detalhes do produto.
    """
    produto = servico.repositorio.obter_produto_por_id(comando.id_produto)
    if produto:
        produto.atualizar_detalhes(
            nome=comando.nome,
            descricao=comando.descricao,
            preco=comando.preco,
            quantidade_estoque=comando.quantidade_estoque
        )
        servico.repositorio.salvar_produto(produto)
        
        # Cria um evento de produto atualizado (se necessário)
        # evento = ProdutoAtualizado(...)
        # servico.barramento.publicar_evento(evento)
    else:
        raise ValueError(f"Produto com ID {comando.id_produto} não encontrado.")