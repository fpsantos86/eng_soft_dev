import threading
from flask import Flask, json, make_response, request, jsonify
from flask_cors import CORS
from flask_restx import Api, Resource, fields
from adapters import repositorio_mongo
from camada_servico.barramento_mensagens import BarramentoMensagens
from config import RABBITMQ_URL
from camada_servico.manipuladores_comando import manipular_adicionar_produto
from camada_servico.manipuladores_consulta import manipular_consultar_detalhes_produto
from domain.consultas import ConsultarDetalhesProduto
from domain.comandos import AdicionarProdutoComando
from adapters.repositorio_mongo import RepositorioConsultaMongoDB
from adapters.repositorio import RepositorioProduto

from camada_servico.consumidor_eventos import iniciar_consumidor_produtos

app = Flask(__name__)
# Adicione a configuração de CORS
CORS(app, resources={r"/*": {"origins": "*"}})

api = Api(app, title="API do Catálogo de Produtos", version="1.0", description="Documentação da API do Catálogo")

# Namespace para organizar os endpoints
ns_produtos = api.namespace("produtos", description="Operações relacionadas aos produtos")

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
        manipular_adicionar_produto(comando, repositorio,barramento)
        return {"message": "Produto adicionado com sucesso"}, 201

if __name__ == "__main__":
   
     # Inicia o consumidor em outra thread
    consumidor_thread = threading.Thread(target=iniciar_consumidor_produtos,daemon=True)
    consumidor_thread.start()
    # Inicia o Flask na thread principal
    app.run(debug=True)