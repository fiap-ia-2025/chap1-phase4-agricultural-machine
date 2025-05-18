import os
import sys
import sqlite3
from datetime import datetime
from database.db_setup import create_database
from database.db_operations import (
    connect_db, 
    parse_sensor_data,
    insert_sensor_reading,
    get_sensor_readings,
    get_sensor_reading_by_id,
    update_sensor_reading,
    delete_sensor_reading,
)

def clear_screen():
    """Limpa a tela do console."""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header(title):
    """Imprime um cabeçalho formatado."""
    clear_screen()
    print("=" * 80)
    print(f" {title} ".center(80, "="))
    print("=" * 80)
    print()

def print_table(rows, title="Resultados"):
    """Imprime uma tabela formatada com os resultados."""
    if not rows:
        print("Nenhum resultado encontrado.")
        return
    
    # Obter as colunas do primeiro resultado
    columns = rows[0].keys()
    
    # Determinar a largura de cada coluna
    col_width = {col: max(len(col), max(len(str(row[col])) for row in rows)) for col in columns}
    
    # Imprimir o título
    print("\n" + "=" * 80)
    print(f" {title} ".center(80, "="))
    print("=" * 80)
    
    # Imprimir o cabeçalho
    header = " | ".join(col.ljust(col_width[col]) for col in columns)
    print(header)
    print("-" * len(header))
    
    # Imprimir as linhas
    for row in rows:
        line = " | ".join(str(row[col]).ljust(col_width[col]) for col in columns)
        print(line)
    
    print("=" * 80 + "\n")

def process_data_file(conn):

    print_header("Processar Dados de Leitura")
    
    # Solicitar o caminho do arquivo
    default_file = "sample_data.txt"
    file_path = input(f"Digite o caminho do arquivo (ou Enter para usar '{default_file}'): ")
    if not file_path:
        file_path = default_file
    
    if not os.path.exists(file_path):
        print(f"Erro: Arquivo '{file_path}' não encontrado.")
        input("\nPressione Enter para continuar...")
        return
    
    # Obter as leituras existentes para verificar duplicações
    cursor = conn.cursor()
    cursor.execute("SELECT timestamp FROM leitura_sensor")
    existing_timestamps = set()
    for row in cursor.fetchall():
        columns = [column[0] for column in cursor.description]
        row_dict = {columns[i]: row[i] for i in range(len(columns))}
        existing_timestamps.add(row_dict['timestamp'])
    
    # Processar o arquivo
    count_total = 0
    count_new = 0
    count_duplicate = 0
    
    with open(file_path, 'r') as file:
        for line_num, line in enumerate(file, 1):
            line = line.strip()
            count_total += 1
            try:
                    data = parse_sensor_data(line)
                    
                    # Verificar se já existe uma leitura com este timestamp
                    if data['timestamp'] in existing_timestamps:
                        count_duplicate += 1
                        continue
                    
                    # Inserir nova leitura
                    insert_sensor_reading(conn, 1, data)
                    existing_timestamps.add(data['timestamp'])
                    count_new += 1
                    
            except Exception as e:
                    print(f"Erro ao processar linha {line_num}: {line}")
                    print(f"Erro: {e}")
    
    print(f"\nProcessamento concluído!")
    print(f"Total de leituras no arquivo: {count_total}")
    print(f"Novas leituras inseridas: {count_new}")
    print(f"Leituras duplicadas ignoradas: {count_duplicate}")
    
    input("\nPressione Enter para continuar...")

def view_readings(conn):
   
    print_header("Visualizar Leituras de Sensores")
    
    # Solicitar a quantidade de leituras a exibir
    try:
        limit_input = input("Quantas leituras deseja visualizar? (Enter para todas): ")
        if limit_input:
            limit = int(limit_input)
        else:
            limit = 1000  # Um valor alto para "todas"
        
        # Obter as leituras
        readings = get_sensor_readings(conn, limit=limit)
        
        # Exibir as leituras
        print_table(readings, f"Últimas {len(readings)} Leituras")
        
    except ValueError:
        print("Erro: Por favor, digite um número válido.")
    
    input("\nPressione Enter para continuar...")

def update_reading(conn):
    
    print_header("Atualizar Leitura de Sensor")
    
    # Solicitar o ID da leitura a atualizar
    try:
        reading_id = int(input("Digite o ID da leitura que deseja atualizar: "))
        
        # Verificar se a leitura existe
        reading = get_sensor_reading_by_id(conn, reading_id)
        if not reading:
            print(f"Erro: Leitura com ID {reading_id} não encontrada.")
            input("\nPressione Enter para continuar...")
            return
        
        # Exibir a leitura atual
        print("\nLeitura atual:")
        print_table([reading], f"Leitura ID: {reading_id}")
        
        # Solicitar novos valores
        print("\nDigite os novos valores (ou Enter para manter o valor atual):")
        
        # Fósforo (booleano)
        fosforo_input = input(f"Fósforo (1=Presente, 0=Ausente) [{reading['fosforo']}]: ")
        fosforo = bool(int(fosforo_input)) if fosforo_input else reading['fosforo']
        
        # Potássio (booleano)
        potassio_input = input(f"Potássio (1=Presente, 0=Ausente) [{reading['potassio']}]: ")
        potassio = bool(int(potassio_input)) if potassio_input else reading['potassio']
        
        # pH (float)
        ph_input = input(f"pH (0-14) [{reading['ph']}]: ")
        ph = float(ph_input) if ph_input else reading['ph']
        
        # Umidade (float)
        umidade_input = input(f"Umidade (%) [{reading['umidade']}]: ")
        umidade = float(umidade_input) if umidade_input else reading['umidade']
        
        # Status da bomba (booleano)
        bomba_input = input(f"Status da bomba (1=Ligada, 0=Desligada) [{reading['status_bomba']}]: ")
        status_bomba = bool(int(bomba_input)) if bomba_input else reading['status_bomba']
        
        # Atualizar a leitura
        updated_data = {
            'fosforo': fosforo,
            'potassio': potassio,
            'ph': ph,
            'umidade': umidade,
            'status_bomba': status_bomba
        }
        
        success = update_sensor_reading(conn, reading_id, updated_data)
        if success:
            print("\nLeitura atualizada com sucesso!")
            
            # Exibir a leitura atualizada
            updated_reading = get_sensor_reading_by_id(conn, reading_id)
            print_table([updated_reading], f"Leitura Atualizada (ID: {reading_id})")
        else:
            print("\nErro ao atualizar leitura.")
        
    except ValueError:
        print("Erro: Por favor, digite valores válidos.")
    
    input("\nPressione Enter para continuar...")

def delete_reading(conn):
  
    print_header("Excluir Leitura de Sensor")
    
    # Solicitar o ID da leitura a excluir
    try:
        reading_id = int(input("Digite o ID da leitura que deseja excluir: "))
        
        # Verificar se a leitura existe
        reading = get_sensor_reading_by_id(conn, reading_id)
        if not reading:
            print(f"Erro: Leitura com ID {reading_id} não encontrada.")
            input("\nPressione Enter para continuar...")
            return
        
        # Exibir a leitura a ser excluída
        print("\nLeitura a ser excluída:")
        print_table([reading], f"Leitura ID: {reading_id}")
        
        # Confirmar exclusão
        confirm = input("\nTem certeza que deseja excluir esta leitura? (s/n): ")
        if confirm.lower() != 's':
            print("Exclusão cancelada.")
            input("\nPressione Enter para continuar...")
            return
        
        # Excluir a leitura
        success = delete_sensor_reading(conn, reading_id)
        if success:
            print("\nLeitura excluída com sucesso!")
        else:
            print("\nErro ao excluir leitura.")
        
    except ValueError:
        print("Erro: Por favor, digite um ID válido.")
    
    input("\nPressione Enter para continuar...")

def generate_statistics(conn):
    
    print_header("Estatísticas das Leituras")
    
    cursor = conn.cursor()
    
    # Consulta para estatísticas
    cursor.execute('''
    SELECT 
        COUNT(*) as total_leituras,
        AVG(ph) as ph_media,
        MIN(ph) as ph_min,
        MAX(ph) as ph_max,
        AVG(umidade) as umidade_media,
        MIN(umidade) as umidade_min,
        MAX(umidade) as umidade_max,
        SUM(CASE WHEN fosforo = 1 THEN 1 ELSE 0 END) as fosforo_presente,
        SUM(CASE WHEN potassio = 1 THEN 1 ELSE 0 END) as potassio_presente,
        SUM(CASE WHEN status_bomba = 1 THEN 1 ELSE 0 END) as bomba_ativa
    FROM leitura_sensor
    ''')
    
    row = cursor.fetchone()
    if not row:
        print("Nenhum dado disponível para estatísticas.")
        input("\nPressione Enter para continuar...")
        return
    
    # Converter para dicionário
    columns = [column[0] for column in cursor.description]
    stats = {columns[i]: row[i] for i in range(len(columns))}
    
    # Exibir estatísticas
    print(f"Total de leituras: {stats['total_leituras']}")
    print("\n=== Estatísticas de pH ===")
    print(f"Média: {stats['ph_media']:.2f}")
    print(f"Mínimo: {stats['ph_min']:.2f}")
    print(f"Máximo: {stats['ph_max']:.2f}")
    
    print("\n=== Estatísticas de Umidade ===")
    print(f"Média: {stats['umidade_media']:.2f}%")
    print(f"Mínimo: {stats['umidade_min']:.2f}%")
    print(f"Máximo: {stats['umidade_max']:.2f}%")
    
    print("\n=== Estatísticas de Nutrientes ===")
    print(f"Leituras com Fósforo presente: {stats['fosforo_presente']} ({stats['fosforo_presente']/stats['total_leituras']*100:.1f}%)")
    print(f"Leituras com Potássio presente: {stats['potassio_presente']} ({stats['potassio_presente']/stats['total_leituras']*100:.1f}%)")
    
    print("\n=== Estatísticas da Bomba ===")
    print(f"Tempo de bomba ativa: {stats['bomba_ativa']} leituras ({stats['bomba_ativa']/stats['total_leituras']*100:.1f}%)")
    
    input("\nPressione Enter para continuar...")

def main_menu():
    """Exibe o menu principal e processa as escolhas do usuário."""
    # Conectar ao banco de dados
    conn = create_database()
    
    while True:
        print_header("Sistema de Monitoramento Agrícola")
        
        print("1. Processar Dados de Leitura")
        print("2. Visualizar Leituras")
        print("3. Atualizar Leitura")
        print("4. Excluir Leitura")
        print("5. Estatísticas")
        print("0. Sair")
        
        choice = input("\nEscolha uma opção: ")
        
        if choice == '1':
            process_data_file(conn)
        elif choice == '2':
            view_readings(conn)
        elif choice == '3':
            update_reading(conn)
        elif choice == '4':
            delete_reading(conn)
        elif choice == '5':
            generate_statistics(conn)
        elif choice == '0':
            print("\nEncerrando o programa...")
            conn.close()
            sys.exit(0)
        else:
            print("\nOpção inválida. Por favor, tente novamente.")
            input("\nPressione Enter para continuar...")

if __name__ == "__main__":
    main_menu()