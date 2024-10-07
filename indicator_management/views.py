from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import IndicatorUpdate, UserProfile, Notification
from dados_anuais.models import DadosAnuais

class IndicatorListView(LoginRequiredMixin, ListView):
    model = DadosAnuais
    template_name = 'indicator_management/indicator_list.html'
    context_object_name = 'indicators'

class IndicatorUpdateView(LoginRequiredMixin, UpdateView):
    model = DadosAnuais
    template_name = 'indicator_management/indicator_update.html'
    fields = '__all__'

    def form_valid(self, form):
        response = super().form_valid(form)
        for field in form.changed_data:
            IndicatorUpdate.objects.create(
                user=self.request.user,
                dados_anuais=self.object,
                field_name=field,
                old_value=form.initial[field],
                new_value=form.cleaned_data[field]
            )
        
        # Criar notificação para todos os usuários (exceto o que fez a atualização)
        message = f"O indicador {self.object} foi atualizado por {self.request.user}"
        for user in User.objects.exclude(id=self.request.user.id):
            Notification.objects.create(user=user, message=message)

        return response

class UserProfileView(LoginRequiredMixin, UpdateView):
    model = UserProfile
    template_name = 'indicator_management/user_profile.html'
    fields = ['bio', 'organization']

class NotificationListView(LoginRequiredMixin, ListView):
    model = Notification
    template_name = 'indicator_management/notification_list.html'
    context_object_name = 'notifications'

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user).order_by('-created_at')