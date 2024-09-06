from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import DadosAnuais
from .resource import DadosAnuaisResource

@admin.register(DadosAnuais)
class DadosAnuaisAdmin(ImportExportModelAdmin):
    resource_class = DadosAnuaisResource
    list_display = ('ano', 'operadora', 'assinantes_rede_movel', 'volume_negocio')
    list_filter = ('ano', 'operadora')
    search_fields = ('ano', 'operadora')