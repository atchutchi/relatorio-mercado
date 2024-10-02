from django.views.generic import TemplateView
from ..models import DadosAnuais
import json
from decimal import Decimal
from django.db.models import Sum

class SectorPanoramaView(TemplateView):
    template_name = 'dados_anuais/sector_panorama.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        anos = list(DadosAnuais.get_anos_disponiveis())
        operadoras = [op[0] for op in DadosAnuais.OPERADORAS if op[0] != 'TOTAL']

        panorama_data = self.aggregate_sector_data(anos, operadoras)
        
        context['panorama_data'] = json.dumps(panorama_data, default=self.decimal_default)
        context['anos'] = json.dumps(anos)
        context['operadoras'] = json.dumps(operadoras)
        context['indicators'] = json.dumps(list(panorama_data[anos[0]].keys()))

        return context

    def aggregate_sector_data(self, anos, operadoras):
        panorama_data = {}
        for ano in anos:
            panorama_data[ano] = {}
            total_data = DadosAnuais.objects.filter(ano=ano, operadora='TOTAL').first()
            if total_data:
                for field in DadosAnuais._meta.fields:
                    if field.name not in ['id', 'ano', 'operadora']:
                        panorama_data[ano][field.name] = {
                            'total': getattr(total_data, field.name) or 0,
                            'operadoras': {}
                        }
                        for operadora in operadoras:
                            op_data = DadosAnuais.objects.filter(ano=ano, operadora=operadora).first()
                            if op_data:
                                panorama_data[ano][field.name]['operadoras'][operadora] = getattr(op_data, field.name) or 0
            else:
                # Se não houver dados 'TOTAL', somamos os dados das operadoras
                aggregated_data = DadosAnuais.objects.filter(ano=ano, operadora__in=operadoras).aggregate(
                    **{f'{field.name}_sum': Sum(field.name) for field in DadosAnuais._meta.fields if field.name not in ['id', 'ano', 'operadora']}
                )
                for field in DadosAnuais._meta.fields:
                    if field.name not in ['id', 'ano', 'operadora']:
                        panorama_data[ano][field.name] = {
                            'total': aggregated_data[f'{field.name}_sum'] or 0,
                            'operadoras': {}
                        }
                        for operadora in operadoras:
                            op_data = DadosAnuais.objects.filter(ano=ano, operadora=operadora).first()
                            if op_data:
                                panorama_data[ano][field.name]['operadoras'][operadora] = getattr(op_data, field.name) or 0

        return panorama_data

    def decimal_default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        raise TypeError