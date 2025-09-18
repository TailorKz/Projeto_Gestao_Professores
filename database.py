import os
import psycopg2

DATABASE_URL = os.environ.get('DATABASE_URL')

def get_db_connection():
    conn = psycopg2.connect(DATABASE_URL)
    return conn

def criar_tabelas():
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS professores (
                id SERIAL PRIMARY KEY, nome TEXT NOT NULL, categoria TEXT NOT NULL,
                cpf TEXT, cnpj TEXT, dados_bancarios TEXT
            );
            CREATE TABLE IF NOT EXISTS documentos (
                id SERIAL PRIMARY KEY, professor_id INTEGER NOT NULL, mes INTEGER NOT NULL,
                ano INTEGER NOT NULL, tipo_documento TEXT NOT NULL, caminho_arquivo TEXT NOT NULL,
                nf_numero TEXT, nf_data TEXT, nf_tipo TEXT, nf_valor REAL,
                FOREIGN KEY (professor_id) REFERENCES professores (id) ON DELETE CASCADE
            );
            CREATE TABLE IF NOT EXISTS gastos (
                id SERIAL PRIMARY KEY, categoria TEXT NOT NULL, ano INTEGER NOT NULL,
                parcela INTEGER NOT NULL, descricao TEXT, valor REAL
            );
            CREATE TABLE IF NOT EXISTS parcelas (
                id SERIAL PRIMARY KEY, categoria TEXT NOT NULL, ano INTEGER NOT NULL,
                parcela INTEGER NOT NULL, valor_inicial REAL NOT NULL,
                UNIQUE(categoria, ano, parcela)
            );
            CREATE TABLE IF NOT EXISTS emprestimos (
                id SERIAL PRIMARY KEY, data_retirada TEXT NOT NULL, item TEXT NOT NULL,
                responsavel TEXT NOT NULL, data_devolucao TEXT, observacoes TEXT
            );
            CREATE TABLE IF NOT EXISTS eventos (
                id SERIAL PRIMARY KEY, data TEXT NOT NULL, horario TEXT, descricao TEXT NOT NULL
            );
        ''')
        conn.commit()
        cursor.close()
        print("Tabelas verificadas/criadas com sucesso no PostgreSQL.")
    except Exception as e:
        print(f"Erro ao criar tabelas: {e}")
    finally:
        if conn is not None:
            conn.close()