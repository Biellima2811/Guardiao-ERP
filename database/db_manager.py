import sqlite3
import os

class DatabaseManager:
    def __init__(self, db_name="guardiao.db"):
        # Garante que a pasta data existe
        if not os.path.exists("data"):
            os.makedirs("data")
            
        self.db_path = os.path.join("data", db_name)
        self.inicializar_tabelas()

    def get_conexao(self):
        """Retorna uma conexão segura com o banco"""
        return sqlite3.connect(self.db_path)

    def inicializar_tabelas(self):
        """Cria as tabelas essenciais se não existirem"""
        sql_usuarios = """
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario TEXT UNIQUE NOT NULL,
            senha_hash TEXT NOT NULL,
            nivel TEXT DEFAULT 'operador',
            ativo INTEGER DEFAULT 1
        );
        """
        
        sql_clientes = """
        CREATE TABLE IF NOT EXISTS clientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            cpf_cnpj TEXT,
            telefone TEXT,
            endereco TEXT,
            data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
        
        self.executar_query(sql_usuarios)
        self.executar_query(sql_clientes)
        
        # Cria um usuário ADMIN padrão se não existir (para o primeiro acesso)
        # A senha será definida via sistema de segurança depois
        pass

    def executar_query(self, query, parametros=()):
        """
        Executa uma query de forma segura (evita SQL Injection)
        Use: db.executar_query("INSERT INTO...", (valor1, valor2))
        """
        try:
            with self.get_conexao() as conn:
                cursor = conn.cursor()
                cursor.execute(query, parametros)
                conn.commit()
                return cursor
        except Exception as e:
            print(f"ERRO CRÍTICO NO BANCO: {e}")
            return None

    def buscar_todos(self, query, parametros=()):
        """Retorna todos os resultados de uma busca"""
        with self.get_conexao() as conn:
            cursor = conn.cursor()
            cursor.execute(query, parametros)
            return cursor.fetchall()

    def buscar_um(self, query, parametros=()):
        """Retorna apenas um resultado (ex: login)"""
        with self.get_conexao() as conn:
            cursor = conn.cursor()
            cursor.execute(query, parametros)
            return cursor.fetchone()

# Instância global para ser usada no sistema
db = DatabaseManager()