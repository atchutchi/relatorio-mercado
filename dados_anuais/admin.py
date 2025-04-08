from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import DadosAnuais, Operadora
from .resource import DadosAnuaisResource

@admin.register(Operadora)
class OperadoraAdmin(admin.ModelAdmin):
    list_display = ('nome',)
    search_fields = ('nome',)

@admin.register(DadosAnuais)
class DadosAnuaisAdmin(ImportExportModelAdmin):
    resource_class = DadosAnuaisResource
    list_display = ('ano', 'operadora_nome', 'assinantes_rede_movel', 'receita_total', 'arpu', 'market_share_assinantes')
    list_filter = ('ano', 'operadora')
    search_fields = ('ano', 'operadora__nome')
    ordering = ('-ano', 'operadora__nome')
    list_select_related = ('operadora',)  # Otimiza consultas ao acessar operadora.nome
    
    def operadora_nome(self, obj):
        return obj.operadora.nome
    operadora_nome.short_description = 'Operadora'
    operadora_nome.admin_order_field = 'operadora__nome'  # Permite ordenação por este campo
    
    def arpu_display(self, obj):
        return f"{obj.arpu:.2f}"
    arpu_display.short_description = 'ARPU'
    
    def market_share_display(self, obj):
        return f"{obj.market_share_assinantes:.2f}%"
    market_share_display.short_description = 'Market Share'