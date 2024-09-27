from django.views.generic import TemplateView
from ..models import DadosAnuais
import json

class AnnualComparisonView(TemplateView):
    template_name = 'dados_anuais/annual_comparison.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        anos = list(DadosAnuais.get_anos_disponiveis())
        operadoras = DadosAnuais.OPERADORAS

        comparison_data = {}
        for ano in anos:
            comparison_data[ano] = {}
            for operadora, _ in operadoras:
                dados = DadosAnuais.objects.filter(ano=ano, operadora=operadora).first()
                if dados:
                    comparison_data[ano][operadora] = {
                        'assinantes': dados.assinantes_rede_movel or 0,
                        'receita': float(dados.receita_total or 0),
                        'trafego_dados': dados.trafego_dados or 0,
                        'investimentos': float(dados.investimentos or 0)
                    }

        context['comparison_data'] = json.dumps(comparison_data)
        context['anos'] = json.dumps(anos)
        context['operadoras'] = json.dumps([op[0] for op in operadoras])

        return context