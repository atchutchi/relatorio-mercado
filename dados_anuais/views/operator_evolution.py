from django.views.generic import TemplateView
from django.shortcuts import get_object_or_404
from ..models import DadosAnuais, Operadora
import json
from decimal import Decimal

class OperatorEvolutionView(TemplateView):
    template_name = 'dados_anuais/operator_evolution.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        operadora_nome = self.kwargs.get('operadora')
        
        # Obter a instância de Operadora pelo nome
        operadora = get_object_or_404(Operadora, nome=operadora_nome)
        
        # Usar a instância de Operadora para filtrar os dados
        dados = DadosAnuais.objects.filter(operadora=operadora).order_by('ano')
        anos = list(dados.values_list('ano', flat=True))

        # Adicionar todos os indicadores relevantes
        indicadores = [
            'assinantes_rede_movel', 'assinantes_pos_pago', 'assinantes_pre_pago', 'utilizacao_efetiva',
            'assinantes_banda_larga_movel', 'assinantes_3g', 'assinantes_4g',
            'banda_larga_256kbps', 'banda_larga_256k_2m', 'banda_larga_2m_4m', 
            'banda_larga_5m_10m', 'banda_larga_10m', 'banda_larga_outros',
            'volume_negocio', 'investimentos',
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

        evolution_data = {}
        
        # Processar dados básicos
        for indicador in indicadores:
            evolution_data[indicador] = [decimal_to_float(getattr(d, indicador)) for d in dados]
        
        # Adicionar total de banda larga fixa (que é igual ao banda_larga_256kbps)
        evolution_data['banda_larga_fixa_total'] = evolution_data['banda_larga_256kbps']

        # Calcular crescimento
        growth_data = {}
        for indicador in indicadores + ['banda_larga_fixa_total']:
            growth = []
            values = evolution_data[indicador]
            for i in range(1, len(anos)):
                valor_anterior = values[i-1] or 0
                valor_atual = values[i] or 0
                growth.append(((valor_atual - valor_anterior) / valor_anterior * 100) if valor_anterior else 0)
            growth_data[indicador] = growth

        # Gerar resumo incluindo banda larga fixa
        resumo = self.gerar_resumo(evolution_data, growth_data, anos, operadora.nome)

        context['operadora'] = operadora.nome
        context['anos'] = json.dumps(anos)
        context['evolution_data'] = json.dumps(evolution_data)
        context['growth_data'] = json.dumps(growth_data)
        context['resumo'] = resumo
        return context

    def gerar_resumo(self, evolution_data, growth_data, anos, operadora_nome):
        resumo = f"Resumo da evolução da {operadora_nome} de {anos[0]} a {anos[-1]}:\n\n"

        indicadores_principais = [
            'assinantes_rede_movel',
            'assinantes_banda_larga_movel',
            'banda_larga_fixa_total',
            'receita_total',
            'trafego_dados'
        ]

        for indicador in indicadores_principais:
            valor_inicial = evolution_data[indicador][0]
            valor_final = evolution_data[indicador][-1]
            crescimento_total = ((valor_final - valor_inicial) / valor_inicial) * 100 if valor_inicial else 0

            resumo += f"{indicador.replace('_', ' ').title()}:\n"
            resumo += f"- Valor em {anos[0]}: {valor_inicial:,.0f}\n"
            resumo += f"- Valor em {anos[-1]}: {valor_final:,.0f}\n"
            resumo += f"- Crescimento total: {crescimento_total:.2f}%\n"

            if indicador in growth_data:
                maior_crescimento = max(growth_data[indicador])
                ano_maior_crescimento = anos[growth_data[indicador].index(maior_crescimento) + 1]
                resumo += f"- Maior crescimento anual: {maior_crescimento:.2f}% em {ano_maior_crescimento}\n\n"

        return resumo