from database.db_manager import db
from core.logger import log_erro, log_info

class OSModel:
    
    @staticmethod
    def salvar(cliente_nome, equipamento, defeito, valor, status, prioridade, tecnico, obs):
        """Salva a OS com todos os detalhes"""
        query = """
        INSERT INTO servicos (cliente_nome, equipamento, defeito, valor, status, prioridade, tecnico, observacoes) 
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """
        try:
            if isinstance(valor, str):
                valor = float(valor.replace("R$", "").replace(",", ".").strip() or 0)
                
            db.executar_query(query, (cliente_nome, equipamento, defeito, valor, status, prioridade, tecnico, obs))
            log_info(f"Nova OS criada para {cliente_nome}")
            return True
        except Exception as e:
            log_erro("Erro ao salvar OS", e)
            return False

    @staticmethod
    def buscar_todos(): # <--- CORREÇÃO: Nome padronizado (era buscar_todas)
        query = "SELECT id, cliente_nome, equipamento, defeito, data_entrada, status, valor, prioridade FROM servicos ORDER BY id DESC"
        return db.buscar_todos(query)
    
    # --- NOVOS MÉTODOS ---
    @staticmethod
    def buscar_pod_id(id_os):
        # Busca todos os detalhes de uma OS especifica para edição
        query = "select * from servicos where id = ?"
        return db.buscar_um(query, (id_os,))
    
    @staticmethod
    def atualizar(id_os, tecnico,status, defeito, valor, obs, laudo):
        # Atualiza os dados da OS
        query = """
                update servicos
                set tecnico=?, status=?, defeito=?, observacoes=?, laudo=?
                where id?"""
        try:
            if isinstance(valor, str):
                valor = float(valor.replace('R$', '').replace(',','.').strip() or 0)
            db.executar_query(query, (tecnico, status, defeito, valor, obs, laudo, id_os))
            log_info(f'OS #{id_os} atualiza com sucesso!')
            return True
        except Exception as e:
            log_erro(f'Erro ao atualizar OS #{id_os}', e)
            return False