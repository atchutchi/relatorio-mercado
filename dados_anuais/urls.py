# dados_anuais/urls.py

from django.urls import path
from .views.market_overview import MarketOverviewView
from .views.annual_comparison import AnnualComparisonView
from .views.operator_evolution import OperatorEvolutionView
from .views.market_analysis import MarketAnalysisView
from .views.growth_report import GrowthReportView
from .views.sector_panorama import SectorPanoramaView
from .views.market_evolution import MarketEvolutionView
from .views.annual_report import AnnualReportView

app_name = 'dados_anuais'

urlpatterns = [
    # Relatório Anual Principal
    path('relatorio-anual/', AnnualReportView.as_view(), name='annual_report'),
    
    # Visões Específicas do Mercado
    path('visao-geral/', MarketOverviewView.as_view(), name='market_overview'),
    path('evolucao/', MarketEvolutionView.as_view(), name='market_evolution'),
    path('comparacao-anual/', AnnualComparisonView.as_view(), name='annual_comparison'),
    path('analise/', MarketAnalysisView.as_view(), name='market_analysis'),
    
    # Análises por Operadora
    path('operadora/<str:operadora>/', OperatorEvolutionView.as_view(), name='operator_evolution'),
    path('operadora/mtn/', OperatorEvolutionView.as_view(), {'operadora': 'MTN'}, name='mtn_evolution'),
    path('operadora/orange/', OperatorEvolutionView.as_view(), {'operadora': 'ORANGE'}, name='orange_evolution'),
    
    # Relatórios Específicos
    path('crescimento/', GrowthReportView.as_view(), name='growth_report'),
    path('panorama/', SectorPanoramaView.as_view(), name='sector_panorama'),
    
    # Downloads
    path('relatorio-anual/download/pdf/', AnnualReportView.as_view(), {'format': 'pdf'}, name='annual_report_pdf'),
    path('relatorio-anual/download/word/', AnnualReportView.as_view(), {'format': 'word'}, name='annual_report_word'),
]