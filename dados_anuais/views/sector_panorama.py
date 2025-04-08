from django.views.generic import TemplateView
from ..models import DadosAnuais, Operadora
import json
from decimal import Decimal
from django.db.models import Sum

class SectorPanoramaView(TemplateView):
    template_name = 'dados_anuais/sector_panorama.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        anos = list(DadosAnuais.get_anos_disponiveis())
        operadoras = list(Operadora.objects.values_list('nome', flat=True))

        panorama_data = self.aggregate_sector_data(anos, operadoras)
        
        context['panorama_data'] = json.dumps(panorama_data, default=self.decimal_default)
        context['anos'] = json.dumps(anos)
        context['operadoras'] = json.dumps(operadoras)
        context['indicators'] = json.dumps(list(panorama_data[anos[0]].keys()))

        return context

    def aggregate_sector_data(self, anos, operadoras):
        panorama_data = {}
        
        # Obter todos os campos do modelo, excluindo id, ano e operadora
        model_fields = [field.name for field in DadosAnuais._meta.fields 
                        if field.name not in ['id', 'ano', 'operadora']]
        
        for ano in anos:
            panorama_data[ano] = {}
            
            # Obter todas as operadoras com dados para este ano
            operadoras_no_ano = DadosAnuais.get_operadoras_por_ano(ano)
            
            # Preparar um dicionário com os nomes das operadoras
            operadoras_dict = {operadora.nome: operadora for operadora in operadoras_no_ano}
            
            # Para cada campo, calcular o total do mercado e os valores por operadora
            for field_name in model_fields:
                # Calcular o total do mercado usando o método do modelo
                total_mercado = DadosAnuais.get_total_mercado(ano, field_name)
                
                # Preparar o dicionário para este indicador
                panorama_data[ano][field_name] = {
                    'total': float(total_mercado) if isinstance(total_mercado, Decimal) else total_mercado,
                    'operadoras': {}
                }
                
                # Obter dados para cada operadora
                for operadora_nome, operadora in operadoras_dict.items():
                    op_data = DadosAnuais.objects.filter(
                        ano=ano, 
                        operadora=operadora
                    ).select_related('operadora').first()
                    
                    if op_data:
                        value = getattr(op_data, field_name)
                        panorama_data[ano][field_name]['operadoras'][operadora_nome] = float(value) if isinstance(value, Decimal) else value

        return panorama_data

    def decimal_default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        raise TypeError