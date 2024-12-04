from django.views.generic import TemplateView
from ..models import DadosAnuais
import json
from decimal import Decimal

class GrowthReportView(TemplateView):
   template_name = 'dados_anuais/growth_report.html'

   def get_context_data(self, **kwargs):
       context = super().get_context_data(**kwargs)
       
       anos = list(DadosAnuais.get_anos_disponiveis())
       operadoras = [op[0] for op in DadosAnuais.OPERADORAS if op[0] != 'TOTAL']

       growth_data = self.calculate_growth_rates(anos, operadoras)

       context['growth_data'] = json.dumps(growth_data, default=self.decimal_default)
       context['anos'] = json.dumps(anos)
       context['operadoras'] = json.dumps(operadoras)

       return context

   def calculate_growth_rates(self, anos, operadoras):
       growth_data = {}
       for operadora in operadoras:
           growth_data[operadora] = {}
           for i in range(1, len(anos)):
               ano_anterior = anos[i-1]
               ano_atual = anos[i]
               dados_anterior = DadosAnuais.objects.filter(ano=ano_anterior, operadora=operadora).first()
               dados_atual = DadosAnuais.objects.filter(ano=ano_atual, operadora=operadora).first()
               
               if dados_anterior and dados_atual:
                   growth_data[operadora][ano_atual] = self.calculate_indicators_growth(
                       dados_anterior, dados_atual
                   )

       return growth_data

   def calculate_indicators_growth(self, dados_anterior, dados_atual):
       indicadores_principais = {
           'assinantes_rede_movel': 'Assinantes Rede Móvel',
           'assinantes_banda_larga_movel': 'Banda Larga Móvel',
           'assinantes_3g': '3G',
           'assinantes_4g': '4G',
           'banda_larga_256kbps': 'Banda Larga Fixa',
           'banda_larga_256k_2m': '256K-2M',
           'banda_larga_2m_4m': '2M-4M',
           'banda_larga_5m_10m': '5M-10M',
           'banda_larga_10m': '10M+',
           'banda_larga_outros': 'Outros',
           'receita_total': 'Receita Total',
           'trafego_dados': 'Tráfego de Dados',
           'investimentos': 'Investimentos',
           'volume_negocio': 'Volume de Negócio'
       }

       growth = {}
       for campo, nome in indicadores_principais.items():
           valor_anterior = getattr(dados_anterior, campo) or 0
           valor_atual = getattr(dados_atual, campo) or 0
           
           if isinstance(valor_anterior, Decimal):
               valor_anterior = float(valor_anterior)
           if isinstance(valor_atual, Decimal):
               valor_atual = float(valor_atual)
               
           if valor_anterior != 0:
               growth[campo] = ((valor_atual - valor_anterior) / valor_anterior) * 100
           else:
               growth[campo] = 0 if valor_atual == 0 else 100

       return growth

   def decimal_default(self, obj):
       if isinstance(obj, Decimal):
           return float(obj)
       raise TypeError