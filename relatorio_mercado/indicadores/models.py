from django.db import models

class Operadora(models.Model):
    nome = models.CharField(max_length=100)

    def __str__(self):
        return self.nome

class EstacoesMoveisEfetivas(models.Model):
    operadora = models.ForeignKey(Operadora, on_delete=models.CASCADE)
    trimestre = models.CharField(max_length=10)
    ano = models.IntegerField()
    numero_estacoes = models.IntegerField()

    def __str__(self):
        return f"{self.operadora} - {self.trimestre} {self.ano}"

class EmpregoSetor(models.Model):
    operadora = models.ForeignKey(Operadora, on_delete=models.CASCADE)
    trimestre = models.CharField(max_length=10)
    ano = models.IntegerField()
    emprego_direto = models.IntegerField()
    emprego_indireto = models.IntegerField()
    nacionais = models.IntegerField()
    homens = models.IntegerField()
    mulheres = models.IntegerField()

    def __str__(self):
        return f"{self.operadora} - {self.trimestre} {self.ano}"


class TrafegoNacional(models.Model):
    trimestre = models.CharField(max_length=10)
    ano = models.IntegerField()
    total_trafego = models.BigIntegerField(verbose_name="Total Tráfego", default=0)
    on_net = models.BigIntegerField(verbose_name="On-net", default=0)
    off_net = models.BigIntegerField(verbose_name="Off-net (saída)", default=0)
    saida_internacional = models.BigIntegerField(verbose_name="Saída Internacional", default=0)
    entrada_internacional = models.BigIntegerField(verbose_name="Entrada Internacional", default=0)
    off_net_entrada = models.BigIntegerField(verbose_name="Off-net (entrada)", default=0)
    roaming_in = models.BigIntegerField(verbose_name="Roaming in", default=0)
    roaming_out = models.BigIntegerField(verbose_name="Roaming out", default=0)

    def __str__(self):
        return f"Tráfego Nacional - {self.trimestre} {self.ano}"

    class Meta:
        verbose_name = "Tráfego Nacional"
        verbose_name_plural = "Tráfegos Nacionais"
        ordering = ['-ano', '-trimestre']


class QuotaMercado(models.Model):
    operadora = models.ForeignKey(Operadora, on_delete=models.CASCADE)
    trimestre = models.CharField(max_length=10)
    ano = models.IntegerField()
    quota_estacoes_moveis = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"{self.operadora} - {self.trimestre} {self.ano}"

class TaxaPenetracao(models.Model):
    trimestre = models.CharField(max_length=10)
    ano = models.IntegerField()
    numero_estacoes = models.IntegerField()
    variacao = models.IntegerField()
    taxa_penetracao = models.DecimalField(max_digits=5, decimal_places=2)
    numero_estacoes_3g = models.IntegerField(null=True, blank=True)
    variacao_3g = models.IntegerField(null=True, blank=True)
    taxa_penetracao_3g = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    numero_estacoes_4g = models.IntegerField(null=True, blank=True)
    variacao_4g = models.IntegerField(null=True, blank=True)
    taxa_penetracao_4g = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f"{self.trimestre} {self.ano}"

class VolumeNegocio(models.Model):
    trimestre = models.CharField(max_length=10)
    ano = models.IntegerField()
    volume_mtn = models.DecimalField(max_digits=15, decimal_places=2)
    volume_orange = models.DecimalField(max_digits=15, decimal_places=2)

    def __str__(self):
        return f"{self.trimestre} {self.ano}"