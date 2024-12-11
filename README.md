# Observatório do Mercado da Guiné-Bissau

### Link to the final page
- [Observatório do Mercado das Telecomunicação na Guiné-Bissau](https://observatorio-mercado-gw-ccc5b800c903.herokuapp.com/).

![ARN Logo]('')


## Overview
O Observatório do Mercado da Guiné-Bissau é uma plataforma desenvolvida para monitorizar e reportar dados económicos e de mercado no país. O site apresenta informações detalhadas sobre indicadores mensais e trimestrais, permitindo análises e visualizações que apoiam a tomada de decisões estratégicas.

## Strategy
O objetivo principal do Observatório do Mercado é centralizar informações económicas relevantes, garantindo acessibilidade e transparência para diferentes stakeholders, incluindo governos, empresas e investigadores.

## User Stories
- **Usuário Geral:**
  - Como um visitante do site, quero visualizar rapidamente os principais indicadores económicos para entender o estado atual do mercado.
  - Como um analista, quero personalizar a visualização de dados para identificar padrões e realizar análises detalhadas.

- **Administrador:**
  - Como administrador, quero uma interface intuitiva para introduzir dados mensais e trimestrais, garantindo que a plataforma esteja sempre atualizada.
  - Como administrador, quero gerenciar permissões de usuários para controlar o acesso às funcionalidades administrativas.

- **Investigador:**
  - Como investigador, quero exportar relatórios em diferentes formatos (PDF, Excel) para usá-los em análises externas.
  - Como investigador, quero acessar dados históricos organizados para comparar tendências ao longo dos anos.

## Skeleton
- **Homepage:** Visão geral dos principais indicadores.
- **Dashboard:** Painel interativo para filtrar e visualizar dados.
- **Relatórios:** Página para download de relatórios.
- **Admin Panel:** Interface para introdução e gestão de dados.

## Models
- **Indicadores Econômicos:** Modelos para armazenar dados mensais e trimestrais.
- **Usuários:** Gestão de acessos e permissões.
- **Relatórios:** Gerar e armazenar documentos de análise.

## Features
- **Homepage:**
  - Exibição dos principais indicadores económicos em gráficos.
  - Destaques de mudanças significativas no mercado.

- **Dashboard:**
  - Filtros para visualização personalizada de dados.
  - Gráficos interativos com opções de download.

- **Relatórios:**
  - Área de download de relatórios anuais e trimestrais.
  - Opção de solicitação de relatórios personalizados.

- **Admin Panel:**
  - Formulários para adicionar e atualizar dados económicos.
  - Gestão de usuários e permissões.

## Testing and Troubleshooting
### Estrutura (dados fornecidos posteriormente)
- Testes de unidade para modelos e funcionalidades principais.
- Testes de integração para fluxos de trabalho completos.

## Future Development
- Desenvolvimento de modelos para introdução de dados mensais e trimestrais diretamente no sistema.
- Implementação de alertas automáticos para atualizações de indicadores.

## Validator Testing
- Validação HTML, CSS, e JS.
- Validação de dados no backend (detalhes fornecidos posteriormente).

## Credits
- **Code:**
  - Desenvolvido por Atchutchi Ferreira.
- **Storage:**
  - Amazon AWS S3 para armazenamento de arquivos estáticos e media.
- **Database:**
  - ElephantSQL.
- **Language Used:**
  - Python Django, HTML, CSS, JavaScript.
- **Deployment:**
  - Heroku.

## Heroku Deployment Steps
1. **Sign Up or Log In to Heroku**
   - Acesse o site da Heroku e faça login ou crie uma conta.

2. **Create a New App**
   - No Dashboard, crie uma nova aplicação com um nome único e selecione a região mais próxima.

3. **Configuration**
   - Navegue para a aba Settings e configure as variáveis de ambiente, incluindo `DATABASE_URL` fornecido pela ElephantSQL.

4. **Environment Variables**
   - Crie um arquivo `env.py` e defina as variáveis necessárias como `DATABASE_URL` e `SECRET_KEY`.
   - Adicione as variáveis ao Config Vars no Heroku.

5. **Database Migration**
   - Atualize `settings.py` com as configurações do banco de dados e realize as migrações.

6. **Static and Media Files Configuration**
   - Configure um bucket S3 na Amazon AWS.
   - Atualize `settings.py` e `env.py` com os detalhes do bucket.

7. **Disable Collectstatic**
   - Temporariamente adicione `DISABLE_COLLECTSTATIC=1` no Config Vars do Heroku.

8. **Dependencies**
   - Garanta que todos os pacotes necessários estão listados em `requirements.txt`.

9. **Application Settings**
   - Configure `ALLOWED_HOSTS` e outros parâmetros no `settings.py`.

10. **Procfile**
    - Crie um arquivo `Procfile` com o comando para rodar a aplicação: `web: gunicorn your_project_name.wsgi`.

11. **Version Control**
    - Faça commit e push das alterações no GitHub.

12. **Heroku Deployment**
    - Realize o deploy manual no Heroku e monitore os logs de build.

## DATABASES
- **ElephantSQL**: Usado como solução de banco de dados em nuvem para Django.
