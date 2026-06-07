import sqlite3

def conectar_banco():
    """Módulo de conexão e inicialização do Banco de Dados Relacional SQLite."""
    try:
        # Cria um banco na memória só para não gerar arquivos extras na máquina de quem testar
        conn = sqlite3.connect(':memory:')
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS leituras (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                sensor VARCHAR(50),
                valor REAL,
                data_hora TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        return "✅ Conexão com o Banco de Dados estabelecida com sucesso!"
    except Exception as e:
        return f"❌ Erro ao conectar no banco: {e}"

# Teste local para o terminal
if __name__ == "__main__":
    print(conectar_banco())