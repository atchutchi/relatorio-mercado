import logging
from django.views.generic import TemplateView
from django.db.models import Sum, Avg, F, Count, Q
from decimal import Decimal
from datetime import datetime, timedelta
import json
from ..models import DadosAnuais, Operadora

logger = logging.getLogger(__name__)

class AnnualReportView(TemplateView):
    template_name = 'dados_anuais/annual_report.html'

    def get_context_data(self, **kwargs):
        """
        Obtém os dados de contexto para o relatório anual.

        Args:
            **kwargs: Argumentos adicionais.

        Returns:
            dict: Dados de contexto para o relatório anual.
        """
        context = super().get_context_data(**kwargs)
        
        try:
            # Obter anos disponíveis
            anos_disponiveis = list(DadosAnuais.get_anos_disponiveis())
            if not anos_disponiveis:
                logger.warning("Nenhum ano disponível encontrado")
                self._add_empty_context(context)
                return context
                
            # Obter o ano selecionado
            ano_selecionado = self.get_selected_year(anos_disponiveis)
            
            # Obter dados do mercado para o ano selecionado
            dados_mercado = self.get_market_data(ano_selecionado)
            
            # Se não há dados para o ano selecionado, tenta usar o ano mais recente disponível
            if not dados_mercado and ano_selecionado != anos_disponiveis[-1]:
                logger.warning(f"Dados não encontrados para o ano {ano_selecionado}, tentando ano mais recente")
                ano_selecionado = anos_disponiveis[-1]
                dados_mercado = self.get_market_data(ano_selecionado)
            
            # Se ainda não há dados, retorna estrutura vazia
            if not dados_mercado:
                logger.warning(f"Dados de mercado não encontrados para o ano {ano_selecionado}")
                self._add_empty_context(context, ano_selecionado, anos_disponiveis)
                return context

            # Obter dados históricos
            dados_historicos = self.get_historic_data(ano_selecionado)
            
            # Estruturar os dados
            data_estruturada = self.estruturar_dados_completos(dados_mercado, dados_historicos.get('dados_anuais', []))
            
            # Adicionar informações adicionais
            data_estruturada.update({
                'historico': dados_historicos.get('market_share', []),
                'anos_disponiveis': anos_disponiveis,
                'ano_selecionado': ano_selecionado,
                'ano_atual': ano_selecionado,
                'resumo_executivo': self.gerar_resumo_executivo(dados_mercado, dados_historicos),
                'analise_setorial': self.gerar_analise_setorial(dados_mercado)
            })
            
            # Preparar dados para JSON
            data_estruturada_json = self.prepare_data_for_json(data_estruturada)
            
            # Atualizar contexto
            context.update({
                'appData': json.dumps(data_estruturada_json),
                'ano_atual': ano_selecionado,
                'anos_disponiveis': anos_disponiveis,
                'dados_mercado': data_estruturada,
                'historic_data': dados_historicos
            })

            # Adicionar logs para debug
            logger.debug(f"Dados estruturados para JSON: {data_estruturada_json}")
            logger.debug(f"Context final: {context}")

        except Exception as e:
            logger.error(f"Erro ao gerar contexto do relatório anual: {str(e)}")
            context['erro'] = f"Ocorreu um erro ao gerar o relatório: {str(e)}"
            self._add_empty_context(context)

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
            dict: Dados de mercado para o ano especificado ou None se não encontrar.
        """
        try:
            # Buscar operadoras disponíveis
            operadoras = {op.nome.lower(): op for op in Operadora.objects.all()}
            if not operadoras:
                logger.warning(f"Nenhuma operadora encontrada no sistema para o ano {ano}")
                return None
                
            dados = {}
            found_any = False
            
            # Buscar dados para cada operadora
            for nome_op, op_obj in operadoras.items():
                try:
                    dados_op = DadosAnuais.objects.filter(
                        ano=ano, 
                        operadora__id=op_obj.id
                    ).select_related('operadora').first()
                    
                    if dados_op:
                        dados[nome_op] = dados_op
                        found_any = True
                    else:
                        logger.warning(f"Dados não encontrados para {nome_op.upper()} no ano {ano}")
                except Exception as e:
                    logger.error(f"Erro ao buscar dados para {nome_op.upper()} no ano {ano}: {str(e)}")
                    
            if not found_any:
                logger.warning(f"Nenhum dado de operadora encontrado para o ano {ano}")
                return None

            # Calcular totais apenas se tiver dados
            if dados:
                totais = self.calcular_totais_mercado(list(dados.values()))
                dados['totais'] = totais
                return dados
                
            return None
            
        except Exception as e:
            logger.error(f"Erro ao buscar dados de mercado para o ano {ano}: {str(e)}")
            return None

    def calcular_totais_mercado(self, operadoras):
        """
        Calcula totais agregados do mercado.
        
        NOTA: Este método foi mantido por compatibilidade, mas agora usa valores padrão 0
        dos campos numéricos ao invés de verificar None.

        Args:
            operadoras (list): Lista de objetos de dados de operadoras.

        Returns:
            dict: Totais agregados do mercado.
        """
        return {
            'assinantes_rede_movel': sum(op.assinantes_rede_movel for op in operadoras),
            'assinantes_pos_pago': sum(op.assinantes_pos_pago for op in operadoras),
            'assinantes_pre_pago': sum(op.assinantes_pre_pago for op in operadoras),
            'utilizacao_efetiva': sum(op.utilizacao_efetiva for op in operadoras),
            'assinantes_banda_larga_movel': sum(op.assinantes_banda_larga_movel for op in operadoras),
            'assinantes_3g': sum(op.assinantes_3g for op in operadoras),
            'assinantes_4g': sum(op.assinantes_4g for op in operadoras),
            'volume_negocio': sum(op.volume_negocio for op in operadoras),
            'receita_total': sum(op.receita_total for op in operadoras),
            'investimentos': sum(op.investimentos for op in operadoras),
            'trafego_dados': sum(op.trafego_dados for op in operadoras),
            'emprego_total': sum(op.emprego_total for op in operadoras),
            'emprego_homens': sum(op.emprego_homens for op in operadoras),
            'emprego_mulheres': sum(op.emprego_mulheres for op in operadoras)
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
            # Se não tiver dados do mercado, retorna estrutura vazia
            if not dados_mercado:
                logger.warning("Estruturação de dados cancelada: dados_mercado está vazio")
                return self.get_empty_structure_templates()
                
            # Dados do histórico para cálculo de crescimento (pode ser None)
            dados_ano_anterior = None
            if dados_historicos and len(dados_historicos) > 1:
                for item in dados_historicos:
                    if item['ano'] < dados_mercado['mtn'].ano:
                        dados_ano_anterior = item['dados']
                        break
                
            return {
                'mercado': self.estruturar_mercado_movel(dados_mercado),
                'indicadores_financeiros': self.estruturar_indicadores_financeiros(dados_mercado),
                'trafego': self.estruturar_trafego(dados_mercado),
                'emprego': self.estruturar_emprego(dados_mercado),
                'crescimento': self.calcular_crescimento_detalhado(dados_mercado, dados_ano_anterior),
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
            if not dados:
                return {}
                
            ano = list(dados.values())[0].ano
            operadoras = Operadora.objects.values_list('nome', flat=True)
            
            # Cálculo dos totais
            total_assinantes = DadosAnuais.get_total_mercado(ano, 'assinantes_rede_movel')
            total_pos_pago = DadosAnuais.get_total_mercado(ano, 'assinantes_pos_pago')
            total_pre_pago = DadosAnuais.get_total_mercado(ano, 'assinantes_pre_pago')
            total_utilizacao_efetiva = DadosAnuais.get_total_mercado(ano, 'utilizacao_efetiva')
            total_banda_larga = DadosAnuais.get_total_mercado(ano, 'assinantes_banda_larga_movel')
            total_3g = DadosAnuais.get_total_mercado(ano, 'assinantes_3g')
            total_4g = DadosAnuais.get_total_mercado(ano, 'assinantes_4g')
            
            # Estrutura para assinantes por operadora
            assinantes_por_operadora = {}
            for operadora in operadoras:
                if operadora.lower() in dados:
                    op_data = dados[operadora.lower()]
                    assinantes_por_operadora[operadora.upper()] = op_data.assinantes_rede_movel or 0
            
            # Estrutura para 3G por operadora
            assinantes_3g_por_operadora = {}
            for operadora in operadoras:
                if operadora.lower() in dados:
                    op_data = dados[operadora.lower()]
                    assinantes_3g_por_operadora[operadora.upper()] = op_data.assinantes_3g or 0
                    
            # Estrutura para 4G por operadora
            assinantes_4g_por_operadora = {}
            for operadora in operadoras:
                if operadora.lower() in dados:
                    op_data = dados[operadora.lower()]
                    assinantes_4g_por_operadora[operadora.upper()] = op_data.assinantes_4g or 0

            # Estrutura final
            return {
                'assinantes': {
                    'total': total_assinantes,
                    'pos_pago': total_pos_pago,
                    'pre_pago': total_pre_pago,
                    'utilizacao_efetiva': total_utilizacao_efetiva,
                    'por_operadora': assinantes_por_operadora
                },
                'banda_larga_movel': {
                    'total': total_banda_larga,
                    '3g': {
                        'total': total_3g,
                        'por_operadora': assinantes_3g_por_operadora
                    },
                    '4g': {
                        'total': total_4g,
                        'por_operadora': assinantes_4g_por_operadora
                    }
                }
            }
        except Exception as e:
            logger.error(f"Erro ao estruturar mercado móvel: {str(e)}")
            return {}

    def estruturar_indicadores_financeiros(self, dados):
        """
        Estrutura os indicadores financeiros.

        Args:
            dados (dict): Dados de mercado.

        Returns:
            dict: Indicadores financeiros estruturados.
        """
        try:
            if not dados:
                return {}
                
            ano = list(dados.values())[0].ano if list(dados.values()) else None
            if not ano:
                return {}
                
            operadoras = Operadora.objects.values_list('nome', flat=True)
            
            resultado = {}
            
            # Campos financeiros a serem estruturados - apenas usar campos que existem no modelo
            campos = [
                'volume_negocio', 'receita_total', 'receita_servicos_voz', 'receita_dados_moveis',
                'receita_servicos_mensagens', 'receita_roaming_out', 'receita_chamadas_terminadas',
                'investimentos'
            ]
            
            # Para cada campo, estruturar por operadora e calcular o total
            for campo in campos:
                resultado[campo] = {}
                
                # Adicionar valor de cada operadora
                for operadora in operadoras:
                    if operadora.lower() in dados and dados[operadora.lower()]:
                        try:
                            resultado[campo][operadora.upper()] = getattr(dados[operadora.lower()], campo) or 0
                        except AttributeError:
                            resultado[campo][operadora.upper()] = 0
                    
                # Adicionar o total
                resultado[campo]['TOTAL'] = DadosAnuais.get_total_mercado(ano, campo) or 0
                
            return resultado
        except Exception as e:
            logger.error(f"Erro ao estruturar indicadores financeiros: {str(e)}")
            return {}
            
    def estruturar_trafego(self, dados):
        """
        Estrutura os dados de tráfego.

        Args:
            dados (dict): Dados de mercado.

        Returns:
            dict: Dados de tráfego estruturados.
        """
        try:
            if not dados:
                return {}
                
            ano = list(dados.values())[0].ano if list(dados.values()) else None
            if not ano:
                return {}
                
            operadoras = Operadora.objects.values_list('nome', flat=True)
            
            resultado = {}
            
            # Campos de tráfego que existem no modelo
            campos = [
                'trafego_voz_originado', 'trafego_dados', 'trafego_sms',
                'trafego_voz_on_net', 'trafego_voz_off_net', 'trafego_voz_internacional',
                'trafego_sms_on_net', 'trafego_sms_off_net', 'trafego_sms_internacional'
            ]
            
            # Para cada campo, estruturar por operadora e calcular o total
            for campo in campos:
                resultado[campo] = {}
                
                # Adicionar valor de cada operadora
                for operadora in operadoras:
                    if operadora.lower() in dados and dados[operadora.lower()]:
                        try:
                            resultado[campo][operadora.upper()] = getattr(dados[operadora.lower()], campo) or 0
                        except AttributeError:
                            resultado[campo][operadora.upper()] = 0
                    
                # Adicionar o total
                resultado[campo]['TOTAL'] = DadosAnuais.get_total_mercado(ano, campo) or 0
            
            # Estruturar dados por operadora para facilitar o acesso no template
            resultado['por_operadora'] = {}
            for operadora in operadoras:
                if operadora.lower() in dados:
                    op_data = {}
                    for campo in campos:
                        try:
                            op_data[campo] = getattr(dados[operadora.lower()], campo) or 0
                        except AttributeError:
                            op_data[campo] = 0
                    resultado['por_operadora'][operadora.upper()] = op_data
                
            return resultado
        except Exception as e:
            logger.error(f"Erro ao estruturar dados de tráfego: {str(e)}")
            return {}
            
    def estruturar_emprego(self, dados):
        """
        Estrutura os dados de emprego.

        Args:
            dados (dict): Dados de mercado.

        Returns:
            dict: Dados de emprego estruturados.
        """
        try:
            if not dados:
                return {}
                
            ano = list(dados.values())[0].ano if list(dados.values()) else None
            if not ano:
                return {}
                
            operadoras = Operadora.objects.values_list('nome', flat=True)
            
            resultado = {}
            
            # Campos de emprego que existem no modelo
            campos = [
                'emprego_total', 'emprego_homens', 'emprego_mulheres'
            ]
            
            # Para cada campo, estruturar por operadora e calcular o total
            for campo in campos:
                resultado[campo] = {}
                
                # Adicionar valor de cada operadora
                for operadora in operadoras:
                    if operadora.lower() in dados and dados[operadora.lower()]:
                        try:
                            resultado[campo][operadora.upper()] = getattr(dados[operadora.lower()], campo) or 0
                        except AttributeError:
                            resultado[campo][operadora.upper()] = 0
                    
                # Adicionar o total
                resultado[campo]['TOTAL'] = DadosAnuais.get_total_mercado(ano, campo) or 0
                
            return resultado
        except Exception as e:
            logger.error(f"Erro ao estruturar dados de emprego: {str(e)}")
            return {}

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
            ano = mtn.ano  # Ambos objetos têm o mesmo ano

            # Função auxiliar para calcular market share usando a propriedade do modelo
            def get_market_share(objeto, campo):
                if campo == 'assinantes_rede_movel':
                    return float(objeto.market_share_assinantes)
                elif campo == 'receita_total':
                    return float(objeto.market_share_receita)
                else:
                    # Calcular diretamente usando get_total_mercado
                    total = DadosAnuais.get_total_mercado(ano, campo)
                    valor = getattr(objeto, campo)
                    if total and valor:
                        return (valor / total) * 100
                    return 0

            return {
                'assinantes_rede_movel': {
                    'MTN': get_market_share(mtn, 'assinantes_rede_movel'),
                    'ORANGE': get_market_share(orange, 'assinantes_rede_movel')
                },
                'receita_total': {
                    'MTN': get_market_share(mtn, 'receita_total'),
                    'ORANGE': get_market_share(orange, 'receita_total')
                },
                'trafego_dados': {
                    'MTN': get_market_share(mtn, 'trafego_dados'),
                    'ORANGE': get_market_share(orange, 'trafego_dados')
                }
            }
        except Exception as e:
            logger.error(f"Erro ao estruturar market share: {str(e)}")
            return {}

    def calcular_penetracao(self, dados):
        """
        Calcula a penetração de serviços móveis.

        Args:
            dados (dict): Dados de mercado.

        Returns:
            dict: Dados de penetração.
        """
        try:
            if not dados or 'mtn' not in dados:
                return {
                    'penetracao_movel': 0,
                    'populacao': 2000000
                }
                
            year = dados['mtn'].ano
            
            # Obter o total de assinantes móveis usando get_total_mercado
            total_assinantes = DadosAnuais.get_total_mercado(year, 'assinantes_rede_movel')
            
            # Valor estático para população já que não temos o campo no modelo
            # Para uma implementação real, este valor deveria ser dinâmico ou vir de outra fonte
            populacao_estimada = 2000000  # Estimativa genérica - substituir por valor real
            
            # Calcular a penetração
            penetracao = (total_assinantes / populacao_estimada) * 100 if populacao_estimada else 0
                
            return {
                'penetracao_movel': penetracao,
                'populacao': populacao_estimada
            }
        except Exception as e:
            logger.error(f"Erro ao calcular penetração: {str(e)}")
            return {
                'penetracao_movel': 0,
                'populacao': 2000000
            }

    def calcular_crescimento_detalhado(self, current_year_data, previous_year_data):
        """
        Calcula o crescimento detalhado entre dois anos.

        Args:
            current_year_data (dict): Dados do ano atual.
            previous_year_data (dict): Dados do ano anterior.

        Returns:
            dict: Dados de crescimento.
        """
        if not current_year_data or not previous_year_data:
            return {}

        try:
            # Obtém objetos do ano atual
            mtn_current = current_year_data['mtn']
            orange_current = current_year_data['orange']
            year = mtn_current.ano
            
            # Obtém objetos do ano anterior
            mtn_previous = previous_year_data['mtn']
            orange_previous = previous_year_data['orange']
            prev_year = mtn_previous.ano

            # Obter totais de mercado para os dois anos
            current_total_subscribers = DadosAnuais.get_total_mercado(year, 'assinantes_rede_movel')
            previous_total_subscribers = DadosAnuais.get_total_mercado(prev_year, 'assinantes_rede_movel')
            
            current_total_revenue = DadosAnuais.get_total_mercado(year, 'receita_total')
            previous_total_revenue = DadosAnuais.get_total_mercado(prev_year, 'receita_total')
            
            # Calcular crescimento de assinantes
            def calcular_crescimento(atual, anterior):
                if not anterior or anterior == 0:
                    return 0
                return ((atual - anterior) / anterior) * 100

            resultado = {
                'assinantes_rede_movel': {
                    'MTN': calcular_crescimento(mtn_current.assinantes_rede_movel, mtn_previous.assinantes_rede_movel),
                    'ORANGE': calcular_crescimento(orange_current.assinantes_rede_movel, orange_previous.assinantes_rede_movel),
                    'TOTAL': calcular_crescimento(current_total_subscribers, previous_total_subscribers)
                },
                'receita_total': {
                    'MTN': calcular_crescimento(mtn_current.receita_total, mtn_previous.receita_total),
                    'ORANGE': calcular_crescimento(orange_current.receita_total, orange_previous.receita_total),
                    'TOTAL': calcular_crescimento(current_total_revenue, previous_total_revenue)
                },
                'volume_negocio': {
                    'MTN': calcular_crescimento(mtn_current.volume_negocio, mtn_previous.volume_negocio),
                    'ORANGE': calcular_crescimento(orange_current.volume_negocio, orange_previous.volume_negocio),
                    'TOTAL': calcular_crescimento(
                        DadosAnuais.get_total_mercado(year, 'volume_negocio'), 
                        DadosAnuais.get_total_mercado(prev_year, 'volume_negocio')
                    )
                }
            }
            
            # Usar o método calcular_crescimento do modelo para outros campos
            campos = ['trafego_dados', 'investimentos', 'assinantes_banda_larga_movel', 'assinantes_banda_larga_fixa']
            
            for campo in campos:
                current_total = DadosAnuais.get_total_mercado(year, campo)
                previous_total = DadosAnuais.get_total_mercado(prev_year, campo)
                
                resultado[campo] = {
                    'MTN': mtn_current.calcular_crescimento(campo, mtn_previous),
                    'ORANGE': orange_current.calcular_crescimento(campo, orange_previous),
                    'TOTAL': calcular_crescimento(current_total, previous_total)
                }
            
            return resultado
        except Exception as e:
            logger.error(f"Erro ao calcular crescimento detalhado: {str(e)}")
            return {}
    
    def get_empty_structure_templates(self):
        """
        Retorna uma estrutura vazia para os templates.

        Returns:
            dict: Estrutura vazia para os templates.
        """
        return {
            'mercado': {},
            'historico': [],
            'anos_disponiveis': [],
            'ano_selecionado': None,
            'indicadores_financeiros': {},
            'trafego': {},
            'emprego': {},
            'crescimento': {},
            'market_share': {},
            'penetracao': {}
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

    def decimal_default(self, obj):
        """
        JSON serializer for objects not serializable by default.
        """
        if isinstance(obj, Decimal):
            return str(obj)
        if hasattr(obj, 'isoformat'):
            return obj.isoformat()
        return str(obj)
    
    def prepare_data_for_json(self, data):
        """
        Prepara dados para serialização JSON.
        """
        if isinstance(data, dict):
            return {key: self.prepare_data_for_json(value) for key, value in data.items()}
        elif isinstance(data, (list, tuple)):
            return [self.prepare_data_for_json(item) for item in data]
        elif isinstance(data, Decimal):
            return str(data)
        elif hasattr(data, 'isoformat'):
            return data.isoformat()
        return data

    def get_historic_data(self, ano_atual):
        """
        Retrieves historic market data.
        
        Args:
            ano_atual (int): O ano atual para o qual buscar dados históricos.
            
        Returns:
            dict: Dados históricos estruturados ou dicionário vazio se não encontrar dados.
        """
        try:
            # Pegar apenas anos que tenham dados
            anos_disponiveis = list(DadosAnuais.get_anos_disponiveis())
            if not anos_disponiveis:
                logger.warning("Nenhum ano disponível encontrado para dados históricos")
                return {'dados_anuais': [], 'market_share': []}
            
            # Filtra apenas anos anteriores ou igual ao ano_atual
            anos_anteriores = [ano for ano in anos_disponiveis if ano <= ano_atual]
            
            # Limita a no máximo 5 anos (incluindo o atual)
            if len(anos_anteriores) > 5:
                anos_anteriores = anos_anteriores[-5:]
                
            dados_historicos = []
            
            for ano in anos_anteriores:
                dados_ano = self.get_market_data(ano)
                if dados_ano:  # Só adiciona se encontrou dados válidos
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
            return {'dados_anuais': [], 'market_share': []}

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
            # Obter dados estruturados
            mercado = self.estruturar_mercado_movel(dados_mercado)
            market_share = self.estruturar_market_share(dados_mercado)
            
            # Obter operadoras
            operadoras = Operadora.objects.values_list('nome', flat=True)
            
            # Encontrar a operadora dominante (com maior market share)
            operadora_dominante = None
            share_dominante = 0
            
            for operadora in operadoras:
                share = market_share.get('assinantes_rede_movel', {}).get(operadora.upper(), 0)
                if share > share_dominante:
                    share_dominante = share
                    operadora_dominante = operadora
            
            # Se não encontrou operadora dominante
            if not operadora_dominante:
                operadora_dominante = "operadora principal"
                share_dominante = 50  # valor padrão
            
            # Calcular dados de tecnologia
            total_3g = mercado.get('banda_larga_movel', {}).get('3g', {}).get('total', 0)
            total_4g = mercado.get('banda_larga_movel', {}).get('4g', {}).get('total', 0)
            ratio_4g = (total_4g / (total_3g + total_4g)) * 100 if (total_3g + total_4g) > 0 else 0
            
            total_assinantes = mercado.get('assinantes', {}).get('total', 0)
            
            return {
                'visao_geral': {
                    'titulo': 'Visão Geral do Mercado',
                    'conteudo': f"""
                    O mercado de telecomunicações da Guiné-Bissau apresenta uma estrutura com {len(operadoras)} operadoras, 
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
            if not dados_mercado:
                return {
                    'banda_larga': {'titulo': 'Erro', 'conteudo': '', 'desafios': []},
                    'emprego': {'titulo': 'Erro', 'conteudo': '', 'recomendacoes': []}
                }
                
            # Usando o método existente para estruturar os dados
            dados_estruturados = self.estruturar_dados_completos(dados_mercado, [])
            
            # Obtendo operadoras
            operadoras = Operadora.objects.values_list('nome', flat=True)
            
            # Obtendo dados estruturados
            banda_larga = dados_estruturados.get('mercado', {}).get('banda_larga_movel', {})
            emprego = dados_estruturados.get('emprego', {})
            
            ano = list(dados_mercado.values())[0].ano
            
            # Calculando totais usando os campos que existem no modelo
            total_usuarios = DadosAnuais.get_total_mercado(ano, 'assinantes_banda_larga_movel') or 0
            total_3g = DadosAnuais.get_total_mercado(ano, 'assinantes_3g') or 0
            total_4g = DadosAnuais.get_total_mercado(ano, 'assinantes_4g') or 0
            
            # Usando os campos de emprego que realmente existem no modelo
            total_empregos_diretos = DadosAnuais.get_total_mercado(ano, 'emprego_total') or 0
            total_emprego_homens = DadosAnuais.get_total_mercado(ano, 'emprego_homens') or 0
            total_emprego_mulheres = DadosAnuais.get_total_mercado(ano, 'emprego_mulheres') or 0
            
            # Calculando proporções de gênero em vez de nacionalidade
            total_funcionarios = total_emprego_homens + total_emprego_mulheres
            proporcao_mulheres = (total_emprego_mulheres / total_funcionarios) * 100 if total_funcionarios > 0 else 0
            
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
                    O setor emprega um total de {total_empregos_diretos:,} profissionais diretos, com 
                    {proporcao_mulheres:.1f}% de participação feminina. A distribuição entre as {len(operadoras)} operadoras
                    mostra oportunidades para políticas de inclusão e diversidade mais efetivas.
                    """,
                    'recomendacoes': [
                        "Implementar programas de capacitação profissional",
                        "Aumentar a participação de profissionais de grupos diversos",
                        "Desenvolver políticas de retenção de talentos e equidade de gênero"
                    ]
                }
            }
            
        except Exception as e:
            logger.error(f"Erro ao gerar análise setorial: {str(e)}")
            return {
                'banda_larga': {'titulo': 'Erro', 'conteudo': '', 'desafios': []},
                'emprego': {'titulo': 'Erro', 'conteudo': '', 'recomendacoes': []}
            }

    def _add_empty_context(self, context, ano_selecionado=None, anos_disponiveis=None):
        """
        Adiciona dados vazios ao contexto para evitar erros no template.
        
        Args:
            context (dict): O contexto a ser atualizado
            ano_selecionado (int, optional): O ano selecionado ou None
            anos_disponiveis (list, optional): Lista de anos disponíveis ou None
        """
        if anos_disponiveis is None:
            anos_disponiveis = []
            
        if ano_selecionado is None and anos_disponiveis:
            ano_selecionado = anos_disponiveis[-1]
        elif ano_selecionado is None:
            ano_selecionado = datetime.now().year
            
        empty_data = self.get_empty_structure_templates()
        
        # Adicionar informações adicionais
        empty_data.update({
            'historico': [],
            'anos_disponiveis': anos_disponiveis,
            'ano_selecionado': ano_selecionado,
            'ano_atual': ano_selecionado,
            'resumo_executivo': {
                'visao_geral': {
                    'titulo': 'Sem Dados Disponíveis',
                    'conteudo': 'Não existem dados disponíveis para o período selecionado.'
                },
                'tecnologia': {
                    'titulo': 'Sem Dados Tecnológicos',
                    'conteudo': 'Não existem dados tecnológicos disponíveis.'
                },
                'recomendacoes': {
                    'titulo': 'Recomendações',
                    'pontos': ['Inserir dados para o período selecionado']
                }
            },
            'analise_setorial': {
                'banda_larga': {
                    'titulo': 'Sem Dados de Banda Larga',
                    'conteudo': 'Não existem dados de banda larga disponíveis.',
                    'desafios': []
                },
                'emprego': {
                    'titulo': 'Sem Dados de Emprego',
                    'conteudo': 'Não existem dados de emprego disponíveis.',
                    'recomendacoes': []
                }
            }
        })
        
        # Atualizar contexto
        context.update({
            'appData': json.dumps(self.prepare_data_for_json(empty_data)),
            'ano_atual': ano_selecionado,
            'anos_disponiveis': anos_disponiveis,
            'dados_mercado': empty_data,
            'historic_data': {'dados_anuais': [], 'market_share': []}
        })

    class Meta:
        verbose_name = "Relatório Anual do Mercado"
        verbose_name_plural = "Relatórios Anuais do Mercado"