from django.views.generic import TemplateView
from ..models import DadosAnuais
import json
from decimal import Decimal

class AnnualComparisonView(TemplateView):
    template_name = 'dados_anuais/annual_comparison.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        anos = list(DadosAnuais.get_anos_disponiveis())
        operadoras = [op[0] for op in DadosAnuais.OPERADORAS if op[0] != 'TOTAL']

        comparison_data = {}
        for ano in anos:
            comparison_data[ano] = {}
            for operadora in operadoras:
                dados = DadosAnuais.objects.filter(ano=ano, operadora=operadora).first()
                if dados:
                    comparison_data[ano][operadora] = self.get_all_fields(dados)

        context['comparison_data'] = json.dumps(comparison_data, default=self.decimal_default)
        context['anos'] = json.dumps(anos)
        context['operadoras'] = json.dumps(operadoras)

        return context

    def get_all_fields(self, obj):
        return {field.name: self.get_field_value(obj, field.name) for field in DadosAnuais._meta.fields if field.name not in ['id', 'ano', 'operadora']}

    def get_field_value(self, obj, field_name):
        value = getattr(obj, field_name)
        if isinstance(value, Decimal):
            return float(value)
        return value or 0

    def decimal_default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        raise TypeError