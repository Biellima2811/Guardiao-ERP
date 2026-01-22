from database.db_manager import db
from core.logger import log_erro, log_info

class ProductModel:
    
    @staticmethod
    def _tratar_valor(valor):
        """Método auxiliar para limpar R$ e converter para float"""
        if isinstance(valor, str):
            # Remove R$, tira pontos de milhar e troca vírgula por ponto
            # Ex: "R$ 1.200,50" -> "1200.50"
            return float(valor.replace('R$', '').replace('.', '').replace(',', '.').strip() or 0)
        return valor

    @staticmethod
    def adicionar(nome, codigo, custo, venda, estoque, descricao):
        query = """
                INSERT INTO produtos(nome, codigo, preco_custo, preco_venda, estoque, descricao)
                VALUES (?, ?, ?, ?, ?, ?)
                """
        try:
            # Tratamento robusto
            custo = ProductModel._tratar_valor(custo)
            venda = ProductModel._tratar_valor(venda)
            if isinstance(estoque, str): estoque = int(estoque.strip() or 0)

            db.executar_query(query, (nome, codigo, custo, venda, estoque, descricao))
            log_info(f'✅ - Produto Cadastrado: {nome}')
            return True 
        except Exception as e:
            log_erro(f'⚠️ - Erro ao realizar o cadastro do produto: {nome}', e)
            return False

    @staticmethod
    def buscar_todos():
        # A ordem deve ser exata: id, nome, codigo, estoque, venda, custo
        query = "SELECT id, nome, codigo, estoque, preco_venda, preco_custo FROM produtos ORDER BY nome ASC"
        return db.buscar_todos(query)
    
    @staticmethod
    def atualizar(id_prod, nome, codigo, custo, venda, estoque, descricao):
        query = """
                UPDATE produtos
                SET nome=?, codigo=?, preco_custo=?, preco_venda=?, estoque=?, descricao=?
                WHERE id=?
                """
        try:
            custo = ProductModel._tratar_valor(custo)
            venda = ProductModel._tratar_valor(venda)
            if isinstance(estoque, str): estoque = int(estoque.strip() or 0)
            
            db.executar_query(query, (nome, codigo, custo, venda, estoque, descricao, id_prod))
            log_info(f'✅ - Produto Atualizado: {nome}')
            return True
        except Exception as e:
            log_erro(f'Erro ao atualizar produto: {nome}', e)
            return False

    @staticmethod
    def excluir(id_prod):
        try:
            db.executar_query("DELETE FROM produtos WHERE id=?", (id_prod,))
            return True
        except Exception as e:
            log_erro(f"Erro ao excluir produto:{id_prod}", e)
            return False
            
    @staticmethod
    def buscar_por_id(id_prod):
        return db.buscar_um("SELECT * FROM produtos WHERE id=?", (id_prod,))