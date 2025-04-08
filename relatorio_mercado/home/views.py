from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import json
import logging
from .chatbot import Chatbot

# Configurar logging
logger = logging.getLogger(__name__)

# Instanciar o chatbot
chatbot_instance = Chatbot()

def index(request):
    """ A view to return the index page """
    return render(request, 'home/index.html')

@csrf_exempt
@require_POST
def chatbot_view(request):
    """
    View para processar as requisições do chatbot
    """
    try:
        # Obter a mensagem do usuário do corpo da requisição
        data = json.loads(request.body)
        user_message = data.get('message', '')
        
        # Obter ID da sessão, se existir
        session_id = request.session.get('chatbot_session_id')
        
        # Verificar se a mensagem está vazia
        if not user_message:
            return JsonResponse({
                'message': 'Por favor, digite uma mensagem.',
                'status': 'error',
                'error_type': 'empty_message'
            }, status=400)
        
        # Registrar a mensagem recebida (sem incluir dados sensíveis)
        logger.info(f"Mensagem recebida do usuário - comprimento: {len(user_message)}")
        
        # Obter a resposta do chatbot
        response_data = chatbot_instance.get_response(user_message, session_id)
        
        # Salvar ID da sessão no cookie se não existir
        if 'session_id' in response_data and (response_data['status'] == 'success' or response_data.get('using_fallback', False)):
            request.session['chatbot_session_id'] = response_data['session_id']
            # Definir que a sessão não expira quando o navegador fecha
            request.session.set_expiry(60 * 60 * 24 * 7)  # 7 dias
        
        # Registrar se estamos usando fallback
        if response_data.get('using_fallback', False):
            logger.info("Usando resposta de fallback para o usuário")
        
        # Retornar a resposta como JSON
        return JsonResponse(response_data)
    
    except json.JSONDecodeError:
        logger.warning("Requisição com JSON inválido recebida")
        return JsonResponse({
            'message': 'Formato de mensagem inválido. Envie um JSON válido.',
            'status': 'error',
            'error_type': 'invalid_json'
        }, status=400)
    
    except Exception as e:
        # Logar o erro
        logger.error(f"Erro no processamento do chatbot: {str(e)}", exc_info=True)
        return JsonResponse({
            'message': 'Desculpe, ocorreu um erro inesperado. Por favor, tente novamente mais tarde.',
            'status': 'error',
            'error_type': 'server_error'
        }, status=500)

@csrf_exempt
@require_POST
def reset_chatbot(request):
    """
    View para resetar a conversa do chatbot
    """
    try:
        # Obter ID da sessão
        session_id = request.session.get('chatbot_session_id')
        
        # Resetar o chatbot
        chatbot_instance.reset_conversation(session_id)
        
        # Log da ação
        logger.info(f"Conversa resetada para sessão: {session_id}")
        
        return JsonResponse({
            'message': 'Conversa reiniciada com sucesso',
            'status': 'success'
        })
    
    except Exception as e:
        # Logar o erro
        logger.error(f"Erro ao resetar conversa: {str(e)}", exc_info=True)
        return JsonResponse({
            'message': 'Não foi possível reiniciar a conversa. Tente novamente.',
            'status': 'error',
            'error_type': 'reset_error'
        }, status=500)