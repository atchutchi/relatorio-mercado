from django import forms
from ..models.estacoes_moveis import EstacoesMoveisIndicador

class EstacoesMoveisForm(forms.ModelForm):
    class Meta:
        model = EstacoesMoveisIndicador
        fields = '__all__'
        widgets = {
            'ano': forms.NumberInput(attrs={'class': 'form-control'}),
            'mes': forms.Select(attrs={'class': 'form-control'}),
            'afectos_planos_pos_pagos': forms.NumberInput(attrs={'class': 'form-control'}),
            'afectos_planos_pos_pagos_utilizacao': forms.NumberInput(attrs={'class': 'form-control'}),
            'afectos_planos_pre_pagos': forms.NumberInput(attrs={'class': 'form-control'}),
            'afectos_planos_pre_pagos_utilizacao': forms.NumberInput(attrs={'class': 'form-control'}),
            'associados_situacoes_especificas': forms.NumberInput(attrs={'class': 'form-control'}),
            'outros_residuais': forms.NumberInput(attrs={'class': 'form-control'}),
            'sms': forms.NumberInput(attrs={'class': 'form-control'}),
            'mms': forms.NumberInput(attrs={'class': 'form-control'}),
            'mobile_tv': forms.NumberInput(attrs={'class': 'form-control'}),
            'roaming_internacional_out_parc_roaming_out': forms.NumberInput(attrs={'class': 'form-control'}),
            'banda_larga_movel_3g_4g': forms.NumberInput(attrs={'class': 'form-control'}),
            'utilizadores_5g_upgrades': forms.NumberInput(attrs={'class': 'form-control'}),
            'utilizadores_servico_acesso_internet_banda_larga': forms.NumberInput(attrs={'class': 'form-control'}),
            'utilizadores_placas_box': forms.NumberInput(attrs={'class': 'form-control'}),
            'utilizadores_placas_usb': forms.NumberInput(attrs={'class': 'form-control'}),
            'utilizadores_servico_4g': forms.NumberInput(attrs={'class': 'form-control'}),
            'utilizadores_servico_banda_larga': forms.NumberInput(attrs={'class': 'form-control'}),
            'utilizadores_placas_box_banda_larga': forms.NumberInput(attrs={'class': 'form-control'}),
            'utilizadores_placas_usb_banda_larga': forms.NumberInput(attrs={'class': 'form-control'}),
            'numero_utilizadores_mulher': forms.NumberInput(attrs={'class': 'form-control'}),
            'numero_utilizadores_homem': forms.NumberInput(attrs={'class': 'form-control'}),
            'total_carregamentos_mulher': forms.NumberInput(attrs={'class': 'form-control'}),
            'total_carregamentos_homem': forms.NumberInput(attrs={'class': 'form-control'}),
            'total_levantamentos_mulher': forms.NumberInput(attrs={'class': 'form-control'}),
            'total_levantamentos_homem': forms.NumberInput(attrs={'class': 'form-control'}),
            'total_transferencias_mulher': forms.NumberInput(attrs={'class': 'form-control'}),
            'total_transferencias_homem': forms.NumberInput(attrs={'class': 'form-control'}),
        }