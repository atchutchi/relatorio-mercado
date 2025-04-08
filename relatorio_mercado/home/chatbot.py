import os
import json
import logging
import re
from typing import Optional, Dict, List, Any
from django.conf import settings
from django.core.cache import cache
from django.db.models import Q

# Importações para Hugging Face
from huggingface_hub import InferenceClient

# Importar modelos de dados (adicione conforme necessário)
from dados_anuais.models import DadosAnuais

# Importação para buscas web
import requests
from bs4 import BeautifulSoup

# Configurar logging
logger = logging.getLogger(__name__)

class Chatbot:
    """
    Classe para gerenciar a comunicação com a API da Hugging Face
    com foco no Observatório do Mercado de Telecomunicações
    """
    def __init__(self):
        # Configurar o token da API
        self.api_token = settings.HUGGINGFACE_API_TOKEN
        
        # Definir o modelo a ser usado
        self.model = "mistralai/Mistral-7B-Instruct-v0.2"  # Bom modelo multilíngue com suporte a português
        self.max_tokens = 1000
        self.temperature = 0.7
        
        # Prefixo para a chave de cache
        self.cache_prefix = "chatbot_session_"
        
        # Contexto do sistema para o chatbot
        self.system_message = """
        Você é um assistente do Observatório do Mercado de Telecomunicações da Guiné-Bissau.
        
        IMPORTANTE:
        1. Seja amigável e natural nas respostas, como uma conversa normal
        2. Responda saudações de forma educada e breve
        3. Evite introduções muito longas, mas não seja extremamente direto
        4. Use um tom cordial e profissional
        
        Informações principais:
        - Operadoras: MTN e Orange
        - Penetração móvel: 95.8%
        - Assinantes: 2.3 milhões
        - Receita anual: 128 bilhões XOF
        
        Responda sempre em português, de forma profissional e acessível.
        """
        
        # Inicializar histórico de mensagens
        self.reset_conversation()
    
    def get_session_id(self, session_id: Optional[str] = None) -> str:
        """
        Obtém ou gera um ID de sessão para o usuário
        
        Args:
            session_id: ID de sessão existente, se disponível
            
        Returns:
            str: ID de sessão a ser usado
        """
        if not session_id:
            # Gerar um ID único se não for fornecido
            import uuid
            session_id = str(uuid.uuid4())
        
        return session_id
    
    def get_conversation_history(self, session_id: str) -> List[Dict[str, str]]:
        """
        Recupera o histórico de conversa do cache
        
        Args:
            session_id: ID da sessão do usuário
            
        Returns:
            List[Dict[str, str]]: Histórico de conversa ou novo histórico se não existir
        """
        cache_key = f"{self.cache_prefix}{session_id}"
        history = cache.get(cache_key)
        
        if not history:
            # Iniciar nova conversa se não existir no cache
            history = [{"role": "system", "content": self.system_message}]
        
        return history
    
    def save_conversation_history(self, session_id: str, history: List[Dict[str, str]]) -> None:
        """
        Salva o histórico de conversa no cache
        
        Args:
            session_id: ID da sessão do usuário
            history: Histórico de conversa atualizado
        """
        cache_key = f"{self.cache_prefix}{session_id}"
        # Salvar por 30 minutos
        cache.set(cache_key, history, 60 * 30)
    
    def reset_conversation(self, session_id: Optional[str] = None) -> None:
        """
        Reinicia o histórico da conversa
        
        Args:
            session_id: ID da sessão do usuário (opcional)
        """
        if session_id:
            cache_key = f"{self.cache_prefix}{session_id}"
            # Limpar o cache para esta sessão
            cache.delete(cache_key)
        
        # Restaurar conversa padrão
        self.conversation_history = [
            {"role": "system", "content": self.system_message}
        ]
    
    def get_response(self, user_message: str, session_id: str = None) -> Dict[str, Any]:
        """
        Processa a mensagem do usuário e retorna uma resposta do assistente

        Args:
            user_message: Mensagem enviada pelo usuário
            session_id: ID da sessão

        Returns:
            Dict: Resposta formatada com a mensagem do assistente
        """
        try:
            # Verificar se o usuário enviou uma mensagem vazia
            if not user_message or not user_message.strip():
                return self._handle_error("Por favor, digite uma mensagem válida.", "empty_message")

            # Normalizar session_id para garantir que seja uma string válida
            if not session_id:
                session_id = str(uuid.uuid4())

            # Gerar novo ID se for uma string vazia
            if session_id.strip() == "":
                session_id = str(uuid.uuid4())

            # Obter histórico de conversa atual
            conversation_history = self.get_conversation_history(session_id)

            # Verificar se é uma saudação simples
            saudacoes = ["ola", "olá", "oi", "bom dia", "boa tarde", "boa noite", "boas", "hey", "hi", "hello"]
            is_greeting = user_message.lower().strip() in saudacoes or any(user_message.lower().startswith(s + " ") for s in saudacoes)
            
            if is_greeting:
                # Responder com uma saudação amigável
                import random
                greeting_responses = [
                    "Olá! Como posso ajudar com informações sobre o mercado de telecomunicações da Guiné-Bissau?",
                    "Oi! Em que posso ajudar hoje?",
                    "Olá! Precisa de alguma informação sobre o mercado de telecomunicações?",
                    "Boas! Como posso ser útil?"
                ]
                response = random.choice(greeting_responses)
                
                # Adicionar à conversa
                conversation_history.append({"role": "user", "content": user_message})
                conversation_history.append({"role": "assistant", "content": response})
                self.save_conversation_history(session_id, conversation_history)
                
                return {
                    "message": response,
                    "session_id": session_id,
                    "status": "success"
                }

            # Verificar configuração de API
            if not self.api_token:
                logger.warning("API key não configurada. Usando respostas locais.")
                return self._get_fallback_response(user_message, session_id, "api_key_missing")

            # Primeiro, tentar buscar dados específicos no banco
            database_response = self._search_database(user_message)
            
            if database_response:
                # Adicionar pergunta e resposta ao histórico
                conversation_history.append({"role": "user", "content": user_message})
                conversation_history.append({"role": "assistant", "content": database_response})
                self.save_conversation_history(session_id, conversation_history)
                
                return {
                    "message": database_response,
                    "session_id": session_id,
                    "status": "success",
                    "source": "database"
                }

            # Se não encontrou no banco, usar API Hugging Face
            # Adicionar mensagem do usuário ao histórico
            conversation_history.append({"role": "user", "content": user_message})
            
            logger.info(f"Enviando solicitação para API Hugging Face: {len(conversation_history)} mensagens")
            
            try:
                # Formatar histórico para o formato do modelo
                formatted_prompt = self._format_history_for_mistral(conversation_history)
                
                # Criar cliente de inferência
                client = InferenceClient(model=self.model, token=self.api_token)
                
                # Informar ao modelo sobre informações encontradas no banco
                if database_response:
                    formatted_prompt += f"\n\n[INST] Informações encontradas no banco de dados: {database_response} [/INST]"
                
                # Fazer chamada à API
                response = client.text_generation(
                    formatted_prompt,
                    max_new_tokens=self.max_tokens,
                    temperature=self.temperature,
                    do_sample=True,
                )
                
                # Processar a resposta para extrair apenas a parte relevante
                assistant_message = self._process_mistral_response(response)
                
                # Adicionar resposta ao histórico
                conversation_history.append({"role": "assistant", "content": assistant_message})
                
                # Salvar conversa atualizada
                self.save_conversation_history(session_id, conversation_history)
                
                # Atualizar histórico local também
                self.conversation_history = conversation_history
                
                # Retornar resposta formatada
                return {
                    "message": assistant_message,
                    "session_id": session_id,
                    "status": "success"
                }
                
            except Exception as e:
                logger.error(f"Erro na API Hugging Face: {str(e)}", exc_info=True)
                # Se houver qualquer erro com a API, usar o fallback
                return self._get_fallback_response(user_message, session_id, "api_error")
                
        except Exception as e:
            # Log do erro genérico
            logger.error(f"Erro ao comunicar com a API: {str(e)}", exc_info=True)
            return self._handle_error("Não foi possível processar sua pergunta. Tente novamente mais tarde.", "general_error")
    
    def _format_history_for_mistral(self, history: List[Dict[str, str]]) -> str:
        """
        Formata o histórico de conversa para o formato esperado pelo modelo Mistral
        
        Args:
            history: Histórico de conversa
            
        Returns:
            str: Prompt formatado para o modelo
        """
        formatted_prompt = ""
        
        # Adicionar mensagem do sistema no início
        system_content = ""
        for msg in history:
            if msg["role"] == "system":
                system_content = msg["content"]
                break
        
        # Iniciar com instruções do sistema
        formatted_prompt = f"<s>[INST] {system_content} [/INST]</s>\n\n"
        
        # Adicionar histórico de conversas (exceto sistema)
        for i, msg in enumerate(history):
            if msg["role"] == "system":
                continue
                
            if msg["role"] == "user":
                formatted_prompt += f"<s>[INST] {msg['content']} [/INST]"
            elif msg["role"] == "assistant" and i < len(history) - 1:  # Não adicionar a última resposta (que acabamos de gerar)
                formatted_prompt += f" {msg['content']}</s>\n\n"
        
        return formatted_prompt
    
    def _process_mistral_response(self, response: str) -> str:
        """
        Processa a resposta bruta do modelo para extrair apenas a parte relevante
        
        Args:
            response: Resposta completa do modelo
            
        Returns:
            str: Texto processado da resposta
        """
        # Remover qualquer tag de formatação que o modelo possa ter incluído
        clean_response = response.replace("<s>", "").replace("</s>", "").replace("[INST]", "").replace("[/INST]", "")
        
        # Remover qualquer texto que pareça ser uma instrução ou repetição da pergunta
        lines = clean_response.split("\n")
        filtered_lines = []
        for line in lines:
            if not line.strip():
                continue
            filtered_lines.append(line)
        
        result = "\n".join(filtered_lines).strip()
        
        # Lista de introduções extremamente verbosas para remover (reduzida)
        intro_patterns = [
            "Como assistente do Observatório do Mercado de Telecomunicações da Guiné-Bissau, posso informar que",
            "Como assistente virtual do Observatório do Mercado de Telecomunicações da Guiné-Bissau, devo mencionar que",
            "Gostaria de informar que, como assistente do Observatório,"
        ]
        
        # Remover apenas introduções muito longas
        for pattern in intro_patterns:
            if result.startswith(pattern):
                # Remover a introdução e começar com a primeira letra maiúscula
                parts = result.split(".", 1)
                if len(parts) > 1 and parts[1].strip():
                    result = parts[1].strip()
                    if result and result[0].islower():
                        result = result[0].upper() + result[1:]
        
        # Limitar tamanho da resposta para evitar verbosidade excessiva, mas não tão agressivamente
        if len(result.split()) > 150:  # Aumentado de 100 para 150 palavras
            # Tentar reduzir para as primeiras frases mais importantes, mas manter mais conteúdo
            sentences = result.split(". ")
            if len(sentences) > 5:  # Aumentado de 3 para 5 frases
                result = ". ".join(sentences[:5]) + "."
        
        return result
    
    def _get_fallback_response(self, user_message: str, session_id: str, error_type: str) -> Dict[str, Any]:
        """
        Gera uma resposta local simples quando a API não está disponível
        
        Args:
            user_message: Mensagem do usuário
            session_id: ID da sessão
            error_type: Tipo do erro que causou o fallback
            
        Returns:
            Dict: Resposta formatada com mensagem gerada localmente
        """
        # Verificar por palavras-chave na mensagem do usuário para tentar fornecer uma resposta útil
        user_query = user_message.lower()
        
        # Detectar saudações
        saudacoes = ["ola", "olá", "oi", "bom dia", "boa tarde", "boa noite", "boas", "hey", "hi", "hello"]
        if any(user_query.strip() == saudacao for saudacao in saudacoes):
            saudacao_respostas = [
                "Olá! Como posso ajudar com informações sobre o mercado de telecomunicações da Guiné-Bissau?",
                "Oi! Em que posso ajudar hoje?",
                "Olá! Precisa de alguma informação sobre o mercado de telecomunicações?",
                "Boas! Como posso ser útil?"
            ]
            import random
            return {
                "message": random.choice(saudacao_respostas),
                "session_id": session_id,
                "status": "success",
                "using_fallback": True
            }
        
        # Respostas pré-definidas para consultas comuns
        if "taxa de penetração" in user_query or "penetração móvel" in user_query:
            response = "A taxa de penetração móvel na Guiné-Bissau atualmente é de 95.8%. Isso representa um mercado bastante desenvolvido para o contexto regional."
        
        elif "assinantes" in user_query or "subscritores" in user_query:
            response = "O mercado de telecomunicações da Guiné-Bissau conta com aproximadamente 2.3 milhões de assinantes, divididos principalmente entre as operadoras MTN e Orange."
        
        elif "operadoras" in user_query or "empresas" in user_query:
            response = "As principais operadoras no mercado são a MTN e a Orange. Ambas oferecem serviços de voz e dados, competindo pelo mercado com estratégias diferentes."
        
        elif "receita" in user_query or "faturamento" in user_query or "volume de negócio" in user_query:
            response = "A receita anual do setor de telecomunicações da Guiné-Bissau é de aproximadamente 128 bilhões de XOF, contribuindo significativamente para a economia do país."
        
        elif "relatório" in user_query or "relatórios" in user_query:
            response = "Você pode encontrar os relatórios anuais e trimestrais na seção 'Relatórios' do menu principal. Lá estão disponíveis análises detalhadas do mercado e das operadoras."
        
        else:
            # Mensagem genérica para outras perguntas
            if error_type == "quota_exceeded":
                response = "Desculpe, no momento nosso serviço está com alta demanda. Por favor, tente novamente mais tarde ou navegue pelo site para encontrar as informações que procura."
            elif error_type == "api_key_missing":
                response = "O assistente está passando por manutenção neste momento. Enquanto isso, você pode navegar pelo site para encontrar informações ou entrar em contato com a ARN diretamente."
            else:
                response = "Desculpe, não consegui processar sua pergunta corretamente. Poderia reformulá-la ou tentar novamente mais tarde?"
        
        # Adicionamos a resposta gerada localmente ao histórico
        conversation_history = self.get_conversation_history(session_id)
        conversation_history.append({"role": "user", "content": user_message})
        conversation_history.append({"role": "assistant", "content": response})
        self.save_conversation_history(session_id, conversation_history)
        
        # Registrar que estamos usando o fallback
        logger.warning(f"Usando resposta de fallback devido a erro: {error_type}")
        
        return {
            "message": response,
            "session_id": session_id,
            "status": "success",
            "using_fallback": True
        }
    
    def _handle_error(self, message: str, error_type: str) -> Dict[str, Any]:
        """
        Padroniza o formato de resposta para erros
        
        Args:
            message: Mensagem de erro amigável
            error_type: Tipo do erro ocorrido
            
        Returns:
            Dict: Resposta formatada com informações de erro
        """
        return {
            "message": message,
            "status": "error",
            "error_type": error_type
        }
    
    def _search_database(self, query: str) -> Optional[str]:
        """
        Busca informações no banco de dados com base na consulta do usuário
        
        Args:
            query: Consulta do usuário
            
        Returns:
            Optional[str]: Resposta encontrada ou None se nada for encontrado
        """
        query_lower = query.lower()
        
        # Verificar saudações simples e retornar None para permitir resposta amigável
        saudacoes = ["ola", "olá", "oi", "bom dia", "boa tarde", "boa noite", "boas", "hey", "hi", "hello"]
        if any(query_lower.strip() == saudacao for saudacao in saudacoes) or any(query_lower.startswith(s + " ") for s in saudacoes):
            # Para saudações, retornar None para permitir que o modelo de linguagem responda de forma amigável
            return None
            
        # Verificar se a consulta é muito curta, mas permitir perguntas diretas sobre dados
        palavras = query_lower.split()
        if len(palavras) < 3 and not any(keyword in query_lower for keyword in ["assinantes", "receita", "operadoras", "mercado", "tráfego", "penetração", "emprego", "dados"]):
            return None
        
        # Padrões para reconhecer tipos de consulta
        year_pattern = r'\b(20\d{2})\b'  # Padrão para anos como 2020, 2021, etc.
        year_match = re.search(year_pattern, query)
        
        year = None
        trimestre = None
        
        if year_match:
            year = int(year_match.group(1))
            logger.info(f"Ano detectado na consulta: {year}")
        
        # Detectar trimestre
        if "primeiro trimestre" in query_lower or "1º trimestre" in query_lower or "1o trimestre" in query_lower:
            trimestre = 1
        elif "segundo trimestre" in query_lower or "2º trimestre" in query_lower or "2o trimestre" in query_lower:
            trimestre = 2
        elif "terceiro trimestre" in query_lower or "3º trimestre" in query_lower or "3o trimestre" in query_lower:
            trimestre = 3
        elif "quarto trimestre" in query_lower or "4º trimestre" in query_lower or "4o trimestre" in query_lower:
            trimestre = 4
        
        # Palavras-chave para tipos de dados
        assinantes_keywords = ["assinantes", "subscritores", "clientes", "usuários"]
        receita_keywords = ["receita", "faturamento", "volume de negócio", "faturação"]
        emprego_keywords = ["emprego", "empregos", "funcionários", "colaboradores"]
        trafego_keywords = ["tráfego", "trafego", "chamadas", "minutos", "comunicações"]
        operadoras_keywords = ["operadoras", "operadores", "mtn", "orange", "empresas"]
        
        # Verificar tipo de dado solicitado
        data_type = None
        
        for keyword in assinantes_keywords:
            if keyword in query_lower:
                data_type = "assinantes"
                break
                
        if not data_type:
            for keyword in receita_keywords:
                if keyword in query_lower:
                    data_type = "receita"
                    break
        
        if not data_type:
            for keyword in emprego_keywords:
                if keyword in query_lower:
                    data_type = "emprego"
                    break
        
        if not data_type:
            for keyword in trafego_keywords:
                if keyword in query_lower:
                    data_type = "trafego"
                    break
        
        if not data_type:
            for keyword in operadoras_keywords:
                if keyword in query_lower:
                    data_type = "operadoras"
                    break
        
        # Buscar dados com base no tipo e período
        result = None
        
        try:
            # Verificar se é uma consulta de dados anuais
            if "anual" in query_lower or (year and not trimestre) or "relatório anual" in query_lower:
                result = self._search_annual_data(year, data_type, query_lower)
            
            # Verificar se é uma consulta de dados trimestrais
            elif ("trimestre" in query_lower or "trimestral" in query_lower or trimestre) and year:
                result = self._search_quarterly_data(year, trimestre, data_type, query_lower)
            
            # Busca geral se não for específica
            else:
                # Primeiro tentar dados anuais recentes
                result = self._search_annual_data(None, data_type, query_lower)
                
                # Se não encontrar, tentar dados trimestrais
                if not result:
                    result = self._search_quarterly_data(None, None, data_type, query_lower)
        
        except Exception as e:
            logger.error(f"Erro ao buscar dados no banco: {str(e)}", exc_info=True)
            return None
        
        return result
    
    def _search_annual_data(self, year: Optional[int], data_type: Optional[str], query: str) -> Optional[str]:
        """
        Busca dados anuais específicos
        
        Args:
            year: Ano dos dados
            data_type: Tipo de dado (assinantes, receita, etc.)
            query: Consulta original
            
        Returns:
            Optional[str]: Resposta formatada ou None
        """
        try:
            # Buscar dados do ano específico ou do último ano disponível se não especificado
            filter_params = {}
            if year:
                filter_params['ano'] = year
            
            # Buscar dados ordenados pelo ano mais recente
            dados_anuais = DadosAnuais.objects.all().order_by('-ano')
            
            if filter_params:
                dados_anuais = dados_anuais.filter(**filter_params)
            
            # Se não houver dados para o ano especificado, usar o último ano disponível
            if not dados_anuais.exists():
                if year:
                    # Tentar encontrar o ano mais próximo
                    dados_anuais = DadosAnuais.objects.all().order_by('-ano')
                    if dados_anuais.exists():
                        year_found = dados_anuais.first().ano
                        return f"Não encontrei dados para {year}. Os dados mais recentes são de {year_found}. Consulte o relatório anual para mais informações."
                return None
            
            # Selecionar o primeiro resultado (mais recente para o ano)
            dados = dados_anuais.first()
            year_found = dados.ano
            
            # Responder com base no tipo de dado
            if data_type == "assinantes":
                return f"Total de assinantes em {year_found}: {dados.assinantes_rede_movel:,.0f} assinantes. MTN: {dados.market_share_assinantes:.1f}% do mercado."
            
            elif data_type == "receita":
                return f"Receita total do setor em {year_found}: {dados.receita_total:,.0f} XOF."
            
            elif data_type == "emprego":
                return f"Total de empregos no setor em {year_found}: {dados.emprego_total:,.0f}."
            
            elif data_type == "trafego":
                return f"Tráfego de voz em {year_found}: {dados.trafego_voz_originado:,.0f} minutos. Dados: {dados.trafego_dados:,.0f} GB."
            
            elif data_type == "operadoras":
                return f"Operadoras em {year_found}: MTN (Market share: {dados.market_share_assinantes:.1f}%)."
            
            else:
                # Resposta geral sobre os dados do ano
                return f"Dados de {year_found}: {dados.assinantes_rede_movel:,.0f} assinantes, receita de {dados.receita_total:,.0f} XOF, {dados.emprego_total:,.0f} empregos no setor."
        
        except Exception as e:
            logger.error(f"Erro ao buscar dados anuais: {str(e)}", exc_info=True)
            return None
    
    def _search_quarterly_data(self, year: Optional[int], trimestre: Optional[int], data_type: Optional[str], query: str) -> Optional[str]:
        """
        Busca dados trimestrais específicos (adaptado para usar DadosAnuais já que não temos DadosTrimestre)
        
        Args:
            year: Ano dos dados
            trimestre: Número do trimestre (1-4)
            data_type: Tipo de dado (assinantes, receita, etc.)
            query: Consulta original
            
        Returns:
            Optional[str]: Resposta formatada ou None
        """
        try:
            # Como não temos dados trimestrais específicos, usamos os dados anuais
            # e ajustamos a resposta para indicar que são dados anuais, não trimestrais
            filter_params = {}
            if year:
                filter_params['ano'] = year
            
            # Buscar dados ordenados pelo ano mais recente
            dados_anuais = DadosAnuais.objects.all().order_by('-ano')
            
            if filter_params:
                dados_anuais = dados_anuais.filter(**filter_params)
            
            # Se não houver dados para o ano especificado, retornar None
            if not dados_anuais.exists():
                if year:
                    # Tentar encontrar o ano mais próximo
                    dados_anuais = DadosAnuais.objects.all().order_by('-ano')
                    if dados_anuais.exists():
                        dados = dados_anuais.first()
                        return f"Não encontrei dados trimestrais, mas tenho dados anuais de {dados.ano}. Os dados mais recentes disponíveis são de {dados.ano}."
                return None
            
            # Selecionar o primeiro resultado (mais recente)
            dados = dados_anuais.first()
            ano_encontrado = dados.ano
            
            # Responder com base no tipo de dado, mas indicando que são dados anuais (não trimestrais)
            if data_type == "assinantes":
                return f"Dados anuais de {ano_encontrado}: {dados.assinantes_rede_movel:,.0f} assinantes. MTN: {dados.market_share_assinantes:.1f}% do mercado."
            
            elif data_type == "receita":
                return f"Dados anuais de {ano_encontrado}: Receita total de {dados.receita_total:,.0f} XOF."
            
            elif data_type == "trafego":
                return f"Dados anuais de {ano_encontrado}: Tráfego de voz: {dados.trafego_voz_originado:,.0f} minutos. Dados: {dados.trafego_dados:,.0f} (unidades)."
            
            elif data_type == "operadoras":
                return f"Dados anuais de {ano_encontrado}: MTN (Market share: {dados.market_share_assinantes:.1f}%) e outras operadoras no mercado."
            
            else:
                # Resposta geral sobre os dados do ano
                return f"Dados anuais de {ano_encontrado}: {dados.assinantes_rede_movel:,.0f} assinantes, receita de {dados.receita_total:,.0f} XOF."
        
        except Exception as e:
            logger.error(f"Erro ao buscar dados trimestrais (adaptado): {str(e)}", exc_info=True)
            return None
    
    def _search_web(self, query: str) -> Optional[str]:
        """
        Busca informações na internet sobre telecomunicações na Guiné-Bissau
        
        Args:
            query: Consulta do usuário
            
        Returns:
            Optional[str]: Resposta encontrada ou None
        """
        try:
            # Adicionar "Guiné-Bissau telecomunicações" à consulta
            search_query = f"{query} Guiné-Bissau telecomunicações"
            
            # Tentar buscar no Google
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            
            response = requests.get(
                f"https://www.google.com/search?q={search_query.replace(' ', '+')}", 
                headers=headers,
                timeout=5
            )
            
            if response.status_code != 200:
                return None
            
            # Analisar página
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Extrair resumo (featured snippet) ou primeiro resultado
            featured_snippet = soup.select_one('.ILfuVd')
            
            if featured_snippet:
                result = featured_snippet.get_text()
                return f"{result} (Fonte: busca web, informação não oficial do observatório)"
            
            # Tentar extrair informação dos resultados
            search_results = soup.select('.g .VwiC3b')
            if search_results and len(search_results) > 0:
                first_result = search_results[0].get_text()
                return f"{first_result} (Fonte: busca web, informação não oficial do observatório)"
            
            return None
        
        except Exception as e:
            logger.error(f"Erro ao buscar informações na web: {str(e)}", exc_info=True)
            return None 