from django.urls import path
from .views.market_overview import MarketOverviewView
from .views.annual_comparison import AnnualComparisonView

urlpatterns = [
    path('market-overview/', MarketOverviewView.as_view(), name='market_overview'),
    path('annual-comparison/', AnnualComparisonView.as_view(), name='annual_comparison'),
]