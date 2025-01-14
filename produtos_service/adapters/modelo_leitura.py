class ModeloLeituraProduto:
    def __init__(self, conexao_bd):
        self.conexao_bd = conexao_bd

    def obter_resumo_produto(self, id):
        consulta = "SELECT nome, preco FROM produtos WHERE id = %s"
        cursor = self.conexao_bd.cursor()
        cursor.execute(consulta, (id,))
        return cursor.fetchone()
