from django.db import models
from django.contrib.auth.models import User
from dados_anuais.models import DadosAnuais

class IndicatorUpdate(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    dados_anuais = models.ForeignKey(DadosAnuais, on_delete=models.CASCADE)
    field_name = models.CharField(max_length=100)
    old_value = models.TextField()
    new_value = models.TextField()
    updated_at = models.DateTimeField(auto_now_add=True)

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    organization = models.CharField(max_length=100, blank=True)

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)