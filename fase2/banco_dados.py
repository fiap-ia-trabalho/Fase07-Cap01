import sqlite3

def conectar_banco():
    """
    Módulo de conexão e inicialização do Banco de Dados Relacional (Fase 2).
    Utiliza abordagem in-memory (SQLite) para garantir alta disponibilidade, 
    baixa latência e isolamento durante a execução da Dashboard Streamlit.
    """
    try:
        conn = sqlite3.connect(':memory:')
        cursor = conn.cursor()
        
        # 1. Cria a tabela de Sensores (IoT)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS leituras (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                sensor VARCHAR(50),
                valor REAL,
                data_hora TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # 2. Cria a tabela de Culturas 
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS culturas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome VARCHAR(50),
                espacamento_metros REAL,
                tempo_colheita_dias INTEGER
            )
        ''')

        # 3. 4 culturas da Fase 1 pré-cadastradas no banco
        cursor.execute('SELECT COUNT(*) FROM culturas')
        if cursor.fetchone()[0] == 0:
            culturas_iniciais = [
                ('Soja', 0.45, 120),
                ('Milho', 0.90, 90),
                ('Café', 2.50, 730),
                ('Laranja', 4.00, 365) 
            ]
            cursor.executemany('INSERT INTO culturas (nome, espacamento_metros, tempo_colheita_dias) VALUES (?, ?, ?)', culturas_iniciais)
            conn.commit()

        return "✅ Conexão estabelecida! Tabelas de Sensores e Culturas prontas na memória."
    
    except Exception as e:
        return f"❌ Erro de integridade ao conectar no banco: {e}"

if __name__ == "__main__":
    print("Iniciando rotina de banco de dados...\n")
    print(conectar_banco())