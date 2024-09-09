from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import DadosAnuais
from .resource import DadosAnuaisResource

@admin.register(DadosAnuais)
class DadosAnuaisAdmin(ImportExportModelAdmin):
    resource_class = DadosAnuaisResource