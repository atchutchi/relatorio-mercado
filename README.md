# Observatório do Mercado da Guiné-Bissau

### Link to the final page
- [Observatório do Mercado das Telecomunicação na Guiné-Bissau](https://observatorio-mercado-gw-ccc5b800c903.herokuapp.com/).

![ARN Logo](media/arn-logo.png)


## Overview
O Observatório do Mercado da Guiné-Bissau é uma plataforma desenvolvida para monitorizar e reportar dados económicos e de mercado no país. O site apresenta informações detalhadas sobre indicadores mensais e trimestrais, permitindo análises e visualizações que apoiam a tomada de decisões estratégicas.

## Strategy
O objetivo principal do Observatório do Mercado é centralizar informações económicas relevantes, garantindo acessibilidade e transparência para diferentes stakeholders, incluindo governos, empresas e investigadores.

## User Stories
- **Usuário Geral:**
  - Como um visitante do site, quero visualizar rapidamente os principais indicadores económicos para entender o estado atual do mercado.
  - Como um analista, quero personalizar a visualização de dados para identificar padrões e realizar análises detalhadas.
  - Como um usuário com dúvidas, quero poder interagir com um assistente virtual para obter informações rápidas sobre o mercado de telecomunicações.

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
- **Chatbot:** Assistente virtual para consultas rápidas sobre o mercado.

## Models
- **Indicadores Econômicos:** Modelos para armazenar dados mensais e trimestrais.
- **Usuários:** Gestão de acessos e permissões.
- **Relatórios:** Gerar e armazenar documentos de análise.

## Features
- **Homepage:**
  - Exibição dos principais indicadores económicos em gráficos.
  - Destaques de mudanças significativas no mercado.
  - Design moderno e responsivo.

- **Dashboard:**
  - Filtros para visualização personalizada de dados.
  - Gráficos interativos com opções de download.

- **Relatórios:**
  - Área de download de relatórios anuais e trimestrais.
  - Opção de solicitação de relatórios personalizados.

- **Admin Panel:**
  - Formulários para adicionar e atualizar dados económicos.
  - Gestão de usuários e permissões.

- **Chatbot:**
  - Assistente virtual integrado em todas as páginas.
  - Sugestões de perguntas frequentes sobre o mercado.
  - Interface intuitiva com animações de digitação.
  - Persistência de sessão para manter o histórico de conversas.
  - Capacidade de responder a consultas sobre dados de mercado, operadoras e relatórios disponíveis.
  - Busca automática de dados em tempo real no banco de dados da aplicação.
  - Respostas concisas e diretas, focadas apenas na informação solicitada.
  - Sistema de fallback com busca na web quando informações não estão disponíveis no banco.

## Testing and Troubleshooting

### Problemas Encontrados e Soluções

#### 1. Problemas de Layout e Interface
- **Problema**: Layout desorganizado com elementos sobrepostos, especialmente no cabeçalho e na navegação.
  - **Solução**: Reestruturação completa do HTML/CSS seguindo as melhores práticas do Bootstrap 5. Implementação de um sistema de grid responsivo e uso consistente de classes utilitárias.

- **Problema**: Incompatibilidade de estilo entre dispositivos móveis e desktop.
  - **Solução**: Criação de um sistema de design com variáveis CSS (`:root`) para garantir consistência visual. Implementação de media queries específicas para cada breakpoint.

- **Problema**: Sobreposição do conteúdo com o cabeçalho fixo.
  - **Solução**: Adição de `padding-top` ao body correspondente à altura do cabeçalho, com ajustes dinâmicos para diferentes tamanhos de tela.

#### 2. Problemas de Responsividade
- **Problema**: Menu de navegação quebrado em dispositivos móveis.
  - **Solução**: Criação de componentes específicos para dispositivos móveis (`mobile-top-header.html`) e implementação de lógica condicional para exibição baseada no tamanho da tela.

- **Problema**: Elementos UI muito grandes ou pequenos em diferentes dispositivos.
  - **Solução**: Implementação de tipografia responsiva e ajuste dos tamanhos de fonte, ícones e espaçamento usando unidades relativas (rem) e media queries.

#### 3. Problemas com JavaScript
- **Problema**: Variáveis sendo redeclaradas causando erros no console.
  - **Solução**: Utilização de `const` em vez de `let` para declarações que não mudam e implementação de um padrão IIFE (Immediately Invoked Function Expression) para evitar poluição do escopo global.

- **Problema**: Funcionalidades JavaScript não funcionando em alguns navegadores.
  - **Solução**: Adição de verificações de recursos (feature detection) e implementação de fallbacks para navegadores que não suportam recursos modernos.

- **Problema**: Conflitos com múltiplas declarações de variáveis de cores para gráficos.
  - **Solução**: Centralização das definições de cores em um único arquivo e uso de constantes para evitar redeclarações.

#### 4. Problemas de Carregamento de Dados
- **Problema**: Erros quando não há dados disponíveis para exibição.
  - **Solução**: Implementação de verificações robustas para `null`, `undefined` e objetos vazios. Adição de estados vazios (empty states) com mensagens informativas para o usuário.

- **Problema**: Dados inconsistentes entre diferentes visualizações.
  - **Solução**: Centralização da lógica de busca de dados e implementação de validação consistente em todo o aplicativo.

- **Problema**: Falhas ao renderizar relatórios para anos sem dados.
  - **Solução**: Aprimoramento da função `get_context_data()` para incluir verificações de anos disponíveis e implementação de mecanismos de fallback para utilizar o ano mais recente com dados.

#### 5. Problemas de Desempenho
- **Problema**: Carregamento lento de páginas com muitos elementos visuais.
  - **Solução**: Otimização de imagens, carregamento assíncrono de recursos não críticos, e implementação de lazy loading para conteúdo abaixo da dobra.

- **Problema**: Animações causando travamentos em dispositivos de baixo desempenho.
  - **Solução**: Simplificação de animações e uso da propriedade CSS `will-change` para elementos animados. Implementação de detecção de capacidade do dispositivo para ajustar a complexidade visual.

#### 6. Problemas com o Chatbot
- **Problema**: Conversas sendo reiniciadas ao navegar entre páginas.
  - **Solução**: Implementação de persistência de sessão utilizando sessionStorage para manter o histórico de conversas.

- **Problema**: Falta de feedback durante o processamento de mensagens.
  - **Solução**: Adição de animação de "digitando" e indicadores de carregamento para melhorar a experiência do usuário.

- **Problema**: Chatbot sem contexto específico sobre o mercado de telecomunicações.
  - **Solução**: Aprimoramento do sistema de prompts com informações específicas sobre o mercado da Guiné-Bissau, operadoras e indicadores-chave.

- **Problema**: Chatbot demasiado verboso com introduções longas e explicações desnecessárias.
  - **Solução**: Modificação do sistema de instruções e pós-processamento para garantir respostas diretas e concisas sem introduções verbosas.

- **Problema**: Respostas inconsistentes ou não baseadas em dados reais do mercado.
  - **Solução**: Implementação de um sistema de consulta ao banco de dados que busca informações atualizadas sobre assinantes, receitas, operadoras e tráfego diretamente das tabelas do sistema.

- **Problema**: Indisponibilidade de respostas quando a API do modelo de linguagem está inacessível.
  - **Solução**: Sistema de fallback em três camadas: primeiro busca no banco de dados, depois na API do modelo, e por fim realiza uma busca web para encontrar informações relevantes.

### Testes Realizados

#### Testes de Interface
- Verificação de consistência visual em diferentes navegadores (Chrome, Firefox, Safari, Edge).
- Testes de responsividade em múltiplos dispositivos e orientações (desktop, tablet, mobile).
- Verificação de acessibilidade usando ferramentas como WAVE e Lighthouse.
- Testes de contraste e legibilidade para garantir que todos os textos sejam facilmente lidos.

#### Testes Funcionais
- Verificação da funcionalidade de pesquisa e filtragem de dados.
- Testes das interações de usuário (cliques, hover, formulários).
- Validação da exibição correta de gráficos e visualizações de dados.
- Testes de navegação entre páginas e conservação de estados.
- Verificação do funcionamento correto de todos os links e botões.

#### Testes de Performance
- Análise de tempo de carregamento usando Chrome DevTools.
- Otimização de recursos estáticos (CSS, JavaScript, imagens).
- Verificação de performance em conexões lentas.
- Monitoramento do consumo de memória durante o uso intensivo.

#### Testes de Browser Compatibility
- Verificação de compatibilidade em diferentes navegadores e versões.
- Validação da experiência do usuário em diferentes sistemas operacionais.
- Testes em dispositivos com diferentes capacidades de processamento.

#### Testes do Chatbot
- Verificação da acurácia das respostas em diferentes cenários de consulta.
- Testes de robustez com entradas inesperadas ou malformadas.
- Verificação da persistência de sessão entre navegações.
- Validação da experiência do usuário com o efeito de digitação e animações.
- Testes de desempenho com conversas longas.

### Ferramentas Utilizadas para Testes
- Chrome DevTools para debugging e performance testing
- Lighthouse para auditorias de performance e acessibilidade
- Validators W3C para HTML e CSS
- ESLint para validação de JavaScript
- Django Debug Toolbar para análise de queries e performance do backend

## Future Development
- Desenvolvimento de modelos para introdução de dados mensais e trimestrais diretamente no sistema.
- Implementação de alertas automáticos para atualizações de indicadores.
- Expansão das capacidades do chatbot para incluir análises preditivas e recomendações.
- Aprimoramento da integração do chatbot com APIs externas para responder a consultas mais complexas.
- Análise de sentimento das interações com o chatbot para melhorar continuamente as respostas.
- Implementação de um sistema de feedback do usuário após cada interação com o chatbot.
- Integração com APIs de outros serviços de telecomunicações para dados em tempo real.
- Implementação de um sistema de notificações personalizáveis para usuários cadastrados.

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
- **AI Integration:**
  - Hugging Face API para o assistente virtual (chatbot) utilizando o modelo Mistral-7B-Instruct.
  - Implementação híbrida com consultas ao banco de dados e busca web como fallback.
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
   - Para o chatbot, adicione a variável `OPENAI_API_KEY` com sua chave da API OpenAI.

5. **Database Migration**
   - Atualize `settings.py` com as configurações do banco de dados e realize as migrações.

6. **Static and Media Files Configuration**
   - Configure um bucket S3 na Amazon AWS.
   - Atualize `settings.py` e `env.py` com os detalhes do bucket.

7. **Disable Collectstatic**
   - Temporariamente adicione `DISABLE_COLLECTSTATIC=1` no Config Vars do Heroku.

8. **Dependencies**
   - Garanta que todos os pacotes necessários estão listados em `requirements.txt`.
   - Adicione `huggingface_hub`, `requests` e `beautifulsoup4` à lista de dependências para o chatbot aprimorado.

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
