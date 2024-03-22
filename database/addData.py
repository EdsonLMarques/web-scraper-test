from pesquisa_manual.lello_imoveis import casas
import sqlite3

# Conecte-se ao banco de dados
conn = sqlite3.connect('imoveis.db')
cursor = conn.cursor()

# Insira os dados na tabela
for imovel in casas:
    try:
        cursor.execute('''
            INSERT INTO imoveis (latitude, longitude, regiao, cidade, valorLocacao)
            VALUES (?, ?, ?, ?, ?)
        ''', (imovel['latitude'], imovel['longitude'], imovel['regiao'], imovel['cidade'], imovel['valorLocacao']))
    except:
        pass

# Salve as alterações e feche a conexão
conn.commit()
conn.close()
