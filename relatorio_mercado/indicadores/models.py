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
    
    # Chamadas Originadas
    on_net = models.BigIntegerField(verbose_name="On-net", default=0)
    off_net = models.BigIntegerField(verbose_name="Off-net (saída)", default=0)
    saida_internacional = models.BigIntegerField(verbose_name="Saída Internacional", default=0)
    
    # Chamadas Terminadas
    off_net_entrada = models.BigIntegerField(verbose_name="Off-net (entrada)", default=0)
    entrada_internacional = models.BigIntegerField(verbose_name="Entrada Internacional", default=0)
    
    # Roaming
    roaming_in = models.BigIntegerField(verbose_name="Roaming in", default=0)
    roaming_out = models.BigIntegerField(verbose_name="Roaming out", default=0)

    @property
    def total_originadas(self):
        return self.on_net + self.off_net + self.saida_internacional

    @property
    def total_terminadas(self):
        return self.off_net_entrada + self.entrada_internacional

    @property
    def total_roaming(self):
        return self.roaming_in + self.roaming_out

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

from django.db import models

class VolumeNegocio(models.Model):
    # Campo para armazenar o trimestre (ex: "Q1", "Q2", etc.)
    trimestre = models.CharField(max_length=10)

    # Campo para armazenar o ano
    ano = models.IntegerField()

    # Percentagem de volume de negócios da MTN (0-100%)
    percentagem_mtn = models.DecimalField(max_digits=5, decimal_places=2, default=0)

    # Percentagem de volume de negócios da Orange (0-100%)
    percentagem_orange = models.DecimalField(max_digits=5, decimal_places=2, default=0)

    # Volume global de negócios (soma dos volumes da MTN e Orange)
    volume_global = models.DecimalField(max_digits=15, decimal_places=2, default=0)

    # Volume de negócios da MTN
    volume_mtn = models.DecimalField(max_digits=15, decimal_places=2, default=0)

    # Volume de negócios da Orange
    volume_orange = models.DecimalField(max_digits=15, decimal_places=2, default=0)

    def __str__(self):
        # Representação string do objeto (ex: "Q1 2024")
        return f"{self.trimestre} {self.ano}"

    def save(self, *args, **kwargs):
        # Calcula o volume global se não estiver definido
        if not self.volume_global:
            self.volume_global = self.volume_mtn + self.volume_orange

        # Calcula as percentagens se o volume global for maior que zero
        if self.volume_global > 0:
            # Calcula a percentagem da MTN
            self.percentagem_mtn = (self.volume_mtn / self.volume_global) * 100
            # Calcula a percentagem da Orange
            self.percentagem_orange = (self.volume_orange / self.volume_global) * 100

        # Chama o método save() da superclasse para salvar o objeto
        super().save(*args, **kwargs)