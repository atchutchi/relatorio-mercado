from django.db.models.signals import post_save
from django.dispatch import receiver
from dados_anuais.models import DadosAnuais
from django.contrib.auth.models import User
from .models import Notification

@receiver(post_save, sender=DadosAnuais)
def create_indicator_notification(sender, instance, created, **kwargs):
    if created:
        message = f"Um novo indicador foi criado: {instance}"
    else:
        message = f"O indicador {instance} foi atualizado"
    
    for user in User.objects.all():
        Notification.objects.create(user=user, message=message)