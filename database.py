import sqlite3

def criar_banco():
    # Conecta à base de dados (cria o ficheiro se não existir)
    conn = sqlite3.connect('gestor.db')
    cursor = conn.cursor()

    # CRIA A TABELA DE PROFESSORES (estrutura)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS professores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            categoria TEXT NOT NULL, -- 'Cultura' ou 'Esporte'
            cpf TEXT,
            cnpj TEXT,
            dados_bancarios TEXT
        );
    ''')

    # CRIA A TABELA DE DOCUMENTOS (estrutura)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS documentos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            professor_id INTEGER NOT NULL,
            mes INTEGER NOT NULL,
            ano INTEGER NOT NULL,
            tipo_documento TEXT NOT NULL,
            caminho_arquivo TEXT NOT NULL,
            nf_numero TEXT,
            nf_data TEXT,
            nf_tipo TEXT,
            nf_valor REAL,
            FOREIGN KEY (professor_id) REFERENCES professores (id)
        );
    ''')

    # CRIA A TABELA DE GASTOS (estrutura)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS gastos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            categoria TEXT NOT NULL,
            ano INTEGER NOT NULL,
            parcela INTEGER NOT NULL,
            descricao TEXT,
            valor REAL
        );
    ''')
    
    # CRIA A TABELA DAS PARCELAS (estrutura)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS parcelas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            categoria TEXT NOT NULL,
            ano INTEGER NOT NULL,
            parcela INTEGER NOT NULL,
            valor_inicial REAL NOT NULL,
            UNIQUE(categoria, ano, parcela)
        );
    ''')

    # CRIA A TABELA DE EMPRÉSTIMOS (estrutura)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS emprestimos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            data_retirada TEXT NOT NULL,
            item TEXT NOT NULL,
            responsavel TEXT NOT NULL,
            data_devolucao TEXT,
            observacoes TEXT
        );
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS eventos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            data TEXT NOT NULL,          -- Formato YYYY-MM-DD
            horario TEXT,                -- Opcional, para a hora do evento
            descricao TEXT NOT NULL
        );
    ''')
    print("Tabelas criadas com sucesso. A base de dados está pronta e vazia.")

    conn.close()

if __name__ == '__main__':
    criar_banco()