/**
 * Observatório do Mercado de Telecomunicações - Main JavaScript
 * Este arquivo contém as principais funcionalidades para todo o site
 */

document.addEventListener('DOMContentLoaded', function() {
    // Inicialização
    console.log('Main JS loaded');
    initializeNavbar();
    initializeAnimations();
    setupScrollEffects();
    setupFormValidation();
    setupDropdownHover();
    setupBackToTop();
});

/**
 * Inicializa comportamentos da barra de navegação
 */
function initializeNavbar() {
    // Barra de navegação fixa com transição
    const navbar = document.querySelector('.navbar');
    
    if (navbar) {
        window.addEventListener('scroll', function() {
            if (window.scrollY > 50) {
                navbar.classList.add('navbar-scrolled');
            } else {
                navbar.classList.remove('navbar-scrolled');
            }
        });

        // Adiciona classe active ao item de menu atual
        const currentPath = window.location.pathname;
        const navLinks = document.querySelectorAll('.nav-link');
        
        navLinks.forEach(link => {
            const href = link.getAttribute('href');
            if (href && currentPath.includes(href) && href !== '/') {
                link.closest('.nav-item').classList.add('active');
            } else if (href === '/' && currentPath === '/') {
                link.closest('.nav-item').classList.add('active');
            }
        });
    }
}

/**
 * Inicializa animações para elementos da página
 */
function initializeAnimations() {
    // Animar elementos ao entrar na viewport
    const animatedElements = document.querySelectorAll('.highlight-card, .report-card, .operator-card, .section-header');
    
    if (animatedElements.length) {
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('animated');
                    observer.unobserve(entry.target);
                }
            });
        }, { threshold: 0.1 });

        animatedElements.forEach(element => {
            element.classList.add('fade-in');
            observer.observe(element);
        });
    }
}

/**
 * Configuração de efeitos de rolagem
 */
function setupScrollEffects() {
    // Rolagem suave para links de âncora
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const targetId = this.getAttribute('href');
            
            if (targetId !== '#') {
                const targetElement = document.querySelector(targetId);
                if (targetElement) {
                    window.scrollTo({
                        top: targetElement.offsetTop - 100,
                        behavior: 'smooth'
                    });
                }
            }
        });
    });
}

/**
 * Configuração de validação de formulários
 */
function setupFormValidation() {
    // Validação básica de formulário
    const forms = document.querySelectorAll('form');
    
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const requiredFields = form.querySelectorAll('[required]');
            let valid = true;
            
            requiredFields.forEach(field => {
                if (!field.value.trim()) {
                    valid = false;
                    field.classList.add('is-invalid');
                } else {
                    field.classList.remove('is-invalid');
                }
            });
            
            if (!valid) {
                e.preventDefault();
                e.stopPropagation();
            }
        });
        
        // Remover destaque de erro quando o usuário digita
        const inputs = form.querySelectorAll('input, select, textarea');
        inputs.forEach(input => {
            input.addEventListener('input', function() {
                if (this.value.trim()) {
                    this.classList.remove('is-invalid');
                }
            });
        });
    });
}

/**
 * Configuração de efeito hover para dropdown
 */
function setupDropdownHover() {
    // Em desktop, mostrar dropdown no hover
    if (window.innerWidth >= 992) {
        const dropdowns = document.querySelectorAll('.navbar .dropdown');
        
        dropdowns.forEach(dropdown => {
            dropdown.addEventListener('mouseenter', function() {
                if (window.innerWidth >= 992) {
                    const dropdownMenu = this.querySelector('.dropdown-menu');
                    dropdownMenu.classList.add('show');
                }
            });
            
            dropdown.addEventListener('mouseleave', function() {
                if (window.innerWidth >= 992) {
                    const dropdownMenu = this.querySelector('.dropdown-menu');
                    dropdownMenu.classList.remove('show');
                }
            });
        });
    }
}

/**
 * Adiciona botão "Voltar ao topo"
 */
function setupBackToTop() {
    // Criar botão dinamicamente
    const backToTopBtn = document.createElement('button');
    backToTopBtn.innerHTML = '<i class="fas fa-arrow-up"></i>';
    backToTopBtn.className = 'back-to-top';
    backToTopBtn.setAttribute('aria-label', 'Voltar ao topo');
    document.body.appendChild(backToTopBtn);
    
    // Mostrar/ocultar botão com base na rolagem
    window.addEventListener('scroll', function() {
        if (window.scrollY > 300) {
            backToTopBtn.classList.add('show');
        } else {
            backToTopBtn.classList.remove('show');
        }
    });
    
    // Ação de clique
    backToTopBtn.addEventListener('click', function() {
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    });
}

/**
 * Função para formatar números
 * @param {number} number - Número a ser formatado
 * @param {string} locale - Localidade para formatação (padrão: 'pt-GW')
 * @returns {string} Número formatado
 */
function formatNumber(number, locale = 'pt-GW') {
    return new Intl.NumberFormat(locale).format(number);
}

/**
 * Função para formatar moeda
 * @param {number} value - Valor a ser formatado
 * @param {string} currency - Código da moeda (padrão: 'XOF')
 * @param {string} locale - Localidade para formatação (padrão: 'pt-GW')
 * @returns {string} Valor formatado como moeda
 */
function formatCurrency(value, currency = 'XOF', locale = 'pt-GW') {
    return new Intl.NumberFormat(locale, {
        style: 'currency',
        currency: currency,
        minimumFractionDigits: 0,
        maximumFractionDigits: 0
    }).format(value);
}

/**
 * Função para formatar tamanho de dados
 * @param {number} bytes - Tamanho em bytes
 * @returns {string} Tamanho formatado
 */
function formatDataSize(bytes) {
    const sizes = ['B', 'KB', 'MB', 'GB', 'TB'];
    if (bytes === 0) return '0 B';
    const i = parseInt(Math.floor(Math.log(bytes) / Math.log(1024)));
    return Math.round(bytes / Math.pow(1024, i) * 100) / 100 + ' ' + sizes[i];
}

// Adicionando algumas regras CSS dinamicamente
(() => {
    const style = document.createElement('style');
    style.textContent = `
        .fade-in {
            opacity: 0;
            transform: translateY(20px);
            transition: opacity 0.5s ease, transform 0.5s ease;
        }
        
        .fade-in.animated {
            opacity: 1;
            transform: translateY(0);
        }
        
        .navbar-scrolled {
            padding: 0.75rem 0;
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
        }
        
        .back-to-top {
            position: fixed;
            bottom: 20px;
            right: 20px;
            width: 40px;
            height: 40px;
            border-radius: 50%;
            background-color: var(--primary-color);
            color: white;
            border: none;
            display: flex;
            align-items: center;
            justify-content: center;
            cursor: pointer;
            opacity: 0;
            transform: translateY(20px);
            transition: opacity 0.3s ease, transform 0.3s ease;
            z-index: 999;
        }
        
        .back-to-top.show {
            opacity: 1;
            transform: translateY(0);
        }
        
        .back-to-top:hover {
            background-color: var(--primary-dark);
        }
    `;
    document.head.appendChild(style);
})(); 