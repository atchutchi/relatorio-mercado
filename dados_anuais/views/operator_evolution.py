from django.views.generic import TemplateView
from ..models import DadosAnuais
import json
from django.db.models import F

class OperatorEvolutionView(TemplateView):
    template_name = 'dados_anuais/operator_evolution.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        operadora = self.kwargs.get('operadora')
        
        dados = DadosAnuais.objects.filter(operadora=operadora).order_by('ano')
        anos = list(dados.values_list('ano', flat=True))

        indicadores = [
            'assinantes_rede_movel', 'assinantes_pos_pago', 'assinantes_pre_pago', 'utilizacao_efetiva',
            'assinantes_banda_larga_movel', 'assinantes_3g', 'assinantes_4g',
            'assinantes_banda_larga_fixa', 'volume_negocio', 'investimentos',
            'trafego_voz_originado', 'trafego_sms', 'trafego_dados',
            'chamadas_originadas', 'trafego_voz_terminado', 'trafego_sms_terminado',
            'chamadas_terminadas', 'roaming_in_minutos', 'roaming_out_minutos',
            'volume_internet_nacional', 'volume_internet_internacional',
            'receita_total', 'banda_larga_internacional', 'emprego_total'
        ]

        evolution_data = {indicador: list(dados.values_list(indicador, flat=True)) for indicador in indicadores}
        
        # Calcular crescimento ano a ano
        growth_data = {}
        for indicador in indicadores:
            growth = []
            for i in range(1, len(anos)):
                valor_anterior = evolution_data[indicador][i-1] or 0
                valor_atual = evolution_data[indicador][i] or 0
                if valor_anterior != 0:
                    growth.append(((valor_atual - valor_anterior) / valor_anterior) * 100)
                else:
                    growth.append(0)
            growth_data[indicador] = growth

        context['operadora'] = operadora
        context['anos'] = json.dumps(anos)
        context['evolution_data'] = json.dumps(evolution_data)
        context['growth_data'] = json.dumps(growth_data)
        return context