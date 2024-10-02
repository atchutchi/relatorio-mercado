from django.urls import path
from .views.market_overview import MarketOverviewView
from .views.annual_comparison import AnnualComparisonView
from .views.operator_evolution import OperatorEvolutionView
from .views.market_analysis import MarketAnalysisView

urlpatterns = [
    path('market-overview/', MarketOverviewView.as_view(), name='market_overview'),
    path('annual-comparison/', AnnualComparisonView.as_view(), name='annual_comparison'),
    path('operator-evolution/<str:operadora>/', OperatorEvolutionView.as_view(), name='operator_evolution'),
    path('market-analysis/', MarketAnalysisView.as_view(), name='market_analysis'),
]