from database.db_manager import db
from core.logger import log_erro

class DashboardModel:
    @staticmethod
    def get_total_clientes():
        # Conta quantos clientes existem no banco
        try:
            resultado = db.buscar_todos('select count(*) from clientes')
            return resultado[0] if resultado else 0
        except Exception as e:
            log_erro('Erro ao contar clientes', e)
            return 0
    
    @staticmethod
    def get_os_pendentes():
        # Conta Os que não estão concluidas
        try:
            # Consideramos pendente tudo que não é 'Concluído' ou 'Cancelado'
            query = "select count(*) from servicos where status not in ('Concluído', 'Cancelado')"
            resultado = db.buscar_um(query)
            return resultado[0] if resultado else 0
        except Exception as e:
            log_erro('Erro ao contar OS pendentes', e)
            return 0
        
    @staticmethod
    def get_faturamento_total():
        # Soma o valor das OS Concluidas
        try:
            query = "select sum(valor) from servicos where status = 'Concluidos'"
            resultado = db.buscar_um(query)
            # Se for None (Nenhuma Venda), retorna 0.0
            return resultado[0] if resultado[0] else 0.0
        except Exception as e:
            log_erro('Erro ao somar faturamento', e)
            return 0.0
    
    @staticmethod
    def get_ultimas_atividades():
        """Pega as 10 últimas OS para a tabela do Dashboard"""
        try:
            query = """
            SELECT data_entrada, cliente_nome, equipamento, valor, status 
            FROM servicos 
            ORDER BY id DESC LIMIT 10
            """
            return db.buscar_todos(query)
        except Exception as e:
            log_erro("Erro ao buscar últimas atividades", e)
            return []
    
    @staticmethod
    def get_taxa_conclusao():
        """Retorna a porcentagem de OS Concluídas vs Total"""
        try:
            total = db.buscar_um("SELECT COUNT(*) FROM servicos")[0]
            concluidas = db.buscar_um("SELECT COUNT(*) FROM servicos WHERE status = 'Concluído'")[0]
            
            if total == 0: return 0
            return int((concluidas / total) * 100)
        except:
            return 0

    @staticmethod
    def get_progresso_meta(meta_mensal=5000):
        """Retorna quanto % do faturamento foi atingido baseado na meta"""
        faturamento = DashboardModel.get_faturamento_total()
        if meta_mensal == 0: return 0
        
        porcentagem = int((faturamento / meta_mensal) * 100)
        return min(porcentagem, 100) # Trava em 100% pra não estourar o gráfico