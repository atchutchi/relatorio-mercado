from django.urls import path
from .views.estacoes_moveis import (
    EstacoesMoveisCreateView, 
    EstacoesMoveisListView, 
    EstacoesMoveisUpdateView, 
    EstacoesMoveisDeleteView,
    EstacoesMoveisDetailView
)

urlpatterns = [
    path('estacoes-moveis/', EstacoesMoveisListView.as_view(), name='estacoes_moveis_list'),
    path('estacoes-moveis/add/', EstacoesMoveisCreateView.as_view(), name='estacoes_moveis_add'),
    path('estacoes-moveis/<int:pk>/', EstacoesMoveisDetailView.as_view(), name='estacoes_moveis_detail'),
    path('estacoes-moveis/<int:pk>/edit/', EstacoesMoveisUpdateView.as_view(), name='estacoes_moveis_edit'),
    path('estacoes-moveis/<int:pk>/delete/', EstacoesMoveisDeleteView.as_view(), name='estacoes_moveis_delete'),
]