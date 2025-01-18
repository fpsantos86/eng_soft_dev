from sqlalchemy import Column, String, Float, Integer, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from config import SQLALCHEMY_DATABASE_URI
import uuid

# Base para o mapeamento ORM
Base = declarative_base()

# Configuração do engine e da sessão
engine = create_engine(SQLALCHEMY_DATABASE_URI)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Modelo ORM para a tabela de produtos
class Produto(Base):
    __tablename__ = "produtos"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True, index=True)
    nome = Column(String, nullable=False)
    descricao = Column(String)
    preco = Column(Float, nullable=False)
    quantidade_estoque = Column(Integer, nullable=False)


class Pedido(Base):
    __tablename__ = "pedidos"

    id_pedido = Column(String, primary_key=True, index=True)
    id_cliente = Column(String, nullable=False)
    status = Column(String, default="Pendente")
    itens = relationship("ItemPedido", back_populates="pedido")


class ItemPedido(Base):
    __tablename__ = "itens_pedido"

    id_item = Column(Integer, primary_key=True, autoincrement=True)
    id_pedido = Column(String, ForeignKey("pedidos.id_pedido"), nullable=False)
    id= Column(String, nullable=False)
    quantidade = Column(Integer, nullable=False)
    preco = Column(Float, nullable=False)
    pedido = relationship("Pedido", back_populates="itens")

# Criar as tabelas no banco de dados (se ainda não existirem)
def criar_tabelas():
    Base.metadata.create_all(bind=engine)
