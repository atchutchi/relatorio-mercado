# Generated by Django 5.0.7 on 2024-09-06 10:53

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DadosAnuais',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ano', models.IntegerField()),
                ('operadora', models.CharField(choices=[('MTN', 'MTN'), ('ORANGE', 'Orange'), ('TOTAL', 'Total')], max_length=10)),
                ('assinantes_rede_movel', models.IntegerField()),
                ('assinantes_pos_pago', models.IntegerField()),
                ('assinantes_pre_pago', models.IntegerField()),
                ('utilizacao_efetiva', models.IntegerField()),
                ('assinantes_banda_larga_movel', models.IntegerField()),
                ('assinantes_3g', models.IntegerField()),
                ('assinantes_3g_box', models.IntegerField()),
                ('assinantes_3g_usb', models.IntegerField()),
                ('assinantes_4g', models.IntegerField()),
                ('assinantes_4g_box', models.IntegerField()),
                ('assinantes_4g_usb', models.IntegerField()),
                ('assinantes_banda_larga_fixa', models.IntegerField()),
                ('banda_larga_256kbps', models.IntegerField()),
                ('banda_larga_256k_2m', models.IntegerField()),
                ('banda_larga_2m_4m', models.IntegerField()),
                ('banda_larga_5m_10m', models.IntegerField()),
                ('banda_larga_10m', models.IntegerField()),
                ('banda_larga_outros', models.IntegerField()),
                ('volume_negocio', models.DecimalField(decimal_places=2, max_digits=20)),
                ('investimentos', models.DecimalField(decimal_places=2, max_digits=20)),
                ('trafego_voz_originado', models.BigIntegerField()),
                ('trafego_voz_on_net', models.BigIntegerField()),
                ('trafego_voz_off_net', models.BigIntegerField()),
                ('trafego_voz_numeros_curtos', models.BigIntegerField()),
                ('trafego_voz_internacional', models.BigIntegerField()),
                ('trafego_sms', models.BigIntegerField()),
                ('trafego_sms_on_net', models.BigIntegerField()),
                ('trafego_sms_off_net', models.BigIntegerField()),
                ('trafego_sms_internacional', models.BigIntegerField()),
                ('trafego_dados', models.BigIntegerField()),
                ('trafego_dados_2g', models.BigIntegerField()),
                ('trafego_dados_3g', models.BigIntegerField()),
                ('trafego_dados_3g_box', models.BigIntegerField()),
                ('trafego_dados_3g_usb', models.BigIntegerField()),
                ('trafego_dados_4g', models.BigIntegerField()),
                ('trafego_dados_4g_box', models.BigIntegerField()),
                ('trafego_dados_4g_usb', models.BigIntegerField()),
                ('chamadas_originadas', models.BigIntegerField()),
                ('chamadas_originadas_on_net', models.BigIntegerField()),
                ('chamadas_originadas_off_net', models.BigIntegerField()),
                ('chamadas_originadas_numeros_curtos', models.BigIntegerField()),
                ('chamadas_originadas_internacional', models.BigIntegerField()),
                ('trafego_voz_terminado', models.BigIntegerField()),
                ('trafego_voz_terminado_off_net', models.BigIntegerField()),
                ('trafego_voz_terminado_internacional', models.BigIntegerField()),
                ('trafego_sms_terminado', models.BigIntegerField()),
                ('trafego_sms_terminado_off_net', models.BigIntegerField()),
                ('trafego_sms_terminado_internacional', models.BigIntegerField()),
                ('chamadas_terminadas', models.BigIntegerField()),
                ('chamadas_terminadas_off_net', models.BigIntegerField()),
                ('chamadas_terminadas_internacional', models.BigIntegerField()),
                ('roaming_in_minutos', models.IntegerField()),
                ('roaming_out_minutos', models.IntegerField()),
                ('roaming_in_chamadas', models.IntegerField()),
                ('roaming_out_chamadas', models.IntegerField()),
                ('volume_internet_nacional', models.BigIntegerField()),
                ('volume_internet_internacional', models.BigIntegerField()),
                ('trafego_sms_roaming_in', models.IntegerField()),
                ('trafego_sms_roaming_out', models.IntegerField()),
                ('receita_total', models.DecimalField(decimal_places=2, max_digits=20)),
                ('receita_servicos_voz', models.DecimalField(decimal_places=2, max_digits=20)),
                ('receita_roaming_out', models.DecimalField(decimal_places=2, max_digits=20)),
                ('receita_servicos_mensagens', models.DecimalField(decimal_places=2, max_digits=20)),
                ('receita_dados_moveis', models.DecimalField(decimal_places=2, max_digits=20)),
                ('receita_chamadas_originadas', models.DecimalField(decimal_places=2, max_digits=20)),
                ('receita_chamadas_on_net', models.DecimalField(decimal_places=2, max_digits=20)),
                ('receita_chamadas_off_net', models.DecimalField(decimal_places=2, max_digits=20)),
                ('receita_chamadas_internacional', models.DecimalField(decimal_places=2, max_digits=20)),
                ('receita_chamadas_terminadas', models.DecimalField(decimal_places=2, max_digits=20)),
                ('receita_chamadas_terminadas_off_net', models.DecimalField(decimal_places=2, max_digits=20)),
                ('receita_chamadas_terminadas_internacional', models.DecimalField(decimal_places=2, max_digits=20)),
                ('receita_mobile_money', models.DecimalField(decimal_places=2, max_digits=20)),
                ('banda_larga_internacional', models.DecimalField(decimal_places=2, max_digits=20)),
                ('emprego_total', models.IntegerField()),
                ('emprego_homens', models.IntegerField()),
                ('emprego_mulheres', models.IntegerField()),
            ],
            options={
                'verbose_name': 'Dados Anuais',
                'verbose_name_plural': 'Dados Anuais',
                'ordering': ['-ano', 'operadora'],
                'unique_together': {('ano', 'operadora')},
            },
        ),
    ]
