from flask import Flask, json, make_response, request, jsonify, send_from_directory
from flask_cors import CORS
from flask_restx import Api, Resource, fields
from adapters import repositorio_mongo
from camada_servico.barramento_mensagens import BarramentoMensagens
from camada_servico.servicos import ServicoProduto
from config import RABBITMQ_URL
from camada_servico.manipuladores_comando import manipular_adicionar_produto,  manipular_atualizar_produto, manipular_excluir_produto
from camada_servico.manipuladores_consulta import manipular_consultar_detalhes_produto
from domain.consultas import ConsultarDetalhesProduto
from domain.comandos import AdicionarProdutoComando, RemoverProdutoComando, AtualizarProdutoComando
from adapters.repositorio_mongo import RepositorioConsultaMongoDB
from adapters.repositorio import RepositorioProduto
import logging

from domain.eventos import ProdutoAtualizadoEvento, ProdutoRemovidoEvento

logging.basicConfig()
LOGGER = logging.getLogger("reprod-case")
LOGGER.setLevel(logging.DEBUG)
LOGGER.info("Created LOGGER")
logging.getLogger('flask_cors').level = logging.DEBUG

app = Flask(__name__)
# Adicione a configuração de CORS
CORS(app, resources={r"/*": {"origins": "http://localhost:3000/"}})  # Permite todas as origens

# Adicione o prefixo /api/produtos
api = Api(app, 
          title="API do Catálogo de Produtos", 
          version="1.0", 
          description="Documentação da API do Catálogo", 
          prefix="/api/produtos")

# Modelo de produto para o Swagger
produto_model = api.model("Produto", {
    "id": fields.String(  # Alterado de id para id
        required=False,  # Não obrigatório
        description="ID do produto",
        example="123e4567-e89b-12d3-a456-426614174000"
    ),
    "nome": fields.String(
        required=True,
        description="Nome do produto",
        example="Produto Exemplo"
    ),
    "descricao": fields.String(
        required=True,
        description="Descrição do produto",
        example="Descrição do produto exemplo"
    ),
    "preco": fields.Float(
        required=True,
        description="Preço do produto",
        example=99.99
    ),
    "quantidade_estoque": fields.Integer(
        required=True,
        description="Quantidade em estoque",
        example=10
    )
})

produto_model_atualizacao = api.model("Produto", {
    "nome": fields.String(
        required=True,
        description="Nome do produto",
        example="Produto Exemplo"
    ),
    "descricao": fields.String(
        required=True,
        description="Descrição do produto",
        example="Descrição do produto exemplo"
    ),
    "preco": fields.Float(
        required=True,
        description="Preço do produto",
        example=99.99
    ),
    "quantidade_estoque": fields.Integer(
        required=True,
        description="Quantidade em estoque",
        example=10
    )
})



# Namespace para organizar os endpoints
ns_produtos = api.namespace("", description="Operações relacionadas aos produtos")

@ns_produtos.route("/<string:id>", strict_slashes=False)  # Alterado de id para id
class ProdutoResource(Resource):
    @ns_produtos.doc("consultar_produto")
    def get(self, id):  # Alterado de id para id
        """
        Retorna os detalhes de um produto pelo ID.
        """
        consulta = ConsultarDetalhesProduto(id=id)  # Alterado de id para id
        # Inicializando o repositório
        repositorio = RepositorioConsultaMongoDB()
        produto = manipular_consultar_detalhes_produto(consulta, repositorio)
        return make_response(jsonify(produto), 200)

    @ns_produtos.doc("atualizar_produto")
    @ns_produtos.expect(produto_model_atualizacao)
    def put(self, id):  # Alterado de id para id
        """
        Atualiza todos os detalhes de um produto pelo ID.
        """
        dados = request.json
        comando = AtualizarProdutoComando(
            id=id,  # Alterado de id para id
            nome=dados["nome"],
            descricao=dados["descricao"],
            preco=dados["preco"],
            quantidade_estoque=dados["quantidade_estoque"]
        )
        # Inicializando o repositório
        repositorio = RepositorioProduto()

        # Publicar evento de atualização
        barramento = BarramentoMensagens()
        barramento.configurar_exchange("atualizacao_produto", "direct")
        barramento.configurar_fila("atualizacao_produto", "atualizacao_produto", "produto_key")
        produto = manipular_atualizar_produto(comando, repositorio, barramento)

        return make_response(produto.to_dict(), 200)
    

    @ns_produtos.doc("remover_produto")
    def delete(self, id):  # Alterado de id para id
        """
        Remove um produto pelo ID.
        """
        comando = RemoverProdutoComando(id=id) 
        
        # Inicializando o repositório
        repositorio = RepositorioProduto()
        barramento = BarramentoMensagens()
        barramento.configurar_exchange("exclusao_produto", "direct")
        barramento.configurar_fila("exclusao_produto", "exclusao_produto", "produto_key")
        manipular_excluir_produto(comando, repositorio, barramento)
        
        return {"message": "Produto removido com sucesso"}, 200

@ns_produtos.route("/", strict_slashes=False)
class ProdutoListaResource(Resource):
    @ns_produtos.expect(produto_model)
    @ns_produtos.doc("adicionar_produto")
    def post(self):
        """
        Adiciona um novo produto ao catálogo.
        """
        dados = request.json
        comando = AdicionarProdutoComando(
            nome=dados["nome"],
            descricao=dados["descricao"],
            preco=dados["preco"],
            quantidade_estoque=dados["quantidade_estoque"],
        )
        # Inicializando o repositório
        repositorio = RepositorioProduto()
        barramento = BarramentoMensagens()
        barramento.configurar_exchange("inclusao_produto", "direct")
        barramento.configurar_fila("inclusao_produto", "inclusao_produto", "produto_key")
        produto = manipular_adicionar_produto(comando, repositorio, barramento)
        return make_response(produto.to_dict(), 201)

    @ns_produtos.doc("listar_produtos")
    def get(self):
        """
        Retorna a lista de produtos filtrada, paginada e ordenada.
        """
        # Obter os parâmetros da query string
        filter_param = request.args.get("filter", "{}")
        range_param = request.args.get("range", "[0,9]")
        sort_param = request.args.get("sort", '["id", "ASC"]')

        # Converter os parâmetros de string JSON para objetos Python
        import json
        filter_param = json.loads(filter_param)
        range_param = json.loads(range_param)
        sort_param = json.loads(sort_param)

        # Desestruturar os parâmetros
        start, end = range_param  # Indices para paginação
        sort_field, sort_order = sort_param  # Campo e ordem para ordenação

        # Consultar o repositório
        repositorio = RepositorioConsultaMongoDB()
        produtos = repositorio.listar_todos()

        # Aplicar ordenação
        produtos = sorted(produtos, key=lambda x: x.get(sort_field), reverse=(sort_order == "DESC"))

        # Aplicar paginação
        produtos_paginados = produtos[start:end + 1]

        # Formatar os produtos
        produtos_formatados = [
            {
                "id": produto["id"],
                "nome": produto["nome"],
                "descricao": produto["descricao"],
                "preco": produto["preco"],
                "quantidade_estoque": produto["quantidade_estoque"]
            }
            for produto in produtos_paginados
        ]

        # Retornar no formato esperado pelo React-Admin
        return make_response(jsonify({"data": produtos_formatados, "total": len(produtos)}), 200)

@app.after_request
def after_request(response):
    
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')

    return response