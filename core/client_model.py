from database.db_manager import db
from core.logger import log_erro

class ClienteModel:
    
    @staticmethod
    def adicionar(nome, cpf, tel, email, cep, logradouro, numero, bairro, cidade, uf):
        # Atualizamos a Query para incluir endereco (Rua) e numero
        query = """
        INSERT INTO clientes (nome, cpf_cnpj, telefone, email, cep, endereco, numero, bairro, cidade, uf) 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        try:
            db.executar_query(query, (nome, cpf, tel, email, cep, logradouro, numero, bairro, cidade, uf))
            return True
        except Exception as e:
            log_erro("Erro ao adicionar cliente", e)
            return False

    @staticmethod
    def buscar_todos():
        query = "SELECT id, nome, cpf_cnpj, telefone, cidade, email FROM clientes ORDER BY id DESC"
        return db.buscar_todos(query)
    
    @staticmethod
    def buscar_por_nome(termo):
        termo = f'%{termo}%'
        query = """
                SELECT id, nome, cpf_cnpj, telefone, cidade, email
                FROM clientes
                WHERE nome LIKE ? OR cpf_cnpj LIKE ?
                """
        return db.buscar_todos(query, (termo, termo))