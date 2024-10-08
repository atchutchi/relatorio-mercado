# Relatório do Mercado

### Link to the final page
- [Observatório do Mercado das Telecomunicação na Guiné-Bissau](https://observatorio-mercado-gw-ccc5b800c903.herokuapp.com/).

![ARN Logo]('/relatorio_mercado/media/arn-logo.png')

Relatório do Mercado é um site desenvolvido para a Autoridade Reguladora Nacional (ARN) da Guiné-Bissau. O site apresenta análises detalhadas e indicadores do mercado de telecomunicações do país, incluindo dados sobre estações móveis, emprego no setor, tráfego nacional, quotas de mercado, taxa de penetração e volume de negócios.

## Conteúdo

- [Funcionalidades](#funcionalidades)
- [Tecnologias Utilizadas](#tecnologias-utilizadas)
- [Instalação](#instalação)
- [Uso](#uso)
- [Créditos](#créditos)
- [Licença](#licença)

## Funcionalidades

- Visualização de dados do mercado de telecomunicações em gráficos interativos
- Análise detalhada de diversos indicadores do setor
- Comparação entre operadoras (MTN e Orange)
- Apresentação de relatórios trimestrais
- Interface responsiva para acesso em diferentes dispositivos

## Testing and Troubleshooting

During the development of this project, we encountered and resolved several issues. This document outlines these problems and their solutions for future reference.

### 1. UserProfile Redirect Issue

**Problem Description:**
After updating the user profile, the application raised an ImproperlyConfigured exception with the message "No URL to redirect to. Either provide a url or define a get_absolute_url method on the Model."

**Solution:**
We updated the UserProfileView to include a success_url:

```python
from django.urls import reverse_lazy

class UserProfileView(LoginRequiredMixin, UpdateView):
    model = UserProfile
    template_name = 'indicator_management/user_profile.html'
    fields = ['bio', 'organization']
    success_url = reverse_lazy('user_profile')

    def get_object(self, queryset=None):
        return UserProfile.objects.get_or_create(user=self.request.user)[0]
```

### 2. Template Does Not Exist Error
**Problem Description:**
When trying to access the indicator creation page, a TemplateDoesNotExist error was raised for 'indicator_management/indicator_create.html'.
**Solution:**
We ensured that the template file was created in the correct directory and updated the TEMPLATES setting in settings.py to include the indicator_management templates directory:

```python

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            # ... other directories ...
            os.path.join(BASE_DIR, 'indicator_management', 'templates'),
        ],
        'APP_DIRS': True,
        # ... rest of the configuration ...
    },
]
```

### 3. Data Not Passing to Templates
**Problem Description:**
Data was not being correctly passed to the templates, resulting in empty or incorrect displays.
**Solution:**
We reviewed and updated the view functions to ensure all necessary data was being passed to the context. For example, in the market analysis view:

```python
def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    # ... data processing ...
    context['market_share_data'] = json.dumps(market_share_data)
    context['hhi_data'] = json.dumps(hhi_data)
    # ... more context data ...
    return context
```

### 4. Responsive Design Issues
**Problem Description:**
The layout was not properly responsive, especially for tablet-sized screens.
**Solution:**
We updated the CSS to better handle different screen sizes:

```css
@media (min-width: 768px) and (max-width: 991px) {
    .container {
        max-width: 95%;
    }
    .chart-container {
        height: 300px;
    }
}
```

### 5. Template Syntax Error with Custom Filter

**Problem Description:**
Encountered a TemplateSyntaxError with the message "Invalid filter: 'replace'" when trying to use a custom template filter.

**Solution:**
Updated the custom filter in `custom_filters.py` to use the built-in `cut` filter in combination with our custom `replace_underscore` filter:

```python

@register.filter
def replace_underscore(value):
    return value.replace('_', ' ')

```
Usage in template:
```python
{{ campo|cut:'_atual'|replace_underscore|title }}
```

### 6. Recursion Error in Custom getattr Filter
**Problem Description:**
Encountered a RecursionError with the message "maximum recursion depth exceeded" when using a custom getattr filter.
**Solution:**
Renamed the custom getattr filter to avoid conflict with Python's built-in getattr function and simplified its implementation:

```python
@register.filter
def getattr_filter(obj, attr):
    return getattr(obj, attr)

```
Updated template usage:

```python
{{ dado|getattr_filter:campo|intcomma }}
```

### 7. Data Not Rendering in Evolution of Indicators View
**Problem Description:**
The evolution of indicators data was not being rendered correctly in the template.
**Solution:**
Refactored the evolucao_indicadores view to handle missing data and sum operator data when necessary. Also updated the corresponding template and JavaScript to correctly display the data:

Updated view to handle missing 'TOTAL' data and fallback to summing individual operator data.
Modified template to use the new data structure.
Updated JavaScript to create charts based on the new data format.

### 8. Inconsistent Data Presentation in Annual Data Page
**Problem Description:**
The annual data page was not presenting data in an easily understandable format, and there were concerns about calculation accuracy.
**Solution:**
Proposed a new structure for the annual data presentation, including:

Overview of the market with evolution of key indicators.
Annual comparison between operators.
Operator-specific evolution pages.
Market analysis with market share visualizations.
Detailed pages for specific indicator categories.
Growth report with year-over-year comparisons.
Overall sector panorama.
Interactive dashboard for custom data visualization.

Implementation of this solution involves updating models, views, templates, and JavaScript to ensure accurate calculations and clear data presentation.





## Tecnologias Utilizadas

- HTML
- CSS
- JavaScript
- Python
- Django
- Chart.js
- Bootstrap

## Instalação

1. Clone o repositório:

## Créditos