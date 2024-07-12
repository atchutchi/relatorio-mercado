from django.views.generic import TemplateView
from .models import EstacoesMoveisEfetivas, EmpregoSetor, TrafegoNacional, QuotaMercado, TaxaPenetracao, VolumeNegocio

class EstacoesMoveisView(TemplateView):
    template_name = 'indicadores/estacoes_moveis.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        estacoes_moveis = EstacoesMoveisEfetivas.objects.order_by('ano', 'trimestre')
        
        context['estacoes_moveis_data'] = {
            'labels': [],
            'mtn': [],
            'orange': [],
            'total': [],
        }
        
        for estacao in estacoes_moveis:
            label = f"{estacao.trimestre} {estacao.ano}"
            context['estacoes_moveis_data']['labels'].append(label)
            context['estacoes_moveis_data']['mtn'].append(estacao.mtn_estacoes)
            context['estacoes_moveis_data']['orange'].append(estacao.orange_estacoes)
            context['estacoes_moveis_data']['total'].append(estacao.mtn_estacoes + estacao.orange_estacoes)
        
        return context


class EmpregoSetorView(TemplateView):
    template_name = 'indicadores/emprego_setor.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        latest_data = EmpregoSetor.objects.order_by('-ano', '-trimestre').first()
        if latest_data:
            context['emprego_data'] = {
                'mtn': {
                    'direto': latest_data.mtn_emprego_direto,
                    'nacionais': latest_data.mtn_nacionais,
                    'homem': latest_data.mtn_homem,
                    'mulher': latest_data.mtn_mulher,
                    'indireto': latest_data.mtn_emprego_indireto,
                },
                'orange': {
                    'direto': latest_data.orange_emprego_direto,
                    'nacionais': latest_data.orange_nacionais,
                    'homem': latest_data.orange_homem,
                    'mulher': latest_data.orange_mulher,
                    'indireto': latest_data.orange_emprego_indireto,
                },
            }
        return context


class TrafegoNacionalView(TemplateView):
    template_name = 'indicadores/trafego_nacional.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        trafego = TrafegoNacional.objects.order_by('ano', 'trimestre')
        
        context['trafego_data'] = {
            'labels': [],
            'on_net': [],
            'off_net': [],
            'saida_internacional': [],
            'entrada_internacional': [],
            'roaming_in': [],
            'roaming_out': [],
        }
        
        for t in trafego:
            label = f"{t.trimestre} {t.ano}"
            context['trafego_data']['labels'].append(label)
            context['trafego_data']['on_net'].append(t.trafego_on_net)
            context['trafego_data']['off_net'].append(t.trafego_off_net)
            context['trafego_data']['saida_internacional'].append(t.trafego_internacional_saida)
            context['trafego_data']['entrada_internacional'].append(t.trafego_internacional_entrada)
            context['trafego_data']['roaming_in'].append(t.trafego_roaming_in)
            context['trafego_data']['roaming_out'].append(t.trafego_roaming_out)
        
        return context


class QuotaMercadoView(TemplateView):
    template_name = 'indicadores/quota_mercado.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        quotas = QuotaMercado.objects.order_by('ano', 'trimestre')
        
        context['quota_data'] = {
            'labels': [],
            'mtn': [],
            'orange': [],
        }
        
        for q in quotas:
            label = f"{q.trimestre} {q.ano}"
            context['quota_data']['labels'].append(label)
            context['quota_data']['mtn'].append(q.quota_mtn)
            context['quota_data']['orange'].append(q.quota_orange)
        
        return context


class TaxaPenetracaoView(TemplateView):
    template_name = 'indicadores/taxa_penetracao.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        taxas = TaxaPenetracao.objects.order_by('ano', 'trimestre')
        
        context['taxa_data'] = {
            'labels': [],
            'taxa_geral': [],
            'taxa_3g': [],
            'taxa_4g': [],
            'numero_estacoes': [],
            'variacao': [],
        }
        
        for t in taxas:
            label = f"{t.trimestre} {t.ano}"
            context['taxa_data']['labels'].append(label)
            context['taxa_data']['taxa_geral'].append(t.taxa_penetracao)
            context['taxa_data']['taxa_3g'].append(t.taxa_penetracao_3g)
            context['taxa_data']['taxa_4g'].append(t.taxa_penetracao_4g)
            context['taxa_data']['numero_estacoes'].append(t.numero_estacoes)
            context['taxa_data']['variacao'].append(t.variacao)
        
        return context


class VolumeNegocioView(TemplateView):
    template_name = 'indicadores/volume_negocio.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        volumes = VolumeNegocio.objects.order_by('ano', 'trimestre')
        
        context['volume_data'] = {
            'labels': [],
            'mtn': [],
            'orange': [],
            'total': [],
        }
        
        for v in volumes:
            label = f"{v.trimestre} {v.ano}"
            context['volume_data']['labels'].append(label)
            context['volume_data']['mtn'].append(v.volume_mtn)
            context['volume_data']['orange'].append(v.volume_orange)
            context['volume_data']['total'].append(v.volume_mtn + v.volume_orange)
        
        return context