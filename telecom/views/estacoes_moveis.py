from django.views.generic import CreateView, ListView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy
from ..models.estacoes_moveis import EstacoesMoveisIndicador
from ..forms import EstacoesMoveisForm

class EstacoesMoveisCreateView(CreateView):
    model = EstacoesMoveisIndicador
    form_class = EstacoesMoveisForm  # Use esta linha em vez de get_form_class
    template_name = 'telecom/estacoes_moveis_form.html'
    success_url = reverse_lazy('estacoes_moveis_list')

class EstacoesMoveisListView(ListView):
    model = EstacoesMoveisIndicador
    template_name = 'telecom/estacoes_moveis_list.html'
    context_object_name = 'estacoes_moveis_list'

class EstacoesMoveisUpdateView(UpdateView):
    model = EstacoesMoveisIndicador
    form_class = EstacoesMoveisForm  # Use esta linha em vez de get_form_class
    template_name = 'telecom/estacoes_moveis_form.html'
    success_url = reverse_lazy('estacoes_moveis_list')

class EstacoesMoveisDeleteView(DeleteView):
    model = EstacoesMoveisIndicador
    template_name = 'telecom/estacoes_moveis_confirm_delete.html'
    success_url = reverse_lazy('estacoes_moveis_list')

class EstacoesMoveisDetailView(DetailView):
    model = EstacoesMoveisIndicador
    template_name = 'telecom/estacoes_moveis_detail.html'
    context_object_name = 'indicador'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        indicador = self.get_object()
        context['total_utilizadores'] = indicador.total_utilizadores
        context['total_carregamentos'] = indicador.total_carregamentos
        context['total_levantamentos'] = indicador.total_levantamentos
        context['total_transferencias'] = indicador.total_transferencias
        return context
