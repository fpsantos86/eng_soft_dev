from adapters.repositorio import RepositorioPedido, RepositorioProduto
from domain.comandos import AdicionarProdutoComando, AtualizarPrecoProdutoComando, RemoverProdutoComando
from domain.comandos import CriarPedidoComando, AtualizarStatusPedidoComando, AtualizarProdutoComando
from domain.eventos import PedidoCriadoEvento, ProdutoAdicionadoEvento, ProdutoAtualizadoEvento
from domain.modelo import Produto
from camada_servico.servicos import ServicoProduto, ServicoPedido
from camada_servico.barramento_mensagens import BarramentoMensagens

from domain.comandos import AtualizarPrecoProdutoComando
from domain.eventos import PrecoProdutoAtualizado
from domain.eventos import PrecoProdutoAtualizadoEvento
from domain.eventos import ProdutoRemovidoEvento
import uuid


def manipular_adicionar_produto(comando: AdicionarProdutoComando, repositorio: RepositorioProduto, barramento: BarramentoMensagens):
    """
    Manipula o comando para adicionar um novo produto.
    """
    produto = Produto(
        id=comando.id or str(uuid.uuid4()),  # Alterado de id para id
        nome=comando.nome,
        descricao=comando.descricao,
        preco=comando.preco,
        quantidade_estoque=comando.quantidade_estoque,
    )
    repositorio.salvar_produto(produto)
    
    # Criar o evento
    evento = ProdutoAdicionadoEvento(
        id=produto.id,  # Alterado de id para id
        nome=produto.nome,
        descricao=produto.descricao,
        preco=produto.preco,
        quantidade_estoque=produto.quantidade_estoque
    )

    # Publicar o evento no barramento
    barramento.publicar_produto("produtos_eventos", "produto.criacao", evento)
    
    return produto

def manipular_excluir_produto(comando: RemoverProdutoComando, repositorio: RepositorioProduto, barramento: BarramentoMensagens):
    """
    Manipula o comando para adicionar um novo produto.
    """
    
    repositorio.excluir_produto(comando.id)
    
    # Criar o evento
    evento = ProdutoRemovidoEvento(id=comando.id)
    
    # Publicar o evento no barramento
    barramento.publicar_produto("produtos_eventos", "produto.exclusao", evento)


def manipular_atualizar_produto(comando: AtualizarProdutoComando, repositorio: RepositorioProduto, barramento: BarramentoMensagens):
    """
    Manipula o comando para adicionar um novo produto.
    """
    produto = Produto(
        id=comando.id or str(uuid.uuid4()),  # Alterado de id para id
        nome=comando.nome,
        descricao=comando.descricao,
        preco=comando.preco,
        quantidade_estoque=comando.quantidade_estoque,
    )
    repositorio.salvar_produto(produto)
    
    # Criar o evento
    evento = ProdutoAtualizadoEvento(
        id=produto.id,  # Alterado de id para id
        nome=produto.nome,
        descricao=produto.descricao,
        preco=produto.preco,
        quantidade_estoque=produto.quantidade_estoque
    )
    
    # Publicar o evento no barramento
    barramento.publicar_produto("produtos_eventos", "produto.atualizacao", evento)
    
    return produto



def manipular_atualizar_preco_produto(comando: AtualizarPrecoProdutoComando, servico: ServicoProduto):
    """
    Manipula o comando de atualização de preço do produto.
    """
    # Atualiza o preço do produto no repositório
    produto = servico.repositorio.obter_produto_por_id(comando.id)  # Alterado de id para id
    if (produto):
        preco_antigo, preco_atualizado = produto.atualizar_preco(comando.novo_preco)
        servico.repositorio.salvar_produto(produto)
        
        # Cria um evento de preço atualizado
        evento = PrecoProdutoAtualizadoEvento(
            id=comando.id,  # Alterado de id para id
            preco_antigo=preco_antigo,
            preco_novo=preco_atualizado
        )
        
        # Publica o evento no barramento de mensagens
        servico.barramento_eventos.publicar(evento)
    else:
        raise ValueError(f"Produto com ID {comando.id} não encontrado.")  # Alterado de id para id


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
            {"id": item.id, "quantidade": item.quantidade} 
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

