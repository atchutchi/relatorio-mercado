from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from .models import IndicatorUpdate, UserProfile, Notification
from dados_anuais.models import DadosAnuais
from django.shortcuts import get_object_or_404
from django.http import HttpResponse

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
    success_url = reverse_lazy('user_profile')

    def get_object(self, queryset=None):
        return UserProfile.objects.get_or_create(user=self.request.user)[0]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        return context


class NotificationListView(LoginRequiredMixin, ListView):
    model = Notification
    template_name = 'indicator_management/notification_list.html'
    context_object_name = 'notifications'

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user).order_by('-created_at')


class IndicatorCreateView(LoginRequiredMixin, CreateView):
    model = DadosAnuais
    template_name = 'indicator_management/indicator_create.html'
    fields = '__all__'
    success_url = reverse_lazy('indicator_list')


# indicator_management/views.py

from django.http import HttpResponse

class IndicatorImportView(LoginRequiredMixin, ListView):
    template_name = 'indicator_management/indicator_import.html'

    def get(self, request, *args, **kwargs):
        # Adicione aqui o seu código de importação, por enquanto retornamos uma resposta simples
        return HttpResponse("Página de importação de indicadores.")

class IndicatorExportView(LoginRequiredMixin, ListView):
    def get(self, request, *args, **kwargs):
        # Adicione aqui o seu código de exportação, por enquanto retornamos uma resposta simples
        return HttpResponse("Página de exportação de indicadores.")


class IndicatorDeleteView(LoginRequiredMixin, DeleteView):
    model = DadosAnuais
    template_name = 'indicator_management/indicator_confirm_delete.html'
    success_url = reverse_lazy('indicator_list')  # Redireciona de volta para a lista de indicadores após a exclusão