from adapters.orm import Base, engine

def criar_tabelas():
    """
    Cria todas as tabelas no banco de dados com base nos modelos definidos no ORM.
    """
    print("Criando tabelas no banco de dados...")
    Base.metadata.create_all(bind=engine)
    print("Tabelas criadas com sucesso!")

if __name__ == "__main__":
    criar_tabelas()
