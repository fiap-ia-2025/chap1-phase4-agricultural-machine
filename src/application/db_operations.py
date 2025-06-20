import sqlite3
import datetime
import re

def connect_db(db_path='farm_data.db'):
    """Conecta ao banco de dados."""
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row 
    return conn

def parse_sensor_data(line: str) -> dict:
    """
    "Formato esperado: P=Presente, K=Presente, Umidade=74.50%, pH=3.4, Bomba=0"
    ou do tipo numérico anterior.
    """
    # ­Regex que captura ‘Presente’ OU número (com ou sem decimal)
    p_match      = re.search(r'P=(Presente|\d+\.\d+|\d+)', line, re.I)
    k_match      = re.search(r'K=(Presente|\d+\.\d+|\d+)', line, re.I)
    umidade_match= re.search(r'Umidade=(\d+\.\d+|\d+)%', line, re.I)
    ph_match     = re.search(r'pH=(\d+\.\d+|\d+)', line, re.I)
    bomba_match  = re.search(r'Bomba=(\d+|True|False)', line, re.I)
    temperatura_match = re.search(r'Temperatura=(\d+\.\d+|\d+)', line, re.I)

    # P e K: “Presente” → True; número > 0 → True; caso contrário False
    def presente_ou_num(match):
        if not match: 
            return False
        val = match.group(1)
        if val.lower() == 'presente':
            return True
        return bool(float(val) > 0)

    p_value = presente_ou_num(p_match)
    k_value = presente_ou_num(k_match)
    umidade = float(umidade_match.group(1)) if umidade_match else 0.0
    ph      = float(ph_match.group(1))      if ph_match      else 7.0
    temperatura      = float(temperatura_match.group(1))      if temperatura_match      else 30.0


    bomba_str = bomba_match.group(1) if bomba_match else "0"
    bomba = {'true': True, 'false': False}.get(bomba_str.lower(), bool(int(bomba_str)))

    return {
        'fosforo':      p_value,
        'potassio':     k_value,
        'umidade':      umidade,
        'ph':           ph,
        'temperatura':  temperatura,
        'status_bomba': bomba,
        'timestamp':    datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }

# CREATE - Inserir nova leitura de sensor
def insert_sensor_reading(conn, id_plantacao, data):
    """
    Insere uma nova leitura de sensor no banco de dados.
    
    Args:
        conn: Conexão com o banco de dados
        id_plantacao: ID da plantação associada
        data: Dicionário com os dados dos sensores
    
    Returns:
        ID da leitura inserida
    """
    cursor = conn.cursor()
    
    cursor.execute('''
    INSERT INTO leitura_sensor (
        id_plantacao, timestamp, fosforo, potassio, ph, umidade, temperatura, status_bomba
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        id_plantacao,
        data['timestamp'],
        data['fosforo'],
        data['potassio'],
        data['ph'],
        data['umidade'],
        data['temperatura'],
        data['status_bomba']
    ))
    
    # Atualizar o status da bomba na tabela bomba
    cursor.execute('''
    UPDATE bomba 
    SET status_atual = ?, data_hora_ultimo_status = ? 
    WHERE id_plantacao = ?
    ''', (data['status_bomba'], data['timestamp'], id_plantacao))
    
    conn.commit()
    return cursor.lastrowid

# READ - Obter leituras de sensores
def get_sensor_readings(conn, limit=10, id_plantacao=None):
    cursor = conn.cursor()
    
    query = "SELECT * FROM leitura_sensor"
    params = []
    
    if id_plantacao:
        query += " WHERE id_plantacao = ?"
        params.append(id_plantacao)
    
    query += " ORDER BY timestamp DESC LIMIT ?"
    params.append(limit)
    
    cursor.execute(query, params)
    
    # Correção: Converter manualmente para dicionários
    columns = [column[0] for column in cursor.description]
    results = []
    
    for row in cursor.fetchall():
        results.append({columns[i]: row[i] for i in range(len(columns))})
    
    return results


# READ - Obter uma leitura específica
def get_sensor_reading_by_id(conn, reading_id):
 
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM leitura_sensor WHERE id = ?", (reading_id,))
    row = cursor.fetchone()
    
    if not row:
        return None
    
    # Converter manualmente para dicionário
    columns = [column[0] for column in cursor.description]
    return {columns[i]: row[i] for i in range(len(columns))}


def update_sensor_reading(conn, reading_id, data):
    cur = conn.cursor()

    # 1. Atualiza a leitura
    cur.execute(
        """
        UPDATE leitura_sensor
           SET fosforo      = :fosforo,
               potassio     = :potassio,
               ph           = :ph,
               umidade      = :umidade,
                temperatura  = :temperatura,
               status_bomba = :status_bomba
         WHERE id = :reading_id
        """,
        {**data, "reading_id": reading_id}
    )

    # 2. Verifica se ela é a leitura mais recente daquela plantação
    cur.execute(
        """
        SELECT id_plantacao
          FROM leitura_sensor
         WHERE id = :reading_id
        """,
        {"reading_id": reading_id}
    )
    id_plantacao = cur.fetchone()[0]

    cur.execute(
        """
        SELECT id
          FROM leitura_sensor
         WHERE id_plantacao = :idp
      ORDER BY timestamp DESC
         LIMIT 1
        """,
        {"idp": id_plantacao}
    )
    leitura_recente_id = cur.fetchone()[0]

    # 3. Se for a última, sincroniza a bomba
    if leitura_recente_id == reading_id:
        cur.execute(
            """
            UPDATE bomba
                SET status_atual            = :status_bomba,
                    data_hora_ultimo_status = datetime('now','localtime')
             WHERE id_plantacao = :idp;
            """,
            {"status_bomba": data["status_bomba"], "idp": id_plantacao}
        )

    conn.commit()
    return True


# DELETE - Remover leitura de sensor
def delete_sensor_reading(conn, reading_id):

    cursor = conn.cursor()
    
    # Verificar se a leitura existe
    cursor.execute("SELECT id FROM leitura_sensor WHERE id = ?", (reading_id,))
    if not cursor.fetchone():
        return False
    
    # Remover a leitura
    cursor.execute("DELETE FROM leitura_sensor WHERE id = ?", (reading_id,))
    conn.commit()
    return True

