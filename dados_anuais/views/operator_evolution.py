from django.views.generic import TemplateView
from ..models import DadosAnuais
import json
from decimal import Decimal

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

        def decimal_to_float(value):
            if isinstance(value, Decimal):
                return float(value)
            return value

        evolution_data = {indicador: [decimal_to_float(getattr(d, indicador)) for d in dados] for indicador in indicadores}
        
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

        # Gerar resumo textual
        resumo = self.gerar_resumo(evolution_data, growth_data, anos)

        context['operadora'] = operadora
        context['anos'] = json.dumps(anos)
        context['evolution_data'] = json.dumps(evolution_data)
        context['growth_data'] = json.dumps(growth_data)
        context['resumo'] = resumo
        return context

    def gerar_resumo(self, evolution_data, growth_data, anos):
        resumo = f"Resumo da evolução da {self.kwargs.get('operadora')} de {anos[0]} a {anos[-1]}:\n\n"

        indicadores_principais = [
            'assinantes_rede_movel', 'receita_total', 'investimentos', 'trafego_dados'
        ]

        for indicador in indicadores_principais:
            valor_inicial = evolution_data[indicador][0]
            valor_final = evolution_data[indicador][-1]
            crescimento_total = ((valor_final - valor_inicial) / valor_inicial) * 100 if valor_inicial else 0

            resumo += f"{indicador.replace('_', ' ').title()}:\n"
            resumo += f"- Valor em {anos[0]}: {valor_inicial:,.0f}\n"
            resumo += f"- Valor em {anos[-1]}: {valor_final:,.0f}\n"
            resumo += f"- Crescimento total: {crescimento_total:.2f}%\n"

            # Adicionar informação sobre o maior crescimento anual
            maior_crescimento = max(growth_data[indicador])
            ano_maior_crescimento = anos[growth_data[indicador].index(maior_crescimento) + 1]
            resumo += f"- Maior crescimento anual: {maior_crescimento:.2f}% em {ano_maior_crescimento}\n\n"

        return resumo