# Generated by Django 5.0.7 on 2024-09-09 11:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dados_anuais', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dadosanuais',
            name='assinantes_3g',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='dadosanuais',
            name='assinantes_3g_box',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='dadosanuais',
            name='assinantes_3g_usb',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='dadosanuais',
            name='assinantes_4g',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='dadosanuais',
            name='assinantes_4g_box',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='dadosanuais',
            name='assinantes_4g_usb',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='dadosanuais',
            name='assinantes_banda_larga_fixa',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='dadosanuais',
            name='assinantes_banda_larga_movel',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='dadosanuais',
            name='assinantes_pos_pago',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='dadosanuais',
            name='assinantes_pre_pago',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='dadosanuais',
            name='assinantes_rede_movel',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='dadosanuais',
            name='banda_larga_10m',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='dadosanuais',
            name='banda_larga_256k_2m',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='dadosanuais',
            name='banda_larga_256kbps',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='dadosanuais',
            name='banda_larga_2m_4m',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='dadosanuais',
            name='banda_larga_5m_10m',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='dadosanuais',
            name='banda_larga_internacional',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=20, null=True),
        ),
        migrations.AlterField(
            model_name='dadosanuais',
            name='banda_larga_outros',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='dadosanuais',
            name='chamadas_originadas',
            field=models.BigIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='dadosanuais',
            name='chamadas_originadas_internacional',
            field=models.BigIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='dadosanuais',
            name='chamadas_originadas_numeros_curtos',
            field=models.BigIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='dadosanuais',
            name='chamadas_originadas_off_net',
            field=models.BigIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='dadosanuais',
            name='chamadas_originadas_on_net',
            field=models.BigIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='dadosanuais',
            name='chamadas_terminadas',
            field=models.BigIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='dadosanuais',
            name='chamadas_terminadas_internacional',
            field=models.BigIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='dadosanuais',
            name='chamadas_terminadas_off_net',
            field=models.BigIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='dadosanuais',
            name='emprego_homens',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='dadosanuais',
            name='emprego_mulheres',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='dadosanuais',
            name='emprego_total',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='dadosanuais',
            name='investimentos',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=20, null=True),
        ),
        migrations.AlterField(
            model_name='dadosanuais',
            name='receita_chamadas_internacional',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=20, null=True),
        ),
        migrations.AlterField(
            model_name='dadosanuais',
            name='receita_chamadas_off_net',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=20, null=True),
        ),
        migrations.AlterField(
            model_name='dadosanuais',
            name='receita_chamadas_on_net',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=20, null=True),
        ),
        migrations.AlterField(
            model_name='dadosanuais',
            name='receita_chamadas_originadas',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=20, null=True),
        ),
        migrations.AlterField(
            model_name='dadosanuais',
            name='receita_chamadas_terminadas',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=20, null=True),
        ),
        migrations.AlterField(
            model_name='dadosanuais',
            name='receita_chamadas_terminadas_internacional',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=20, null=True),
        ),
        migrations.AlterField(
            model_name='dadosanuais',
            name='receita_chamadas_terminadas_off_net',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=20, null=True),
        ),
        migrations.AlterField(
            model_name='dadosanuais',
            name='receita_dados_moveis',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=20, null=True),
        ),
        migrations.AlterField(
            model_name='dadosanuais',
            name='receita_mobile_money',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=20, null=True),
        ),
        migrations.AlterField(
            model_name='dadosanuais',
            name='receita_roaming_out',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=20, null=True),
        ),
        migrations.AlterField(
            model_name='dadosanuais',
            name='receita_servicos_mensagens',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=20, null=True),
        ),
        migrations.AlterField(
            model_name='dadosanuais',
            name='receita_servicos_voz',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=20, null=True),
        ),
        migrations.AlterField(
            model_name='dadosanuais',
            name='receita_total',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=20, null=True),
        ),
        migrations.AlterField(
            model_name='dadosanuais',
            name='roaming_in_chamadas',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='dadosanuais',
            name='roaming_in_minutos',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='dadosanuais',
            name='roaming_out_chamadas',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='dadosanuais',
            name='roaming_out_minutos',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='dadosanuais',
            name='trafego_dados',
            field=models.BigIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='dadosanuais',
            name='trafego_dados_2g',
            field=models.BigIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='dadosanuais',
            name='trafego_dados_3g',
            field=models.BigIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='dadosanuais',
            name='trafego_dados_3g_box',
            field=models.BigIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='dadosanuais',
            name='trafego_dados_3g_usb',
            field=models.BigIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='dadosanuais',
            name='trafego_dados_4g',
            field=models.BigIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='dadosanuais',
            name='trafego_dados_4g_box',
            field=models.BigIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='dadosanuais',
            name='trafego_dados_4g_usb',
            field=models.BigIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='dadosanuais',
            name='trafego_sms',
            field=models.BigIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='dadosanuais',
            name='trafego_sms_internacional',
            field=models.BigIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='dadosanuais',
            name='trafego_sms_off_net',
            field=models.BigIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='dadosanuais',
            name='trafego_sms_on_net',
            field=models.BigIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='dadosanuais',
            name='trafego_sms_roaming_in',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='dadosanuais',
            name='trafego_sms_roaming_out',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='dadosanuais',
            name='trafego_sms_terminado',
            field=models.BigIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='dadosanuais',
            name='trafego_sms_terminado_internacional',
            field=models.BigIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='dadosanuais',
            name='trafego_sms_terminado_off_net',
            field=models.BigIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='dadosanuais',
            name='trafego_voz_internacional',
            field=models.BigIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='dadosanuais',
            name='trafego_voz_numeros_curtos',
            field=models.BigIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='dadosanuais',
            name='trafego_voz_off_net',
            field=models.BigIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='dadosanuais',
            name='trafego_voz_on_net',
            field=models.BigIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='dadosanuais',
            name='trafego_voz_originado',
            field=models.BigIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='dadosanuais',
            name='trafego_voz_terminado',
            field=models.BigIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='dadosanuais',
            name='trafego_voz_terminado_internacional',
            field=models.BigIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='dadosanuais',
            name='trafego_voz_terminado_off_net',
            field=models.BigIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='dadosanuais',
            name='utilizacao_efetiva',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='dadosanuais',
            name='volume_internet_internacional',
            field=models.BigIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='dadosanuais',
            name='volume_internet_nacional',
            field=models.BigIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='dadosanuais',
            name='volume_negocio',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=20, null=True),
        ),
    ]