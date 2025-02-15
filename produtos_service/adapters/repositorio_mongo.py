from pymongo import MongoClient
from config import MONGO_URI, MONGO_DB_NAME, MONGO_COLLECTION_NAME
import uuid

class RepositorioConsultaMongoDB:
    def __init__(self):
        self.client = MongoClient(MONGO_URI)
        self.db = self.client[MONGO_DB_NAME]
        self.collection = self.db[MONGO_COLLECTION_NAME]
        
    def salvar(self, produto):
        """
        Salva ou atualiza um produto na coleção.
        """
        produto["id"] = str(uuid.UUID(produto["id"]))
        self.collection.update_one(
            {"id": produto["id"]},  # Filtro
            {"$set": produto},  # Dados a atualizar
            upsert=True  # Insere se não existir
        )

    def obter_por_id(self, id):
        """
        Obtém um produto pelo ID.
        """
        return self.collection.find_one({"id": str(uuid.UUID(id))})

    def listar_todos(self):
        """
        Retorna todos os produtos.
        """
        return list(self.collection.find({},{'_id': False}))

    def excluir(self, id):
        """
        Exclui um produto pelo ID.
        """
        self.collection.delete_one({"id": str(uuid.UUID(id))})
