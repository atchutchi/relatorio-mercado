from celery import shared_task
from .resource import DadosAnuaisResource
from tablib import Dataset
from django.core.files.storage import default_storage

@shared_task
def process_excel_upload(file_path):
    dados_resource = DadosAnuaisResource()
    dataset = Dataset()
    with default_storage.open(file_path) as f:
        imported_data = dataset.load(f.read(), format='xlsx')
    
    result = dados_resource.import_data(dataset, dry_run=True)
    if not result.has_errors():
        dados_resource.import_data(dataset, dry_run=False)
    
    default_storage.delete(file_path)
    return 'Upload processado com sucesso'