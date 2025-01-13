from flask import Flask, make_response, request, jsonify, send_from_directory
from flask_cors import CORS
from flask_restx import Api, Resource, fields
from adapters import repositorio_mongo
from camada_servico.barramento_mensagens import BarramentoMensagens
from camada_servico.servicos import ServicoProduto
from config import RABBITMQ_URL
from camada_servico.manipuladores_comando import manipular_adicionar_produto, manipular_atualizar_preco_produto, manipular_atualizar_produto
from camada_servico.manipuladores_consulta import manipular_consultar_detalhes_produto
from domain.consultas import ConsultarDetalhesProduto
from domain.comandos import AdicionarProdutoComando, RemoverProdutoComando, AtualizarProdutoComando
from adapters.repositorio_mongo import RepositorioConsultaMongoDB
from adapters.repositorio import RepositorioProduto

app = Flask(__name__)
# Adicione a configuração de CORS
CORS(app, resources={r"/*": {"origins": "*"}})  # Permite todas as origens

# Adicione o prefixo /api/produtos
api = Api(app, 
          title="API do Catálogo de Produtos", 
          version="1.0", 
          description="Documentação da API do Catálogo", 
          prefix="/api/produtos")

# Namespace para organizar os endpoints
ns_produtos = api.namespace("", description="Operações relacionadas aos produtos")

# Modelo de produto para o Swagger
produto_model = api.model("Produto", {
    "id_produto": fields.String(
        required=True,
        description="ID do produto",
        example="12345"
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

@ns_produtos.route("/<string:id_produto>")
class ProdutoResource(Resource):
    @ns_produtos.doc("consultar_produto")
    def get(self, id_produto):
        """
        Retorna os detalhes de um produto pelo ID.
        """
        consulta = ConsultarDetalhesProduto(id_produto=id_produto)
        # Inicializando o repositório
        repositorio = RepositorioConsultaMongoDB()
        produto = manipular_consultar_detalhes_produto(consulta, repositorio)
        return make_response(jsonify(produto), 200)

    @ns_produtos.doc("atualizar_produto")
    @ns_produtos.expect(produto_model)
    def put(self, id_produto):
        """
        Atualiza todos os detalhes de um produto pelo ID.
        """
        dados = request.json
        comando = AtualizarProdutoComando(
            id_produto=id_produto,
            nome=dados["nome"],
            descricao=dados["descricao"],
            preco=dados["preco"],
            quantidade_estoque=dados["quantidade_estoque"]
        )
        # Inicializando o repositório
        repositorio = RepositorioProduto()
        servico = ServicoProduto(repositorio, BarramentoMensagens())
        manipular_atualizar_produto(comando, servico)
        return {"message": "Produto atualizado com sucesso"}, 200

    @ns_produtos.doc("remover_produto")
    def delete(self, id_produto):
        """
        Remove um produto pelo ID.
        """
        comando = RemoverProdutoComando(id_produto=id_produto)
        # Inicializando o repositório
        repositorio = RepositorioProduto()
        repositorio.excluir_produto(id_produto)
        return {"message": "Produto removido com sucesso"}, 200

@ns_produtos.route("/")
class ProdutoListaResource(Resource):
    @ns_produtos.expect(produto_model)
    @ns_produtos.doc("adicionar_produto")
    def post(self):
        """
        Adiciona um novo produto ao catálogo.
        """
        dados = request.json
        comando = AdicionarProdutoComando(
            id_produto=dados["id_produto"],
            nome=dados["nome"],
            descricao=dados["descricao"],
            preco=dados["preco"],
            quantidade_estoque=dados["quantidade_estoque"],
        )
        # Inicializando o repositório
        repositorio = RepositorioProduto()
        barramento = BarramentoMensagens()
        barramento.configurar_exchange("eventos_produtos", "direct")
        barramento.configurar_fila("eventos_produtos", "eventos_produtos", "produto_key")
        manipular_adicionar_produto(comando, repositorio, barramento)
        return {"message": "Produto adicionado com sucesso"}, 201

    @ns_produtos.doc("listar_produtos")
    def get(self):
        """
        Retorna a lista de todos os produtos.
        """
        # Inicializando o repositório
        repositorio = RepositorioConsultaMongoDB()
        produtos = repositorio.listar_todos()
        
        return make_response(jsonify(produtos), 200)

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response