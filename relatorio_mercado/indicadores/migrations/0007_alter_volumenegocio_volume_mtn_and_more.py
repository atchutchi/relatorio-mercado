# Generated by Django 5.0.7 on 2024-07-23 16:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('indicadores', '0006_volumenegocio_percentagem_mtn_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='volumenegocio',
            name='volume_mtn',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=15),
        ),
        migrations.AlterField(
            model_name='volumenegocio',
            name='volume_orange',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=15),
        ),
    ]