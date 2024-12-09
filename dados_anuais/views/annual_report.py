import logging
from django.views.generic import TemplateView
from django.db.models import Sum, Avg, F, Count, Q
from decimal import Decimal
from datetime import datetime, timedelta
import json
from ..models import DadosAnuais

logger = logging.getLogger(__name__)

class AnnualReportView(TemplateView):
    template_name = 'dados_anuais/annual_report.html'

    def get_context_data(self, **kwargs):
        """
        Get the context data for the annual report view.

        Args:
            **kwargs: Additional keyword arguments.

        Returns:
            dict: The context data for the annual report view.
        """
        context = super().get_context_data(**kwargs)
        
        try:
            anos_disponiveis = list(DadosAnuais.get_anos_disponiveis())
            if not anos_disponiveis:
                logger.warning("Nenhum ano disponível encontrado")
                return context
                
            ano_selecionado = self.get_selected_year(anos_disponiveis)
            dados_mercado = self.get_market_data(ano_selecionado)
            
            if not dados_mercado:
                logger.warning(f"Dados de mercado não encontrados para o ano {ano_selecionado}")
                return context

            dados_historicos = self.get_historic_data(ano_selecionado)
            data_estruturada = self.estruturar_dados_completos(dados_mercado, dados_historicos)
            
            data_estruturada.update({
                'ano_atual': ano_selecionado,
                'resumo_executivo': self.gerar_resumo_executivo(dados_mercado, dados_historicos),
                'analise_setorial': self.gerar_analise_setorial(dados_mercado)
            })
            
            context.update({
                'appData': json.dumps(data_estruturada, default=self.decimal_default),
                'ano_atual': ano_selecionado,
                'anos_disponiveis': anos_disponiveis,
                'dados_mercado': data_estruturada,
                'historic_data': dados_historicos
            })

        except Exception as e:
            logger.error(f"Erro ao gerar contexto do relatório anual: {str(e)}")
            context['erro'] = "Ocorreu um erro ao gerar o relatório"

        return context

    def get_selected_year(self, anos_disponiveis):
        """
        Obtém o ano selecionado da query string ou usa o ano mais recente disponível.

        Args:
            anos_disponiveis (list): Lista de anos disponíveis.

        Returns:
            int: O ano selecionado.
        """
        try:
            ano_selecionado = self.request.GET.get('ano')
            if ano_selecionado:
                ano_int = int(ano_selecionado)
                if ano_int in anos_disponiveis:
                    return ano_int
            return anos_disponiveis[-1]  # Retorna o ano mais recente
        except (TypeError, ValueError):
            return anos_disponiveis[-1]

    def get_market_data(self, ano):
        """
        Obtém os dados de mercado para o ano específico.

        Args:
            ano (int): O ano para o qual obter os dados de mercado.

        Returns:
            dict: Dados de mercado para o ano especificado.
        """
        try:
            dados = {
                'mtn': DadosAnuais.objects.filter(ano=ano, operadora='MTN').first(),
                'orange': DadosAnuais.objects.filter(ano=ano, operadora='ORANGE').first()
            }
            
            if not dados['mtn'] or not dados['orange']:
                logger.warning(f"Dados incompletos para o ano {ano}")
                return None

            dados['totais'] = self.calcular_totais_mercado([dados['mtn'], dados['orange']])
            return dados
        except Exception as e:
            logger.error(f"Erro ao buscar dados de mercado para o ano {ano}: {str(e)}")
            return None

    def calcular_totais_mercado(self, operadoras):
        """
        Calcula totais agregados do mercado.

        Args:
            operadoras (list): Lista de objetos de dados de operadoras.

        Returns:
            dict: Totais agregados do mercado.
        """
        return {
            'assinantes_rede_movel': sum(op.assinantes_rede_movel or 0 for op in operadoras),
            'assinantes_pos_pago': sum(op.assinantes_pos_pago or 0 for op in operadoras),
            'assinantes_pre_pago': sum(op.assinantes_pre_pago or 0 for op in operadoras),
            'utilizacao_efetiva': sum(op.utilizacao_efetiva or 0 for op in operadoras),
            'assinantes_banda_larga_movel': sum(op.assinantes_banda_larga_movel or 0 for op in operadoras),
            'assinantes_3g': sum(op.assinantes_3g or 0 for op in operadoras),
            'assinantes_4g': sum(op.assinantes_4g or 0 for op in operadoras),
            'volume_negocio': sum(op.volume_negocio or 0 for op in operadoras),
            'receita_total': sum(op.receita_total or 0 for op in operadoras),
            'investimentos': sum(op.investimentos or 0 for op in operadoras),
            'trafego_dados': sum(op.trafego_dados or 0 for op in operadoras),
            'emprego_total': sum(op.emprego_total or 0 for op in operadoras),
            'emprego_homens': sum(op.emprego_homens or 0 for op in operadoras),
            'emprego_mulheres': sum(op.emprego_mulheres or 0 for op in operadoras)
        }
    
    def estruturar_dados_completos(self, dados_mercado, dados_historicos):
        """
        Estrutura os dados completos do mercado e históricos.

        Args:
            dados_mercado (dict): Dados de mercado.
            dados_historicos (dict): Dados históricos.

        Returns:
            dict: Dados estruturados completos.
        """
        try:
            return {
                'mercado_movel': self.estruturar_mercado_movel(dados_mercado),
                'indicadores_financeiros': self.estruturar_indicadores_financeiros(dados_mercado),
                'trafego': self.estruturar_trafego(dados_mercado),
                'emprego': self.estruturar_emprego(dados_mercado),
                'crescimento': self.calcular_crescimento_detalhado(dados_mercado),
                'market_share': self.estruturar_market_share(dados_mercado),
                'penetracao': self.calcular_penetracao(dados_mercado)
            }
        except Exception as e:
            logger.error(f"Erro ao estruturar dados completos: {str(e)}")
            return self.get_empty_structure_templates()

    def estruturar_mercado_movel(self, dados):
        """
        Estrutura os dados do mercado móvel.

        Args:
            dados (dict): Dados de mercado.

        Returns:
            dict: Dados estruturados do mercado móvel.
        """
        try:
            mtn = dados['mtn']
            orange = dados['orange']
            totais = dados['totais']

            return {
                'assinantes': {
                    'total': totais['assinantes_rede_movel'],
                    'pos_pago': totais['assinantes_pos_pago'],
                    'pre_pago': totais['assinantes_pre_pago'],
                    'utilizacao_efetiva': totais['utilizacao_efetiva'],
                    'mtn_total': mtn.assinantes_rede_movel or 0,
                    'orange_total': orange.assinantes_rede_movel or 0
                },
                'banda_larga_movel': {
                    'total': totais['assinantes_banda_larga_movel'],
                    '3g': {
                        'total': totais['assinantes_3g'],
                        'mtn': mtn.assinantes_3g or 0,
                        'orange': orange.assinantes_3g or 0
                    },
                    '4g': {
                        'total': totais['assinantes_4g'],
                        'mtn': mtn.assinantes_4g or 0,
                        'orange': orange.assinantes_4g or 0
                    }
                }
            }
        except Exception as e:
            logger.error(f"Erro ao estruturar mercado móvel: {str(e)}")
            return self.get_empty_mercado_movel_structure()

    def estruturar_indicadores_financeiros(self, dados):
        """
        Estrutura os indicadores financeiros.

        Args:
            dados (dict): Dados de mercado.

        Returns:
            dict: Indicadores financeiros estruturados.
        """
        try:
            mtn = dados['mtn']
            orange = dados['orange']
            totais = dados['totais']

            return {
                'volume_negocio': {
                    'total': float(totais['volume_negocio']),
                    'mtn': float(mtn.volume_negocio or 0),
                    'orange': float(orange.volume_negocio or 0)
                },
                'receita_total': {
                    'total': float(totais['receita_total']),
                    'mtn': float(mtn.receita_total or 0),
                    'orange': float(orange.receita_total or 0)
                },
                'investimentos': {
                    'total': float(totais['investimentos'])
                },
                'por_operadora': {
                    'MTN': {
                        'volume_negocio': float(mtn.volume_negocio or 0),
                        'receita_total': float(mtn.receita_total or 0)
                    },
                    'ORANGE': {
                        'volume_negocio': float(orange.volume_negocio or 0),
                        'receita_total': float(orange.receita_total or 0)
                    }
                }
            }
        except Exception as e:
            logger.error(f"Erro ao estruturar indicadores financeiros: {str(e)}")
            return self.get_empty_indicadores_financeiros_structure()

    def estruturar_trafego(self, dados):
        """
        Estrutura os dados de tráfego.

        Args:
            dados (dict): Dados de mercado.

        Returns:
            dict: Dados estruturados de tráfego.
        """
        try:
            mtn = dados['mtn']
            orange = dados['orange']

            return {
                'voz': {
                    'total': sum(op.trafego_voz_originado or 0 for op in [mtn, orange]),
                    'on_net': sum(op.trafego_voz_on_net or 0 for op in [mtn, orange]),
                    'off_net': sum(op.trafego_voz_off_net or 0 for op in [mtn, orange]),
                    'internacional': sum(op.trafego_voz_internacional or 0 for op in [mtn, orange]),
                    'por_operadora': {
                        'MTN': {
                            'total': mtn.trafego_voz_originado or 0,
                            'on_net': mtn.trafego_voz_on_net or 0,
                            'off_net': mtn.trafego_voz_off_net or 0
                        },
                        'ORANGE': {
                            'total': orange.trafego_voz_originado or 0,
                            'on_net': orange.trafego_voz_on_net or 0,
                            'off_net': orange.trafego_voz_off_net or 0
                        }
                    }
                },
                'dados': {
                    'total': sum(op.trafego_dados or 0 for op in [mtn, orange]),
                    '3g': sum(op.trafego_dados_3g or 0 for op in [mtn, orange]),
                    '4g': sum(op.trafego_dados_4g or 0 for op in [mtn, orange]),
                    'por_operadora': {
                        'MTN': {
                            'total': mtn.trafego_dados or 0,
                            '3g': mtn.trafego_dados_3g or 0,
                            '4g': mtn.trafego_dados_4g or 0
                        },
                        'ORANGE': {
                            'total': orange.trafego_dados or 0,
                            '3g': orange.trafego_dados_3g or 0,
                            '4g': orange.trafego_dados_4g or 0
                        }
                    }
                }
            }
        except Exception as e:
            logger.error(f"Erro ao estruturar tráfego: {str(e)}")
            return self.get_empty_trafego_structure()
    
    def estruturar_emprego(self, dados):
        """
        Estrutura os dados de emprego.

        Args:
            dados (dict): Dados de mercado.

        Returns:
            dict: Dados estruturados de emprego.
        """
        try:
            mtn = dados['mtn']
            orange = dados['orange']
            totais = dados['totais']

            return {
                'total': totais['emprego_total'],
                'homens': totais['emprego_homens'],
                'mulheres': totais['emprego_mulheres'],
                'por_operadora': {
                    'MTN': {
                        'total': mtn.emprego_total or 0,
                        'homens': mtn.emprego_homens or 0,
                        'mulheres': mtn.emprego_mulheres or 0
                    },
                    'ORANGE': {
                        'total': orange.emprego_total or 0,
                        'homens': orange.emprego_homens or 0,
                        'mulheres': orange.emprego_mulheres or 0
                    }
                }
            }
        except Exception as e:
            logger.error(f"Erro ao estruturar dados de emprego: {str(e)}")
            return self.get_empty_emprego_structure()

    def estruturar_market_share(self, dados):
        """
        Estrutura os dados de market share.

        Args:
            dados (dict): Dados de mercado.

        Returns:
            dict: Dados estruturados de market share.
        """
        try:
            mtn = dados['mtn']
            orange = dados['orange']
            totais = dados['totais']

            def calcular_share(valor_operadora, valor_total):
                if not valor_total:
                    return 0
                return (valor_operadora / valor_total) * 100

            return {
                'assinantes_rede_movel': {
                    'MTN': calcular_share(mtn.assinantes_rede_movel or 0, totais['assinantes_rede_movel']),
                    'ORANGE': calcular_share(orange.assinantes_rede_movel or 0, totais['assinantes_rede_movel'])
                },
                'receita_total': {
                    'MTN': calcular_share(mtn.receita_total or 0, totais['receita_total']),
                    'ORANGE': calcular_share(orange.receita_total or 0, totais['receita_total'])
                },
                'trafego_dados': {
                    'MTN': calcular_share(mtn.trafego_dados or 0, totais['trafego_dados']),
                    'ORANGE': calcular_share(orange.trafego_dados or 0, totais['trafego_dados'])
                }
            }
        except Exception as e:
            logger.error(f"Erro ao estruturar market share: {str(e)}")
            return {}

    def calcular_penetracao(self, dados):
        """
        Calcula a taxa de penetração dos serviços de telecomunicações.

        Args:
            dados (dict): Dados de mercado.

        Returns:
            dict: Taxas de penetração calculadas.
        """
        try:
            totais = dados['totais']
            populacao = 1781308  # População estimada da Guiné-Bissau

            return {
                'telefonia_movel': (totais['assinantes_rede_movel'] / populacao) * 100,
                'banda_larga_movel': (totais['assinantes_banda_larga_movel'] / populacao) * 100,
                '3g': (totais['assinantes_3g'] / populacao) * 100,
                '4g': (totais['assinantes_4g'] / populacao) * 100
            }
        except Exception as e:
            logger.error(f"Erro ao calcular taxas de penetração: {str(e)}")
            return {
                'telefonia_movel': 0,
                'banda_larga_movel': 0,
                '3g': 0,
                '4g': 0
            }

    def calcular_crescimento_detalhado(self, dados):
        """
        Calcula o crescimento detalhado dos serviços de telecomunicações.

        Args:
            dados (dict): Dados de mercado.

        Returns:
            dict: Crescimento detalhado calculado.
        """
        try:
            ano_atual = dados['mtn'].ano
            ano_anterior = ano_atual - 1
            
            dados_anteriores = self.get_market_data(ano_anterior)
            if not dados_anteriores:
                return {'anual': {}, 'trimestral': {}}

            totais_atual = dados['totais']
            totais_anterior = dados_anteriores['totais']

            def calcular_crescimento(valor_atual, valor_anterior):
                if not valor_anterior:
                    return 0
                return ((valor_atual - valor_anterior) / valor_anterior) * 100

            return {
                'anual': {
                    'assinantes_rede_movel': calcular_crescimento(
                        totais_atual['assinantes_rede_movel'],
                        totais_anterior['assinantes_rede_movel']
                    ),
                    'receita_total': calcular_crescimento(
                        totais_atual['receita_total'],
                        totais_anterior['receita_total']
                    ),
                    'trafego_dados': calcular_crescimento(
                        totais_atual['trafego_dados'],
                        totais_anterior['trafego_dados']
                    )
                }
            }
        except Exception as e:
            logger.error(f"Erro ao calcular crescimento detalhado: {str(e)}")
            return {'anual': {}, 'trimestral': {}}
    
    def get_empty_structure_templates(self):
        """
        Retorna templates de estruturas vazias.

        Returns:
            dict: Templates de estruturas vazias.
        """
        return {
            'mercado_movel': self.get_empty_mercado_movel_structure(),
            'indicadores_financeiros': self.get_empty_indicadores_financeiros_structure(),
            'trafego': self.get_empty_trafego_structure(),
            'emprego': self.get_empty_emprego_structure()
        }

    def get_empty_mercado_movel_structure(self):
        """
        Returns a dictionary with the structure for empty mobile market data.
        """
        return {
            'assinantes': {
                'total': 0,
                'pos_pago': 0,
                'pre_pago': 0,
                'utilizacao_efetiva': 0,
                'mtn_total': 0,
                'orange_total': 0
            },
            'banda_larga_movel': {
                'total': 0,
                '3g': {'total': 0, 'mtn': 0, 'orange': 0},
                '4g': {'total': 0, 'mtn': 0, 'orange': 0}
            }
        }

    def get_empty_indicadores_financeiros_structure(self):
        """
        Returns a dictionary with the structure for empty financial indicators.
        """
        return {
            'volume_negocio': {'total': 0},
            'receita_total': {'total': 0},
            'investimentos': {'total': 0},
            'por_operadora': {
                'MTN': {'volume_negocio': 0, 'receita_total': 0},
                'ORANGE': {'volume_negocio': 0, 'receita_total': 0}
            }
        }

    def get_empty_trafego_structure(self):
        """
        Returns a dictionary with the structure for empty traffic data.
        """
        return {
            'voz': {
                'total': 0,
                'on_net': 0,
                'off_net': 0,
                'internacional': 0,
                'por_operadora': {
                    'MTN': {'total': 0, 'on_net': 0, 'off_net': 0},
                    'ORANGE': {'total': 0, 'on_net': 0, 'off_net': 0}
                }
            },
            'dados': {
                'total': 0,
                '3g': 0,
                '4g': 0,
                'por_operadora': {
                    'MTN': {'total': 0, '3g': 0, '4g': 0},
                    'ORANGE': {'total': 0, '3g': 0, '4g': 0}
                }
            }
        }

    def get_empty_emprego_structure(self):
        """
        Returns a dictionary with the structure for empty employment data.
        """
        return {
            'total': 0,
            'homens': 0,
            'mulheres': 0,
            'por_operadora': {
                'MTN': {'total': 0, 'homens': 0, 'mulheres': 0},
                'ORANGE': {'total': 0, 'homens': 0, 'mulheres': 0}
            }
        }

    def decimal_default(self, obj):
        """
        JSON serializer for objects not serializable by default.
        """
        if isinstance(obj, Decimal):
            return float(obj)
        if hasattr(obj, 'isoformat'):
            return obj.isoformat()
        return str(obj)

    def get_historic_data(self, ano_atual):
        """
        Retrieves historic market data.
        """
        try:
            anos_anteriores = range(ano_atual - 4, ano_atual + 1)
            dados_historicos = []
            
            for ano in anos_anteriores:
                dados_ano = self.get_market_data(ano)
                if dados_ano:
                    dados_historicos.append({
                        'ano': ano,
                        'dados': dados_ano
                    })
            
            return {
                'dados_anuais': dados_historicos,
                'market_share': self.calcular_market_share_historico(dados_historicos)
            }
        except Exception as e:
            logger.error(f"Erro ao buscar dados históricos: {str(e)}")
            return {'dados_anuais': [], 'market_share': {}}

    def calcular_market_share_historico(self, dados_historicos):
        """
        Calculates the historic market share for operators.
        """
        try:
            historico = []
            for dado_anual in dados_historicos:
                ano = dado_anual['ano']
                dados = dado_anual['dados']
                
                market_share = self.estruturar_market_share(dados)
                if market_share:
                    historico.append({
                        'ano': ano,
                        'market_share': market_share
                    })
            
            return historico
        except Exception as e:
            logger.error(f"Erro ao calcular histórico de market share: {str(e)}")
            return []

    def gerar_resumo_executivo(self, dados_mercado, dados_historicos):
        """
        Generates an executive summary with analysis and recommendations.
        """
        try:
            mercado_movel = self.estruturar_mercado_movel(dados_mercado)
            market_share = self.estruturar_market_share(dados_mercado)
            
            operadora_dominante = "Orange" if market_share.get('assinantes_rede_movel', {}).get('ORANGE', 0) > 50 else "MTN"
            share_dominante = max(
                market_share.get('assinantes_rede_movel', {}).get('MTN', 0),
                market_share.get('assinantes_rede_movel', {}).get('ORANGE', 0)
            )
            
            total_3g = mercado_movel.get('banda_larga_movel', {}).get('3g', {}).get('total', 0)
            total_4g = mercado_movel.get('banda_larga_movel', {}).get('4g', {}).get('total', 0)
            ratio_4g = (total_4g / (total_3g + total_4g)) * 100 if (total_3g + total_4g) > 0 else 0
            
            total_assinantes = mercado_movel.get('assinantes', {}).get('total', 0)
            
            return {
                'visao_geral': {
                    'titulo': 'Visão Geral do Mercado',
                    'conteudo': f"""
                    O mercado de telecomunicações da Guiné-Bissau apresenta uma estrutura duopolista, 
                    com {operadora_dominante} mantendo posição dominante com {share_dominante:.1f}% do mercado. 
                    A base total de assinantes alcançou {total_assinantes:,} usuários,
                    demonstrando a crescente importância do setor para a economia nacional.
                    """
                },
                'tecnologia': {
                    'titulo': 'Evolução Tecnológica',
                    'conteudo': f"""
                    A adoção de tecnologias móveis mais avançadas continua em evolução, com o 4G 
                    representando {ratio_4g:.1f}% do total de conexões de banda larga móvel. 
                    Existe uma clara oportunidade de expansão da cobertura 4G, especialmente 
                    considerando que {total_3g:,} usuários ainda utilizam tecnologia 3G.
                    """
                },
                'recomendacoes': {
                    'titulo': 'Recomendações',
                    'pontos': [
                        "Incentivar maior competição no mercado para beneficiar os consumidores",
                        "Acelerar a expansão da cobertura 4G em áreas urbanas e rurais",
                        "Desenvolver políticas para reduzir a disparidade de market share",
                        "Promover a inclusão digital através de programas de acesso universal",
                        "Monitorar a qualidade de serviço e satisfação do cliente"
                    ]
                }
            }
                
        except Exception as e:
            logger.error(f"Erro ao gerar resumo executivo: {str(e)}")
            return {
                'visao_geral': {'titulo': 'Erro', 'conteudo': 'Não foi possível gerar o resumo executivo.'},
                'tecnologia': {'titulo': 'Erro', 'conteudo': ''},
                'recomendacoes': {'titulo': 'Erro', 'pontos': []}
            }

    def gerar_analise_setorial(self, dados_mercado):
        """
        Generates detailed sector analysis.
        """
        try:
            dados_estruturados = self.estruturar_dados_completos(dados_mercado, [])
            
            banda_larga = dados_estruturados.get('mercado_movel', {}).get('banda_larga_movel', {})
            emprego = dados_estruturados.get('emprego', {})
            
            total_usuarios = banda_larga.get('total', 0)
            total_3g = banda_larga.get('3g', {}).get('total', 0)
            total_4g = banda_larga.get('4g', {}).get('total', 0)
            
            total_emprego = emprego.get('total', 0)
            total_mulheres = emprego.get('mulheres', 0)
            
            ratio_genero = (total_mulheres / total_emprego) * 100 if total_emprego > 0 else 0
            
            return {
                'banda_larga': {
                    'titulo': 'Análise de Banda Larga Móvel',
                    'conteudo': f"""
                    O setor de banda larga móvel atende atualmente {total_usuarios:,} usuários,
                    com uma distribuição entre tecnologias 3G ({total_3g:,} usuários) 
                    e 4G ({total_4g:,} usuários). A evolução para tecnologias mais
                    avançadas é crucial para suportar o crescente consumo de dados e serviços digitais.
                    """,
                    'desafios': [
                        "Expansão da cobertura em áreas rurais",
                        "Modernização da infraestrutura existente",
                        "Redução do custo de acesso para usuários finais"
                    ]
                },
                'emprego': {
                    'titulo': 'Análise do Mercado de Trabalho',
                    'conteudo': f"""
                    O setor emprega um total de {total_emprego:,} profissionais, com 
                    {ratio_genero:.1f}% de representação feminina. A distribuição entre operadoras
                    mostra oportunidades para políticas de inclusão e diversidade mais efetivas.
                    """,
                    'recomendacoes': [
                        "Implementar programas de capacitação profissional",
                        "Aumentar a participação feminina em cargos técnicos",
                        "Desenvolver políticas de retenção de talentos"
                    ]
                }
            }
            
        except Exception as e:
            logger.error(f"Erro ao gerar análise setorial: {str(e)}")
            return {
                'banda_larga': {'titulo': 'Erro', 'conteudo': '', 'desafios': []},
                'emprego': {'titulo': 'Erro', 'conteudo': '', 'recomendacoes': []}
            }

    class Meta:
        verbose_name = "Relatório Anual do Mercado"
        verbose_name_plural = "Relatórios Anuais do Mercado"