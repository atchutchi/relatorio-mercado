import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'relatorio_mercado.relatorio_mercado.settings')
django.setup()

from django.db import connection
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def execute_sql(query):
    with connection.cursor() as cursor:
        cursor.execute(query)
        if query.strip().upper().startswith('SELECT') or query.strip().upper().startswith('PRAGMA'):
            return cursor.fetchall()
        return None

def main():
    # Verificar quais tabelas existem no banco de dados
    logger.info("Verificando tabelas existentes...")
    tables = execute_sql("SELECT name FROM sqlite_master WHERE type='table';")
    logger.info(f"Tabelas encontradas: {tables}")
    
    # Verificar se a tabela temporária já existe e removê-la
    table_names = [t[0] for t in tables]
    if 'dados_anuais_dadosanuais_new' in table_names:
        logger.info("A tabela temporária já existe. Removendo...")
        execute_sql("DROP TABLE dados_anuais_dadosanuais_new;")
    
    # Verificar se a tabela dados_anuais_dadosanuais existe
    if 'dados_anuais_dadosanuais' not in table_names:
        logger.error("A tabela dados_anuais_dadosanuais não foi encontrada no banco de dados.")
        logger.info("Verificando outras tabelas relacionadas...")
        related_tables = [t for t in table_names if 'dados_anuais' in t]
        logger.info(f"Tabelas relacionadas a dados_anuais: {related_tables}")
        return
    
    # Verificar a estrutura atual da tabela
    logger.info("Verificando a estrutura atual da tabela...")
    structure = execute_sql("PRAGMA table_info(dados_anuais_dadosanuais);")
    logger.info(f"Estrutura atual: {structure}")
    
    if not structure:
        logger.error("Não foi possível obter a estrutura da tabela.")
        return
    
    # Verificar se operadora_id já existe
    has_operadora_id = any(col[1] == 'operadora_id' for col in structure)
    if has_operadora_id:
        logger.info("A coluna operadora_id já existe. Nada a fazer.")
        return
    
    # Verificar se operadora existe
    has_operadora = any(col[1] == 'operadora' for col in structure)
    if not has_operadora:
        logger.error("A coluna operadora não existe. Impossível continuar.")
        # Listar todas as colunas para diagnóstico
        colunas = [col[1] for col in structure]
        logger.info(f"Colunas disponíveis: {colunas}")
        return
    
    # Obter informações das operadoras
    operadoras = execute_sql("SELECT id, nome FROM dados_anuais_operadora;")
    logger.info(f"Operadoras encontradas: {operadoras}")
    
    if not operadoras:
        logger.error("Não foram encontradas operadoras na tabela dados_anuais_operadora.")
        return
    
    # Criar mapeamento de nome para ID
    operadora_map = {op[1]: op[0] for op in operadoras}
    logger.info(f"Mapeamento: {operadora_map}")
    
    # Verificar valores na coluna operadora
    valores_operadora = execute_sql("SELECT DISTINCT operadora FROM dados_anuais_dadosanuais;")
    logger.info(f"Valores distintos na coluna operadora: {valores_operadora}")
    
    # Verificar se todos os valores mapeiam para IDs existentes
    for valor in valores_operadora:
        if valor[0] not in operadora_map:
            logger.error(f"Valor '{valor[0]}' não tem mapeamento para ID. Impossível continuar.")
            return
    
    # Criar uma nova tabela com operadora_id
    logger.info("Criando nova tabela com operadora_id...")
    
    # Obter todas as colunas exceto 'operadora'
    colunas = [col[1] for col in structure if col[1] != 'operadora']
    colunas_str = ", ".join(colunas)
    
    # Criar nova tabela
    create_table_sql = f"""
    CREATE TABLE dados_anuais_dadosanuais_new (
        {colunas_str},
        operadora_id INTEGER NOT NULL,
        FOREIGN KEY (operadora_id) REFERENCES dados_anuais_operadora(id)
    );
    """
    logger.info(f"Executando SQL para criar tabela: {create_table_sql}")
    execute_sql(create_table_sql)
    
    # Copiar dados, substituindo operadora por operadora_id
    logger.info("Copiando dados para a nova tabela...")
    
    # Obter o índice da coluna operadora
    operadora_index = next((i for i, col in enumerate(structure) if col[1] == 'operadora'), -1)
    if operadora_index == -1:
        logger.error("Não foi possível encontrar o índice da coluna operadora.")
        return
    
    logger.info(f"Índice da coluna operadora: {operadora_index}")
    
    # Obter todos os registros
    registros = execute_sql("SELECT * FROM dados_anuais_dadosanuais")
    
    # Inserir cada registro na nova tabela
    contador = 0
    for reg in registros:
        operadora_nome = reg[operadora_index]
        operadora_id = operadora_map.get(operadora_nome)
        
        if not operadora_id:
            logger.error(f"Não foi encontrado ID para operadora '{operadora_nome}'")
            continue
        
        # Construir valores sem a coluna operadora
        values = []
        for i, val in enumerate(reg):
            if i != operadora_index:  # pular a coluna operadora
                if val is None:
                    values.append("NULL")
                elif isinstance(val, str):
                    values.append(f"'{val}'")
                else:
                    values.append(str(val))
        
        # Adicionar operadora_id
        values.append(str(operadora_id))
        
        # Inserir na nova tabela
        insert_sql = f"INSERT INTO dados_anuais_dadosanuais_new VALUES ({', '.join(values)});"
        execute_sql(insert_sql)
        contador += 1
    
    logger.info(f"Foram copiados {contador} registros.")
    
    # Substituir a tabela antiga pela nova
    logger.info("Substituindo a tabela antiga pela nova...")
    execute_sql("DROP TABLE dados_anuais_dadosanuais;")
    execute_sql("ALTER TABLE dados_anuais_dadosanuais_new RENAME TO dados_anuais_dadosanuais;")
    
    # Verificar resultado
    logger.info("Verificando o resultado...")
    nova_estrutura = execute_sql("PRAGMA table_info(dados_anuais_dadosanuais);")
    logger.info(f"Nova estrutura: {nova_estrutura}")
    
    # Verificar alguns registros
    amostra = execute_sql("SELECT id, ano, operadora_id FROM dados_anuais_dadosanuais LIMIT 5;")
    logger.info(f"Amostra de registros: {amostra}")
    
    logger.info("Operação concluída com sucesso!")

if __name__ == "__main__":
    main() 