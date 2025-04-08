from django.views.generic import TemplateView
from ..models import DadosAnuais, Operadora
import json
from decimal import Decimal

class GrowthReportView(TemplateView):
   template_name = 'dados_anuais/growth_report.html'

   def get_context_data(self, **kwargs):
       context = super().get_context_data(**kwargs)
       
       anos = list(DadosAnuais.get_anos_disponiveis())
       operadoras = list(Operadora.objects.values_list('nome', flat=True))

       growth_data = self.calculate_growth_rates(anos, operadoras)
       
       # Adicionar crescimento total do mercado
       growth_data['MERCADO_TOTAL'] = self.calculate_total_market_growth(anos)

       context['growth_data'] = json.dumps(growth_data, default=self.decimal_default)
       context['anos'] = json.dumps(anos)
       context['operadoras'] = json.dumps(operadoras + ['MERCADO_TOTAL'])  # Adicionar total do mercado

       return context

   def calculate_growth_rates(self, anos, operadoras):
       growth_data = {}
       
       # Dicionário de indicadores principais a serem incluídos no relatório
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
       
       for operadora_nome in operadoras:
           growth_data[operadora_nome] = {}
           
           operadora = Operadora.objects.get(nome=operadora_nome)
           
           for i in range(1, len(anos)):
               ano_atual = anos[i]
               
               # Obter o objeto DadosAnuais para este ano e operadora
               dados_atual = DadosAnuais.objects.filter(
                   ano=ano_atual, 
                   operadora=operadora
               ).select_related('operadora').first()
               
               if dados_atual:
                   growth_data[operadora_nome][ano_atual] = {}
                   
                   # Calcular crescimento para cada indicador usando o método do modelo
                   for campo, nome in indicadores_principais.items():
                       crescimento = dados_atual.calcular_crescimento(campo)
                       growth_data[operadora_nome][ano_atual][campo] = float(crescimento)

       return growth_data
       
   def calculate_total_market_growth(self, anos):
       """Calcula o crescimento do mercado total para cada ano."""
       growth_data = {}
       
       # Dicionário de indicadores principais a serem incluídos no relatório
       indicadores_principais = [
           'assinantes_rede_movel',
           'assinantes_banda_larga_movel',
           'assinantes_3g',
           'assinantes_4g',
           'banda_larga_256kbps',
           'receita_total',
           'trafego_dados',
           'investimentos',
           'volume_negocio'
       ]
       
       for i in range(1, len(anos)):
           ano_anterior = anos[i-1]
           ano_atual = anos[i]
           growth_data[ano_atual] = {}
           
           for campo in indicadores_principais:
               # Obter os totais para o ano atual e anterior
               total_atual = DadosAnuais.get_total_mercado(ano_atual, campo)
               total_anterior = DadosAnuais.get_total_mercado(ano_anterior, campo)
               
               # Calcular o crescimento
               if total_anterior and total_anterior != 0:
                   if isinstance(total_atual, Decimal) and isinstance(total_anterior, Decimal):
                       crescimento = ((total_atual - total_anterior) / total_anterior) * Decimal('100')
                       growth_data[ano_atual][campo] = float(crescimento)
                   else:
                       crescimento = ((total_atual - total_anterior) / total_anterior) * 100
                       growth_data[ano_atual][campo] = crescimento
               else:
                   growth_data[ano_atual][campo] = 0 if total_atual == 0 else 100
       
       return growth_data

   def decimal_default(self, obj):
       if isinstance(obj, Decimal):
           return float(obj)
       raise TypeError