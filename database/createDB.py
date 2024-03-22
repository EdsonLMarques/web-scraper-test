import sqlite3

# Conecte-se ao banco de dados
conn = sqlite3.connect('imoveis.db')
cursor = conn.cursor()

# Crie a tabela imoveis
cursor.execute('''
    CREATE TABLE IF NOT EXISTS imoveis (
        id INTEGER PRIMARY KEY,
        latitude REAL,
        longitude REAL,
        regiao TEXT,
        cidade TEXT,
        valorLocacao REAL
    )
''')

# Salve as alterações e feche a conexão
conn.commit()
conn.close()
