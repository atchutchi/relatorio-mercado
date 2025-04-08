/**
 * Script para controlar o widget de chat do Observatório do Mercado
 * Versão aprimorada com animações de digitação, sugestões e persistência
 */

document.addEventListener('DOMContentLoaded', function() {
    // Elementos do DOM
    const chatIcon = document.getElementById('chat-icon');
    const chatWidget = document.getElementById('chat-widget');
    const chatClose = document.getElementById('chat-close');
    const chatMessages = document.getElementById('chat-messages');
    const chatForm = document.getElementById('chat-form');
    const chatInput = document.getElementById('chat-input');
    const resetButton = document.getElementById('reset-chat');
    
    // Estado do chat
    let initialized = false;
    let isTyping = false;
    let lastProcessedMessage = ''; // Armazenar a última mensagem processada
    
    // Configuração do chatbot
    const chatbotConfig = {
        showSuggestions: false // Por padrão, não mostrar sugestões
    };
    
    // Verificar se todos os elementos foram encontrados
    console.log('Chat icon found:', !!chatIcon);
    console.log('Chat widget found:', !!chatWidget);
    console.log('Chat close found:', !!chatClose);
    console.log('Chat messages found:', !!chatMessages);
    console.log('Chat form found:', !!chatForm);
    console.log('Chat input found:', !!chatInput);
    console.log('Reset button found:', !!resetButton);
    
    // Sugestões de perguntas
    const suggestedQueries = [
        "Quais são os dados de assinantes mais recentes?",
        "Como está a evolução do mercado?",
        "Quais operadoras estão no mercado?",
        "Onde encontro os relatórios anuais?",
        "Qual a taxa de penetração móvel?"
    ];

    // Adicionar botão para alternar sugestões
    function addSuggestionsToggleButton() {
        const toggleButton = document.createElement('button');
        toggleButton.innerHTML = '<i class="fas fa-lightbulb"></i>';
        toggleButton.className = 'suggestion-toggle';
        toggleButton.title = 'Mostrar/esconder sugestões';
        
        toggleButton.addEventListener('click', function() {
            const suggestionsDiv = document.querySelector('.chat-suggestions');
            
            if (suggestionsDiv) {
                // Esconder sugestões existentes
                suggestionsDiv.remove();
                chatbotConfig.showSuggestions = false;
            } else {
                // Mostrar sugestões
                addSuggestions();
                chatbotConfig.showSuggestions = true;
            }
        });
        
        const chatControls = document.querySelector('.chat-controls');
        if (chatControls) {
            chatControls.insertBefore(toggleButton, chatControls.firstChild);
        }
    }
    
    // Adicionar botão para alternar sugestões quando o DOM estiver pronto
    addSuggestionsToggleButton();

    // Carregar histórico da sessão atual
    function loadSessionHistory() {
        const savedMessages = sessionStorage.getItem('chatMessages');
        const wasInitialized = sessionStorage.getItem('chatInitialized');
        
        if (savedMessages) {
            chatMessages.innerHTML = savedMessages;
            initialized = wasInitialized === 'true';
            
            // Rolar para a última mensagem
            chatMessages.scrollTop = chatMessages.scrollHeight;
            return true;
        }
        
        return false;
    }
    
    // Salvar histórico na sessão
    function saveSessionHistory() {
        sessionStorage.setItem('chatMessages', chatMessages.innerHTML);
        sessionStorage.setItem('chatInitialized', initialized.toString());
    }
    
    // Adicionar sugestões de mensagens
    function addSuggestions() {
        // Verificar se as sugestões já existem
        if (document.querySelector('.chat-suggestions')) {
            return;
        }
        
        const suggestionsDiv = document.createElement('div');
        suggestionsDiv.classList.add('chat-suggestions');
        
        // Adicionar chips de sugestão
        suggestedQueries.forEach(query => {
            const chip = document.createElement('button');
            chip.classList.add('suggestion-chip');
            chip.textContent = query;
            chip.addEventListener('click', () => {
                chatInput.value = query;
                chatInput.focus();
            });
            suggestionsDiv.appendChild(chip);
        });
        
        // Adicionar após o formulário
        chatForm.parentNode.insertBefore(suggestionsDiv, chatForm.nextSibling);
    }
    
    // Adicionar mensagem de boas-vindas
    function initializeChat() {
        if (!initialized) {
            const sessionLoaded = loadSessionHistory();
            
            if (!sessionLoaded) {
                const welcomeMessage = 'Olá! Sou o assistente virtual do Observatório do Mercado de Telecomunicações. Como posso ajudar você hoje?';
                addMessage('assistant', welcomeMessage, true);
                
                // Só adicionar sugestões se a configuração permitir
                if (chatbotConfig.showSuggestions) {
                    addSuggestions();
                }
            }
            
            initialized = true;
            saveSessionHistory();
        }
    }
    
    // Efeito de digitação
    function typeMessage(element, text, callback) {
        let index = 0;
        element.textContent = '';
        isTyping = true;
        
        function type() {
            if (index < text.length) {
                element.textContent += text.charAt(index);
                index++;
                chatMessages.scrollTop = chatMessages.scrollHeight;
                setTimeout(type, Math.random() * 30 + 20); // Velocidade variável para parecer mais natural
            } else {
                isTyping = false;
                if (callback) callback();
            }
        }
        
        type();
    }
    
    // Adicionar mensagem ao widget
    function addMessage(sender, text, withAnimation = false, source = null) {
        const messageDiv = document.createElement('div');
        messageDiv.classList.add('chat-message', sender);
        
        // Criar ícone diferente dependendo se é usuário ou assistente
        const iconSpan = document.createElement('span');
        iconSpan.classList.add('message-icon');
        
        if (sender === 'user') {
            iconSpan.innerHTML = '<i class="fas fa-user"></i>';
        } else {
            iconSpan.innerHTML = '<i class="fas fa-robot"></i>';
        }
        
        // Criar container para o texto
        const textSpan = document.createElement('span');
        textSpan.classList.add('message-text');
        
        // Sempre adicionar os elementos básicos primeiro
        messageDiv.appendChild(iconSpan);
        messageDiv.appendChild(textSpan);
        
        // Adicionar fonte da informação, se disponível
        if (source && sender === 'assistant') {
            const sourceClass = `source-${source}`;
            const sourceLabels = {
                'database': 'Dados do observatório',
                'web': 'Informação da web',
                'model': 'Assistente IA'
            };
            
            const sourceLabel = sourceLabels[source] || 'Assistente';
            const sourceSpan = document.createElement('span');
            sourceSpan.classList.add('message-source', sourceClass);
            sourceSpan.innerHTML = `<i class="fas fa-${source === 'database' ? 'database' : (source === 'web' ? 'globe' : 'brain')}"></i> ${sourceLabel}`;
            
            // Adicionamos após o span de texto
            messageDiv.appendChild(sourceSpan);
        }
        
        if (withAnimation && sender === 'assistant') {
            textSpan.textContent = '';
            chatMessages.appendChild(messageDiv);
            
            // Iniciar animação de digitação após um breve atraso
            setTimeout(() => {
                typeMessage(textSpan, text, () => {
                    // Processar links no texto após animação
                    textSpan.innerHTML = formatMessageWithLinks(textSpan.textContent);
                    saveSessionHistory();
                });
            }, 500);
        } else {
            if (sender === 'assistant') {
                textSpan.innerHTML = formatMessageWithLinks(text);
            } else {
                textSpan.textContent = text;
            }
            
            chatMessages.appendChild(messageDiv);
        }
        
        // Rolar para a última mensagem
        chatMessages.scrollTop = chatMessages.scrollHeight;
        
        // Salvar no sessionStorage
        if (!isTyping) {
            saveSessionHistory();
        }
    }
    
    // Formatar texto com links clickáveis
    function formatMessageWithLinks(text) {
        // Expressão regular para identificar URLs
        const urlRegex = /(https?:\/\/[^\s]+)/g;
        
        // Substituir URLs por links clicáveis
        return text.replace(urlRegex, url => {
            return `<a href="${url}" target="_blank" rel="noopener noreferrer">${url}</a>`;
        });
    }
    
    // Enviar mensagem para o backend
    async function sendMessage(message) {
        try {
            // Verificar se a mensagem é igual à última processada para evitar duplicação
            if (message === lastProcessedMessage && message.trim() !== '') {
                console.log('Mensagem duplicada detectada e ignorada:', message);
                return;
            }
            
            // Atualizar última mensagem processada
            lastProcessedMessage = message;
            
            // Adicionar loading spinner
            const loadingDiv = document.createElement('div');
            loadingDiv.classList.add('chat-message', 'assistant', 'loading');
            loadingDiv.innerHTML = '<span class="message-icon"><i class="fas fa-spinner fa-spin"></i></span><span class="message-text">Pensando...</span>';
            chatMessages.appendChild(loadingDiv);
            chatMessages.scrollTop = chatMessages.scrollHeight;
            
            // Enviar requisição para o backend
            const response = await fetch('/api/chatbot/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCSRFToken()
                },
                body: JSON.stringify({ message: message }),
            });
            
            // Adicionar um tempo mínimo de "pensamento" (pelo menos 1 segundo)
            const startTime = Date.now();
            const minThinkingTime = 1500; // 1.5 segundos
            
            const data = await response.json();
            
            // Calcular quanto tempo já passou desde o início da requisição
            const elapsedTime = Date.now() - startTime;
            
            // Se o tempo decorrido for menor que o tempo mínimo, esperar a diferença
            if (elapsedTime < minThinkingTime) {
                await new Promise(resolve => setTimeout(resolve, minThinkingTime - elapsedTime));
            }
            
            // Remover loading spinner somente após o tempo mínimo de pensamento
            chatMessages.removeChild(loadingDiv);
            
            if (!response.ok) {
                throw new Error(`Erro HTTP: ${response.status}`);
            }
            
            // Verificar o status da resposta
            if (data.status === 'error') {
                // Tratar erros específicos
                handleErrorMessage(data.error_type, data.message);
                return;
            }
            
            // Determinar a fonte da resposta
            let source = 'model';
            if (data.source === 'database') {
                source = 'database';
            } else if (data.source === 'web') {
                source = 'web';
            }
            
            // Adicionar resposta do assistente com animação (a menos que seja fallback)
            const useAnimation = !data.using_fallback;
            addMessage('assistant', data.message, useAnimation, source);
            
        } catch (error) {
            console.error('Erro ao enviar mensagem:', error);
            addMessage('assistant', 'Desculpe, ocorreu um erro ao processar sua mensagem. Por favor, tente novamente mais tarde.');
            saveSessionHistory();
        }
    }
    
    // Processar diferentes tipos de erro
    function handleErrorMessage(errorType, message) {
        let errorMessage = message;
        
        // Adicionar sugestões adicionais baseadas no tipo de erro
        switch (errorType) {
            case 'rate_limit':
                errorMessage += ' Você pode continuar navegando pelo site enquanto isso.';
                break;
                
            case 'quota_exceeded':
                errorMessage += ' Por favor, explore as diferentes seções do site para encontrar as informações que procura.';
                // Adicionar algumas sugestões de navegação
                addSuggestedLinks();
                break;
                
            case 'connection_error':
                errorMessage += ' Verifique sua conexão com a internet e tente novamente.';
                break;
        }
        
        addMessage('assistant', errorMessage);
        saveSessionHistory();
    }
    
    // Adicionar links de sugestão quando o chatbot não está disponível
    function addSuggestedLinks() {
        const suggestionsDiv = document.createElement('div');
        suggestionsDiv.classList.add('chat-message', 'assistant');
        
        const iconSpan = document.createElement('span');
        iconSpan.classList.add('message-icon');
        iconSpan.innerHTML = '<i class="fas fa-robot"></i>';
        
        const textSpan = document.createElement('span');
        textSpan.classList.add('message-text');
        textSpan.innerHTML = `
            Aqui estão alguns links úteis:<br>
            <a href="/dados_anuais/annual_report/" class="chat-link">Relatório Anual</a><br>
            <a href="/dados_anuais/market_overview/" class="chat-link">Visão Geral do Mercado</a><br>
            <a href="/dados_anuais/operator_evolution/MTN/" class="chat-link">Evolução da MTN</a><br>
            <a href="/dados_anuais/operator_evolution/ORANGE/" class="chat-link">Evolução da Orange</a><br>
        `;
        
        suggestionsDiv.appendChild(iconSpan);
        suggestionsDiv.appendChild(textSpan);
        chatMessages.appendChild(suggestionsDiv);
        
        // Rolar para a última mensagem
        chatMessages.scrollTop = chatMessages.scrollHeight;
        saveSessionHistory();
    }
    
    // Obter CSRF token do cookie
    function getCSRFToken() {
        const cookieValue = document.cookie
            .split('; ')
            .find(row => row.startsWith('csrftoken='))
            ?.split('=')[1];
        
        return cookieValue || '';
    }
    
    // Evento de abertura e fechamento do chat
    if (chatIcon) {
        console.log('Adding click handler to chat icon');
        chatIcon.addEventListener('click', function() {
            console.log('Chat icon clicked');
            chatWidget.classList.add('visible');
            initializeChat();
            chatInput.focus();
        });
    }
    
    if (chatClose) {
        console.log('Adding click handler to chat close');
        chatClose.addEventListener('click', function() {
            console.log('Chat close clicked');
            chatWidget.classList.remove('visible');
        });
    }
    
    // Envio de mensagem
    if (chatForm) {
        console.log('Adding submit handler to chat form');
        chatForm.addEventListener('submit', function(e) {
            e.preventDefault();
            console.log('Chat form submitted');
            
            const message = chatInput.value.trim();
            if (message !== '' && !isTyping) {
                // Adicionar mensagem do usuário
                addMessage('user', message);
                
                // Enviar mensagem para o backend
                sendMessage(message);
                
                // Limpar input
                chatInput.value = '';
            }
        });
    }
    
    // Suporte a teclas
    if (chatInput) {
        chatInput.addEventListener('keydown', function(e) {
            // Enter para enviar (sem shift)
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                chatForm.dispatchEvent(new Event('submit'));
            }
        });
    }
    
    // Resetar conversa
    if (resetButton) {
        console.log('Adding click handler to reset button');
        resetButton.addEventListener('click', function() {
            console.log('Reset button clicked');
            if (!isTyping) {
                // Limpar chat
                chatMessages.innerHTML = '';
                
                // Limpar sessão
                sessionStorage.removeItem('chatMessages');
                sessionStorage.removeItem('chatInitialized');
                
                // Reinicializar
                initialized = false;
                initializeChat();
            }
        });
    }
    
    // Detectar cliques fora do chat para fechar (opcional)
    document.addEventListener('click', function(e) {
        if (chatWidget.classList.contains('open') && 
            !chatWidget.contains(e.target) && 
            e.target !== chatIcon && 
            !chatIcon.contains(e.target)) {
            chatWidget.classList.remove('open');
        }
    });
    
    // Verificar se há histórico ao carregar a página
    if (sessionStorage.getItem('chatMessages')) {
        loadSessionHistory();
    }
}); 