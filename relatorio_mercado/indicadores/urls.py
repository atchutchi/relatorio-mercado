from django.urls import path
from .views import EstacoesMoveisView, EmpregoSetorView, TrafegoNacionalView, QuotaMercadoView, TaxaPenetracaoView, VolumeNegocioView, MercadoTelefoniaMovelView

urlpatterns = [
    path('estacoes-moveis/', EstacoesMoveisView.as_view(), name='estacoes_moveis'),
    path('emprego-setor/', EmpregoSetorView.as_view(), name='emprego_setor'),
    path('trafego-nacional/', TrafegoNacionalView.as_view(), name='trafego_nacional'),
    path('quota-mercado/', QuotaMercadoView.as_view(), name='quota_mercado'),
    path('taxa-penetracao/', TaxaPenetracaoView.as_view(), name='taxa_penetracao'),
    path('volume-negocio/', VolumeNegocioView.as_view(), name='volume_negocio'),
    path('mercado-de-telefonia-movel/', MercadoTelefoniaMovelView.as_view(), name='mercado_de_telefonia_movel'),
]