from django.urls import path
from . import views

urlpatterns = [
    path('', views.DadosAnuaisListView.as_view(), name='dados_anuais_list'),
    path('<int:ano>/<str:operadora>/', views.DadosAnuaisDetailView.as_view(), name='dados_anuais_detail'),
    path('comparacao/<int:ano>/', views.comparacao_operadoras, name='comparacao_operadoras'),
    path('evolucao/', views.evolucao_indicadores, name='evolucao_indicadores'),
]