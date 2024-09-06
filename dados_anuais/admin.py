from django.contrib import admin
from .models import DadosAnuais

@admin.register(DadosAnuais)
class DadosAnuaisAdmin(admin.ModelAdmin):
    list_display = ('ano', 'operadora', 'assinantes_rede_movel', 'volume_negocio')
    list_filter = ('ano', 'operadora')
    search_fields = ('ano', 'operadora')