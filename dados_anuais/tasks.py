from celery import shared_task
from .resource import DadosAnuaisResource
from .models import Operadora
from tablib import Dataset
from django.core.files.storage import default_storage
import logging

logger = logging.getLogger(__name__)

@shared_task
def process_excel_upload(file_path):
    logger.info(f"Iniciando processamento do arquivo: {file_path}")
    
    # Garantir que as operadoras existam
    for nome in ['MTN', 'ORANGE']:
        Operadora.objects.get_or_create(nome=nome)
    logger.info("Operadoras verificadas/criadas com sucesso")
    
    dados_resource = DadosAnuaisResource()
    dataset = Dataset()
    
    try:
        with default_storage.open(file_path) as f:
            imported_data = dataset.load(f.read(), format='xlsx')
        logger.info(f"Arquivo carregado com sucesso: {len(dataset)} linhas")
        
        result = dados_resource.import_data(dataset, dry_run=True)
        if not result.has_errors():
            logger.info("Validação concluída sem erros, importando dados...")
            dados_resource.import_data(dataset, dry_run=False)
            logger.info("Importação concluída com sucesso")
        else:
            logger.error(f"Erros encontrados durante validação: {result.row_errors()}")
        
        default_storage.delete(file_path)
        logger.info(f"Arquivo temporário excluído: {file_path}")
        return 'Upload processado com sucesso'
    except Exception as e:
        logger.error(f"Erro durante processamento do arquivo: {e}")
        # Tentar excluir o arquivo mesmo em caso de erro
        try:
            default_storage.delete(file_path)
            logger.info(f"Arquivo temporário excluído após erro: {file_path}")
        except:
            pass
        return f'Erro no processamento: {str(e)}'