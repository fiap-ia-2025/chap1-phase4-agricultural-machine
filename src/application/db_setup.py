import sqlite3
import os

def create_database(db_path='farm_data.db'):
    """Cria o banco de dados e as tabelas necessárias."""
    # Verifica se o arquivo já existe
    db_exists = os.path.exists(db_path)
    
    # Conecta ao banco de dados (cria se não existir)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Cria as tabelas se o banco não existia
    if not db_exists:
        # Tabela FAZENDA
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS fazenda (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            area_total REAL NOT NULL
        )
        ''')
        
        # Tabela CULTURA
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS cultura (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL
        )
        ''')
        
        # Tabela PLANTACAO
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS plantacao (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_fazenda INTEGER NOT NULL,
            id_cultura INTEGER NOT NULL,
            area_plantada REAL NOT NULL,
            data_plantio TEXT NOT NULL,
            FOREIGN KEY (id_fazenda) REFERENCES fazenda (id),
            FOREIGN KEY (id_cultura) REFERENCES cultura (id)
        )
        ''')
        
        # Tabela SENSOR_UMIDADE
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS sensor_umidade (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_plantacao INTEGER NOT NULL,
            localizacao TEXT NOT NULL,
            FOREIGN KEY (id_plantacao) REFERENCES plantacao (id)
        )
        ''')
        
        # Tabela SENSOR_PH
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS sensor_ph (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_plantacao INTEGER NOT NULL,
            localizacao TEXT NOT NULL,
            FOREIGN KEY (id_plantacao) REFERENCES plantacao (id)
        )
        ''')
        
        # Tabela SENSOR_P
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS sensor_p (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_plantacao INTEGER NOT NULL,
            localizacao TEXT NOT NULL,
            FOREIGN KEY (id_plantacao) REFERENCES plantacao (id)
        )
        ''')
        
        # Tabela SENSOR_K
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS sensor_k (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_plantacao INTEGER NOT NULL,
            localizacao TEXT NOT NULL,
            FOREIGN KEY (id_plantacao) REFERENCES plantacao (id)
        )
        ''')
        
        # Tabela BOMBA
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS bomba (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_plantacao INTEGER NOT NULL,
            localizacao TEXT NOT NULL,
            status_atual BOOLEAN NOT NULL,
            data_hora_ultimo_status TEXT NOT NULL,
            FOREIGN KEY (id_plantacao) REFERENCES plantacao (id)
        )
        ''')
        
        # Tabela LEITURA_SENSOR (principal para os dados do monitor serial)
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS leitura_sensor (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_plantacao INTEGER NOT NULL,
            timestamp TEXT NOT NULL,
            fosforo BOOLEAN NOT NULL,
            potassio BOOLEAN NOT NULL,
            ph REAL NOT NULL,
            umidade REAL NOT NULL,
            status_bomba BOOLEAN NOT NULL,
            FOREIGN KEY (id_plantacao) REFERENCES plantacao (id)
        )
        ''')
        
        # Inserir alguns dados de exemplo para facilitar os testes
        cursor.execute("INSERT INTO fazenda (nome, area_total) VALUES ('Fazenda Modelo', 100.0)")
        cursor.execute("INSERT INTO cultura (nome) VALUES ('Soja')")
        cursor.execute("INSERT INTO plantacao (id_fazenda, id_cultura, area_plantada, data_plantio) VALUES (1, 1, 50.0, '2025-01-15')")
        cursor.execute("INSERT INTO sensor_umidade (id_plantacao, localizacao) VALUES (1, 'Setor A')")
        cursor.execute("INSERT INTO sensor_ph (id_plantacao, localizacao) VALUES (1, 'Setor A')")
        cursor.execute("INSERT INTO sensor_p (id_plantacao, localizacao) VALUES (1, 'Setor A')")
        cursor.execute("INSERT INTO sensor_k (id_plantacao, localizacao) VALUES (1, 'Setor A')")
        cursor.execute("INSERT INTO bomba (id_plantacao, localizacao, status_atual, data_hora_ultimo_status) VALUES (1, 'Setor A', 0, '2025-05-18 10:00:00')")
        
        print("Banco de dados criado com sucesso!")
    else:
        print("Conectado ao banco de dados existente.")
    
    conn.commit()
    return conn

if __name__ == "__main__":
    # Criar o banco de dados quando executado diretamente
    conn = create_database()
    conn.close()