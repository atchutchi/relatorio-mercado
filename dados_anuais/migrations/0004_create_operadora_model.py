# Generated manually to fix migration issues

from django.db import migrations, models


def adicionar_operadoras(apps, schema_editor):
    Operadora = apps.get_model('dados_anuais', 'Operadora')
    
    # Criar as operadoras necessárias
    Operadora.objects.create(nome='MTN')
    Operadora.objects.create(nome='ORANGE')


class Migration(migrations.Migration):

    dependencies = [
        ('dados_anuais', '0003_alter_dadosanuais_operadora'),
    ]

    operations = [
        migrations.CreateModel(
            name='Operadora',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=50, unique=True)),
                ('codigo', models.CharField(blank=True, max_length=50, null=True)),
            ],
            options={
                'verbose_name': 'Operadora',
                'verbose_name_plural': 'Operadoras',
                'ordering': ['nome'],
            },
        ),
        migrations.RunPython(adicionar_operadoras),
    ]