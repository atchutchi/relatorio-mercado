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
                   # Get main fields
                   dados_dic = {
                       'assinantes_rede_movel': dados.assinantes_rede_movel or 0,
                       'assinantes_banda_larga_movel': dados.assinantes_banda_larga_movel or 0,
                       'assinantes_3g': dados.assinantes_3g or 0,
                       'assinantes_4g': dados.assinantes_4g or 0,
                       'banda_larga_fixa': dados.banda_larga_256kbps or 0,
                       '256k_2m': dados.banda_larga_256k_2m or 0,
                       '2m_4m': dados.banda_larga_2m_4m or 0,
                       '5m_10m': dados.banda_larga_5m_10m or 0,
                       '10m': dados.banda_larga_10m or 0,
                       'outros': dados.banda_larga_outros or 0,
                       'receita_total': float(dados.receita_total or 0),
                       'trafego_dados': dados.trafego_dados or 0,
                       'investimentos': float(dados.investimentos or 0),
                       'volume_negocio': float(dados.volume_negocio or 0),
                   }
                   comparison_data[ano][operadora] = dados_dic

       context['comparison_data'] = json.dumps(comparison_data, default=self.decimal_default)
       context['anos'] = json.dumps(anos)
       context['operadoras'] = json.dumps(operadoras)

       return context

   def decimal_default(self, obj):
       if isinstance(obj, Decimal):
           return float(obj)
       raise TypeError