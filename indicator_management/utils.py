from .models import Notification

def create_notification(user, message):
    Notification.objects.create(user=user, message=message)

def notify_all_users(message, exclude_user=None):
    from django.contrib.auth.models import User
    users = User.objects.all()
    if exclude_user:
        users = users.exclude(id=exclude_user.id)
    for user in users:
        create_notification(user, message)