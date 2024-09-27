import logging
from import_export import resources, fields
from import_export.widgets import IntegerWidget, DecimalWidget
from .models import DadosAnuais

logger = logging.getLogger(__name__)

class DadosAnuaisResource(resources.ModelResource):
    ano = fields.Field(attribute='ano', column_name='Ano')
    operadora = fields.Field(attribute='operadora', column_name='Operadora')

    class Meta:
        model = DadosAnuais
        import_id_fields = ()
        fields = ('ano', 'operadora', 'assinantes_rede_movel', 'assinantes_pos_pago', 'assinantes_pre_pago', 'utilizacao_efetiva',
                  'assinantes_banda_larga_movel', 'assinantes_3g', 'assinantes_3g_box', 'assinantes_3g_usb', 'assinantes_4g',
                  'assinantes_4g_box', 'assinantes_4g_usb', 'assinantes_banda_larga_fixa', 'banda_larga_256kbps', 'banda_larga_256k_2m',
                  'banda_larga_2m_4m', 'banda_larga_5m_10m', 'banda_larga_10m', 'banda_larga_outros', 'volume_negocio', 'investimentos',
                  'trafego_voz_originado', 'trafego_voz_on_net', 'trafego_voz_off_net', 'trafego_voz_numeros_curtos',
                  'trafego_voz_internacional', 'trafego_sms', 'trafego_sms_on_net', 'trafego_sms_off_net', 'trafego_sms_internacional',
                  'trafego_dados', 'trafego_dados_2g', 'trafego_dados_3g', 'trafego_dados_3g_box', 'trafego_dados_3g_usb',
                  'trafego_dados_4g', 'trafego_dados_4g_box', 'trafego_dados_4g_usb', 'chamadas_originadas',
                  'chamadas_originadas_on_net', 'chamadas_originadas_off_net', 'chamadas_originadas_numeros_curtos',
                  'chamadas_originadas_internacional', 'trafego_voz_terminado', 'trafego_voz_terminado_off_net',
                  'trafego_voz_terminado_internacional', 'trafego_sms_terminado', 'trafego_sms_terminado_off_net',
                  'trafego_sms_terminado_internacional', 'chamadas_terminadas', 'chamadas_terminadas_off_net',
                  'chamadas_terminadas_internacional', 'roaming_in_minutos', 'roaming_out_minutos', 'roaming_in_chamadas',
                  'roaming_out_chamadas', 'volume_internet_nacional', 'volume_internet_internacional', 'trafego_sms_roaming_in',
                  'trafego_sms_roaming_out', 'receita_total', 'receita_servicos_voz', 'receita_roaming_out',
                  'receita_servicos_mensagens', 'receita_dados_moveis', 'receita_chamadas_originadas', 'receita_chamadas_on_net',
                  'receita_chamadas_off_net', 'receita_chamadas_internacional', 'receita_chamadas_terminadas',
                  'receita_chamadas_terminadas_off_net', 'receita_chamadas_terminadas_internacional', 'receita_mobile_money',
                  'banda_larga_internacional', 'emprego_total', 'emprego_homens', 'emprego_mulheres')
        skip_unchanged = True
        report_skipped = False

    def before_import(self, dataset, using_transactions=True, dry_run=False, **kwargs):
        logger.info("Iniciando o processo de importação")
        logger.debug(f"Tipo do dataset: {type(dataset)}")
        logger.debug(f"Atributos do dataset: {dir(dataset)}")
        
        if hasattr(dataset, 'headers'):
            logger.debug(f"Cabeçalhos originais: {dataset.headers}")
        else:
            logger.warning("Dataset não tem atributo 'headers'")
        
        logger.debug(f"Usando transações: {using_transactions}")
        logger.debug(f"Dry run: {dry_run}")
        
        # Identificar as colunas de ano de forma segura
        self.year_columns = []
        if hasattr(dataset, 'headers') and dataset.headers:
            self.year_columns = [col for col in dataset.headers if col and str(col).isdigit()]
        
        logger.info(f"Colunas de ano identificadas: {self.year_columns}")

        # Verificar se temos dados para processar
        if not dataset or not hasattr(dataset, 'dict') or not dataset.dict:
            logger.warning("Dataset vazio ou inválido")
            return

        # Criar novas linhas para cada ano e operadora
        new_dataset = []
        for row in dataset.dict:
            logger.debug(f"Processando linha: {row}")
            indicador = row.get(dataset.headers[0], '') if dataset.headers else ''
            logger.debug(f"Processando indicador: {indicador}")
            for year in self.year_columns:
                for operadora in ['ORANGE', 'MTN', 'TOTAL']:
                    col_index = dataset.headers.index(year) + ['ORANGE', 'MTN', 'TOTAL'].index(operadora)
                    valor = row.get(dataset.headers[col_index], '')
                    if valor:
                        new_row = {
                            'Ano': year,
                            'Operadora': operadora,
                            indicador: valor
                        }
                        new_dataset.append(new_row)
                        logger.debug(f"Nova linha criada: {new_row}")
        
        # Substituir o dataset original pelo novo
        dataset.dict = new_dataset
        logger.info(f"Novo dataset criado com {len(new_dataset)} linhas")
        logger.debug("Primeiras 5 linhas do novo dataset:")
        for i, row in enumerate(dataset.dict[:5]):
            logger.debug(f"Linha {i}: {row}")

    def import_row(self, row, instance_loader, **kwargs):
        logger.debug(f"Importando linha: {row}")
        return super().import_row(row, instance_loader, **kwargs)

    def get_instance(self, instance_loader, row):
        logger.debug(f"Buscando instância para: ano={row.get('Ano')}, operadora={row.get('Operadora')}")
        try:
            return self.Meta.model.objects.get(
                ano=row['Ano'],
                operadora=row['Operadora']
            )
        except self.Meta.model.DoesNotExist:
            logger.debug("Instância não encontrada, será criada uma nova")
            return None
        except KeyError as e:
            logger.error(f"Erro ao buscar instância: {e}")
            logger.error(f"Conteúdo da linha: {row}")
            return None

    def import_field(self, field, obj, data, **kwargs):
        logger.debug(f"Importando campo: {field.column_name}, valor: {data.get(field.column_name)}")
        if field.column_name in data:
            setattr(obj, field.attribute, field.clean(data))

    def save_instance(self, instance, using_transactions=True, dry_run=False):
        logger.debug(f"Salvando instância: {instance}")
        if not dry_run:
            try:
                instance.save()
                logger.info(f"Instância salva com sucesso: ano={instance.ano}, operadora={instance.operadora}")
            except Exception as e:
                logger.error(f"Erro ao salvar instância: {e}")
        else:
            logger.info(f"Dry run: não salvando instância: ano={instance.ano}, operadora={instance.operadora}")