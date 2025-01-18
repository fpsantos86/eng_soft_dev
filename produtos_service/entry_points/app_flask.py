from camada_servico.notificador_teams import NotificadorTeams
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
CORS(app, resources={r"/*": {"origins": "*"}})

api = Api(app, 
          title="API do Catálogo de Produtos", 
          version="1.0", 
          description="Documentação da API do Catálogo", 
          prefix="/api/produtos")

ns_produtos = api.namespace("", description="Operações relacionadas aos produtos")

produto_model = api.model("Produto", {
    "id": fields.String(  
        required=False,  
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

WEBHOOK_URL = "https://fiapcom.webhook.office.com/webhookb2/62c739a1-e669-4fb7-aa95-b994ed843e16@11dbbfe2-89b8-4549-be10-cec364e59551/IncomingWebhook/d655a315f1b54d758d28c5e30c1b84b1/f5db9e54-1a82-4b45-a6a6-1e5c29ccd23a/V2pxNBVdSm-GPK89NhSO1yz6-BzLF9HoQbYQ2IDgJ9bhU1"
# Instância do TeamsNotifier
notificador = NotificadorTeams(WEBHOOK_URL)

@ns_produtos.route("/<string:id>", strict_slashes=False)
class ProdutoResource(Resource):
    @ns_produtos.doc("consultar_produto")
    def get(self, id):
        consulta = ConsultarDetalhesProduto(id=id)
        repositorio = RepositorioConsultaMongoDB()
        try:
            produto = manipular_consultar_detalhes_produto(consulta, repositorio)
            if produto:
                return make_response(jsonify(produto), 200)
            else:
                return make_response(jsonify({"message": "Produto não encontrado"}), 404)
        except Exception as e:
            return make_response(jsonify({"message": str(e)}), 500)

    @ns_produtos.doc("atualizar_produto")
    @ns_produtos.expect(produto_model_atualizacao)
    def put(self, id):
        dados = request.json
        comando = AtualizarProdutoComando(
            id=id,
            nome=dados["nome"],
            descricao=dados["descricao"],
            preco=dados["preco"],
            quantidade_estoque=dados["quantidade_estoque"]
        )
        
        repositorio = RepositorioProduto()
        barramento = BarramentoMensagens()
        barramento.configurar_exchange("produtos_eventos", "direct")
        barramento.configurar_fila("produtos_eventos", "atualizacao_produto", "produto.atualizacao")
        produto = manipular_atualizar_produto(comando, repositorio, barramento)
        
        notificador.enviar_mensagem(title="Produto Editado",
                                    text=f"O produto com ID {id} foi atualizado para '{dados}'.",
                                    theme_color="FFFF00")
        
        return make_response(produto.to_dict(), 200)
    
    @ns_produtos.doc("remover_produto")
    def delete(self, id):
        
        repositorioReader = RepositorioConsultaMongoDB()
        produto = repositorioReader.obter_por_id(id)
        
        if not produto:
            return make_response(jsonify({"message": "Produto não encontrado"}), 404)
        
        comando = RemoverProdutoComando(id=id)
        barramento = BarramentoMensagens()
        barramento.configurar_exchange("produtos_eventos", "direct")
        barramento.configurar_fila("produtos_eventos", "exclusao_produto", "produto.exclusao")
        repositorio = RepositorioProduto()
        manipular_excluir_produto(comando, repositorio, barramento)
        
        notificador.enviar_mensagem( title="Produto Deletado",
                                        text=f"O produto com ID {id} foi deletado do sistema.",
                                        theme_color="FF0000")
        
        return {"message": "Produto removido com sucesso"}, 200

@ns_produtos.route("/", strict_slashes=False)
class ProdutoListaResource(Resource):
    @ns_produtos.expect(produto_model)
    @ns_produtos.doc("adicionar_produto")
    def post(self):
        dados = request.json
        comando = AdicionarProdutoComando(
            nome=dados["nome"],
            descricao=dados["descricao"],
            preco=dados["preco"],
            quantidade_estoque=dados["quantidade_estoque"],
        )
        repositorio = RepositorioProduto()
        barramento = BarramentoMensagens()
        barramento.configurar_exchange("produtos_eventos", "direct")
        barramento.configurar_fila("produtos_eventos", "inclusao_produto", "produto.criacao")
        produto = manipular_adicionar_produto(comando, repositorio, barramento)
        
        notificador.enviar_mensagem(title="Produto Incluído",
                                    text=f"O produto '{dados}' foi incluído no sistema.",
                                    theme_color="00FF00")
    
        return make_response(produto.to_dict(), 201)

    @ns_produtos.doc("listar_produtos")
    def get(self):
        filter_param = request.args.get("filter", "{}")
        range_param = request.args.get("range", "[0,9]")
        sort_param = request.args.get("sort", '["id", "ASC"]')

        import json
        filter_param = json.loads(filter_param)
        range_param = json.loads(range_param)
        sort_param = json.loads(sort_param)

        start, end = range_param
        sort_field, sort_order = sort_param

        repositorio = RepositorioConsultaMongoDB()
        produtos = repositorio.listar_todos()

        produtos = sorted(produtos, key=lambda x: x.get(sort_field), reverse=(sort_order == "DESC"))

        produtos_paginados = produtos[start:end + 1]

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
        

        return make_response(jsonify({"data": produtos_formatados, "total": len(produtos)}), 200)

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response