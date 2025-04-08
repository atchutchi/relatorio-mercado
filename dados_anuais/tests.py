from django.test import TestCase, Client
from django.urls import reverse
from .models import DadosAnuais, Operadora
from decimal import Decimal

# Create your tests here.

class ModelTestCase(TestCase):
    def setUp(self):
        # Criar operadoras para os testes
        self.mtn = Operadora.objects.create(nome='MTN', codigo='MTN123')
        self.orange = Operadora.objects.create(nome='ORANGE', codigo='ORG456')
        
        # Criar dados anuais para os testes
        self.dados_2022_mtn = DadosAnuais.objects.create(
            ano=2022,
            operadora=self.mtn,
            assinantes_rede_movel=1000000,
            receita_total=Decimal('1000000.00'),
            trafego_dados=500000
        )
        
        self.dados_2022_orange = DadosAnuais.objects.create(
            ano=2022,
            operadora=self.orange,
            assinantes_rede_movel=800000,
            receita_total=Decimal('800000.00'),
            trafego_dados=400000
        )
        
        self.dados_2021_mtn = DadosAnuais.objects.create(
            ano=2021,
            operadora=self.mtn,
            assinantes_rede_movel=900000,
            receita_total=Decimal('900000.00'),
            trafego_dados=400000
        )
        
        self.dados_2021_orange = DadosAnuais.objects.create(
            ano=2021,
            operadora=self.orange,
            assinantes_rede_movel=700000,
            receita_total=Decimal('700000.00'),
            trafego_dados=300000
        )
    
    def test_get_total_mercado(self):
        """Testa o método get_total_mercado"""
        total_assinantes_2022 = DadosAnuais.get_total_mercado(2022, 'assinantes_rede_movel')
        self.assertEqual(total_assinantes_2022, 1800000)
        
        total_receita_2022 = DadosAnuais.get_total_mercado(2022, 'receita_total')
        self.assertEqual(total_receita_2022, Decimal('1800000.00'))
    
    def test_operadora_model(self):
        """Testa o modelo Operadora"""
        self.assertEqual(str(self.mtn), 'MTN')
        self.assertEqual(self.mtn.codigo, 'MTN123')
    
    def test_dados_anuais_model(self):
        """Testa o modelo DadosAnuais"""
        self.assertEqual(self.dados_2022_mtn.ano, 2022)
        self.assertEqual(self.dados_2022_mtn.operadora, self.mtn)
        self.assertEqual(self.dados_2022_mtn.assinantes_rede_movel, 1000000)
    
    def test_get_anos_disponiveis(self):
        """Testa o método get_anos_disponiveis"""
        anos = list(DadosAnuais.get_anos_disponiveis())
        self.assertEqual(anos, [2021, 2022])
    
    def test_market_share(self):
        """Testa o cálculo de market share"""
        market_share_mtn = float(self.dados_2022_mtn.market_share_assinantes)
        self.assertAlmostEqual(market_share_mtn, 55.56, places=2)
        
        market_share_orange = float(self.dados_2022_orange.market_share_assinantes)
        self.assertAlmostEqual(market_share_orange, 44.44, places=2)

class ViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        # Criar operadoras para os testes
        self.mtn = Operadora.objects.create(nome='MTN', codigo='MTN123')
        self.orange = Operadora.objects.create(nome='ORANGE', codigo='ORG456')
        
        # Criar dados anuais para os testes
        self.dados_2022_mtn = DadosAnuais.objects.create(
            ano=2022,
            operadora=self.mtn,
            assinantes_rede_movel=1000000,
            receita_total=Decimal('1000000.00'),
            trafego_dados=500000,
            populacao_estimada=2000000
        )
        
        self.dados_2022_orange = DadosAnuais.objects.create(
            ano=2022,
            operadora=self.orange,
            assinantes_rede_movel=800000,
            receita_total=Decimal('800000.00'),
            trafego_dados=400000,
            populacao_estimada=2000000
        )
    
    def test_annual_report_view(self):
        """Testa a AnnualReportView"""
        response = self.client.get(reverse('annual_report'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dados_anuais/annual_report.html')
        self.assertIn('dados_mercado', response.context)
        self.assertIn('anos_disponiveis', response.context)
    
    def test_growth_report_view(self):
        """Testa a GrowthReportView"""
        response = self.client.get(reverse('growth_report'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dados_anuais/growth_report.html')
        self.assertIn('growth_data', response.context)
        self.assertIn('anos', response.context)
        self.assertIn('operadoras', response.context)
    
    def test_market_evolution_view(self):
        """Testa a MarketEvolutionView"""
        response = self.client.get(reverse('market_evolution'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dados_anuais/market_evolution.html')
        self.assertIn('evolution_data', response.context)
        self.assertIn('anos', response.context)
    
    def test_sector_panorama_view(self):
        """Testa a SectorPanoramaView"""
        response = self.client.get(reverse('sector_panorama'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dados_anuais/sector_panorama.html')
        self.assertIn('panorama_data', response.context)
        self.assertIn('anos', response.context)
        self.assertIn('operadoras', response.context)
