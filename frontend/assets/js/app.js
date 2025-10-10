// ===== APPLICATION STATE =====
const AppState = {
    user: null,
    token: null,
    currentPage: 'dashboard',
    config: {},
    
    // Dados temporários
    manualEntries: [],
    manualMontagemEntries: [],
    
    // Configurações de UI
    sidebarCollapsed: false,
    theme: 'light'
};

// ===== CONFIGURATION =====
const API_BASE_URL = '/api';

// ===== LOGGING SYSTEM =====
class Logger {
    static log(level, message, data = null) {
        const timestamp = new Date().toISOString();
        const logMessage = `[${timestamp}] ${level.toUpperCase()}: ${message}`;
        
        console[level.toLowerCase()](logMessage, data || '');
        
        // Armazenar logs localmente para debug
        const logs = JSON.parse(localStorage.getItem('app_logs') || '[]');
        logs.push({ timestamp, level, message, data });
        
        // Manter apenas os últimos 100 logs
        if (logs.length > 100) logs.shift();
        localStorage.setItem('app_logs', JSON.stringify(logs));
    }
    
    static info(message, data) { this.log('info', message, data); }
    static warn(message, data) { this.log('warn', message, data); }
    static error(message, data) { this.log('error', message, data); }
    static debug(message, data) { this.log('debug', message, data); }
    
    static getLogs() {
        return JSON.parse(localStorage.getItem('app_logs') || '[]');
    }
    
    static clearLogs() {
        localStorage.removeItem('app_logs');
    }
}

// ===== UTILITY CLASSES =====
class SessionManager {
    static saveToken(token) {
        localStorage.setItem('auth_token', token);
        AppState.token = token;
    }
    
    static getToken() {
        const token = localStorage.getItem('auth_token');
        AppState.token = token;
        return token;
    }
    
    static clearSession() {
        localStorage.clear();
        AppState.token = null;
        AppState.user = null;
        showLoginScreen();
    }
    
    static saveUser(user) {
        localStorage.setItem('user_info', JSON.stringify(user));
        AppState.user = user;
    }
    
    static getUser() {
        const user = localStorage.getItem('user_info');
        if (user) {
            AppState.user = JSON.parse(user);
            return AppState.user;
        }
        return null;
    }
}

class NotificationSystem {
    static success(message, duration = 5000) {
        this.showToast('Success', message, 'success', duration);
    }
    
    static error(message, duration = 8000) {
        this.showToast('Erro', message, 'danger', duration);
    }
    
    static warning(message, duration = 6000) {
        this.showToast('Atenção', message, 'warning', duration);
    }
    
    static info(message, duration = 5000) {
        this.showToast('Informação', message, 'info', duration);
    }
    
    static showToast(title, message, type = 'primary', duration = 5000) {
        const toastContainer = document.getElementById('toastContainer');
        const toastId = 'toast_' + Date.now();
        
        const toastHTML = `
            <div id="${toastId}" class="toast" role="alert" aria-live="assertive" aria-atomic="true">
                <div class="toast-header">
                    <i class="fas fa-${this.getToastIcon(type)} text-${type} me-2"></i>
                    <strong class="me-auto">${title}</strong>
                    <button type="button" class="btn-close" data-bs-dismiss="toast"></button>
                </div>
                <div class="toast-body">
                    ${message}
                </div>
            </div>
        `;
        
        toastContainer.insertAdjacentHTML('beforeend', toastHTML);
        
        const toastElement = document.getElementById(toastId);
        const toast = new bootstrap.Toast(toastElement, { delay: duration });
        toast.show();
        
        // Remove o elemento do DOM após ser fechado
        toastElement.addEventListener('hidden.bs.toast', () => {
            toastElement.remove();
        });
    }
    
    static getToastIcon(type) {
        const icons = {
            'success': 'check-circle',
            'danger': 'exclamation-circle',
            'warning': 'exclamation-triangle',
            'info': 'info-circle',
            'primary': 'info-circle'
        };
        return icons[type] || 'info-circle';
    }
    
    static showSpinner(message = 'Carregando...') {
        const overlay = document.getElementById('loadingOverlay');
        const text = overlay.querySelector('.loading-text');
        text.textContent = message;
        overlay.classList.remove('d-none');
    }
    
    static hideSpinner() {
        const overlay = document.getElementById('loadingOverlay');
        overlay.classList.add('d-none');
    }
}

class APIClient {
    static async request(method, endpoint, data = null, options = {}) {
        const token = SessionManager.getToken();
        const headers = {
            'Content-Type': 'application/json',
            ...options.headers
        };
        
        if (token) {
            headers.Authorization = `Bearer ${token}`;
        }
        
        const config = {
            method,
            headers,
            ...options
        };
        
        if (data && method !== 'GET') {
            config.body = JSON.stringify(data);
        }
        
        Logger.info(`📡 API Request: ${method} ${endpoint}`, { data, hasToken: !!token });
        
        try {
            const response = await fetch(`${API_BASE_URL}${endpoint}`, config);
            Logger.info(`📡 API Response: ${method} ${endpoint} - Status: ${response.status}`);
            
            if (response.status === 401) {
                Logger.warn('🔐 Token inválido (401), limpando sessão');
                SessionManager.clearSession();
                return null;
            }
            
            if (!response.ok) {
                const errorData = await response.json().catch(() => ({ message: 'Erro desconhecido' }));
                Logger.error(`❌ API Error ${response.status}: ${method} ${endpoint}`, errorData);
                throw new Error(errorData.message || `HTTP ${response.status}`);
            }
            
            const responseData = await response.json();
            Logger.info(`✅ API Success: ${method} ${endpoint}`, responseData);
            return responseData;
            
        } catch (error) {
            Logger.error(`💥 API Exception: ${method} ${endpoint}`, error);
            console.error('API Error:', error);
            throw error;
        }
    }
    
    static async get(endpoint, options = {}) {
        return this.request('GET', endpoint, null, options);
    }
    
    static async post(endpoint, data, options = {}) {
        return this.request('POST', endpoint, data, options);
    }
    
    static async put(endpoint, data, options = {}) {
        return this.request('PUT', endpoint, data, options);
    }
    
    static async delete(endpoint, options = {}) {
        return this.request('DELETE', endpoint, null, options);
    }
}

// ===== PAGE MANAGERS =====
class PageManager {
    static pages = {
        'dashboard': 'Dashboard de Pendências',
        'prestadores': 'Prestadores de Serviço',
        'montadores': 'Montadores'
    };
    
    static navigateTo(page) {
        if (!this.pages[page]) {
            console.error('Página não encontrada:', page);
            return;
        }
        
        AppState.currentPage = page;
        
        // Atualizar menu ativo
        document.querySelectorAll('.nav-link').forEach(link => {
            link.classList.remove('active');
        });
        document.querySelector(`[data-page="${page}"]`).classList.add('active');
        
        // Atualizar título da página
        document.getElementById('pageTitle').textContent = this.pages[page];
        
        // Carregar conteúdo da página
        this.loadPageContent(page);
        
        // Fechar sidebar em mobile
        this.closeSidebar();
    }
    
    static async loadPageContent(page) {
        const contentDiv = document.getElementById('pageContent');
        
        try {
            NotificationSystem.showSpinner('Carregando página...');
            
            switch (page) {
                case 'dashboard':
                    await this.loadDashboard(contentDiv);
                    break;
                case 'prestadores':
                    await this.loadPrestadores(contentDiv);
                    break;
                case 'montadores':
                    await this.loadMontadores(contentDiv);
                    break;
                default:
                    contentDiv.innerHTML = '<div class="alert alert-warning">Página não encontrada</div>';
            }
        } catch (error) {
            console.error('Erro ao carregar página:', error);
            contentDiv.innerHTML = `<div class="alert alert-danger">Erro ao carregar página: ${error.message}</div>`;
        } finally {
            NotificationSystem.hideSpinner();
        }
    }
    
    static async loadDashboard(container) {
        const dashboardHTML = `
            <div class="dashboard-page">
                <div class="page-header mb-4">
                    <h2><i class="fas fa-calendar-check text-primary me-2"></i> Dashboard de Pendências</h2>
                    <p class="text-muted">Acompanhe os envios pendentes para hoje</p>
                </div>
                
                <div class="row">
                    <!-- Card Prestadores -->
                    <div class="col-xl-6 mb-4">
                        <div class="card">
                            <div class="card-header">
                                <h5><i class="fas fa-user-tie me-2"></i> Prestadores Pendentes</h5>
                            </div>
                            <div class="card-body" id="prestadores-pendentes">
                                <div class="text-center py-4">
                                    <div class="spinner-border text-primary" role="status">
                                        <span class="visually-hidden">Carregando...</span>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                    
                    <!-- Card Montadores -->
                    <div class="col-xl-6 mb-4">
                        <div class="card">
                            <div class="card-header">
                                <h5><i class="fas fa-hard-hat me-2"></i> Montadores Pendentes</h5>
                            </div>
                            <div class="card-body" id="montadores-pendentes">
                                <div class="text-center py-4">
                                    <div class="spinner-border text-primary" role="status">
                                        <span class="visually-hidden">Carregando...</span>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                
                <!-- Resumo do Dia -->
                <div class="row">
                    <div class="col-12">
                        <div class="card">
                            <div class="card-header">
                                <h5><i class="fas fa-chart-line me-2"></i> Resumo do Dia</h5>
                            </div>
                            <div class="card-body">
                                <div class="row text-center">
                                    <div class="col-md-3">
                                        <div class="h4 text-primary" id="totalPendentes">-</div>
                                        <small class="text-muted">Total Pendentes</small>
                                    </div>
                                    <div class="col-md-3">
                                        <div class="h4 text-success" id="totalEnviados">-</div>
                                        <small class="text-muted">Enviados Hoje</small>
                                    </div>
                                    <div class="col-md-3">
                                        <div class="h4 text-warning" id="totalIgnorados">-</div>
                                        <small class="text-muted">Ignorados</small>
                                    </div>
                                    <div class="col-md-3">
                                        <div class="h4 text-info" id="totalPrestadores">-</div>
                                        <small class="text-muted">Prestadores Ativos</small>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        `;
        
        container.innerHTML = dashboardHTML;
        
        // Carregar dados do dashboard
        await this.loadDashboardData();
    }
    
    static async loadDashboardData() {
        try {
            // TODO: Implementar chamadas para a API real
            // Por enquanto, dados mockados para demonstração
            
            setTimeout(() => {
                document.getElementById('prestadores-pendentes').innerHTML = `
                    <div class="alert alert-success">
                        <i class="fas fa-check-circle me-2"></i>
                        Nenhum prestador com pendências para hoje!
                    </div>
                `;
                
                document.getElementById('montadores-pendentes').innerHTML = `
                    <div class="alert alert-success">
                        <i class="fas fa-check-circle me-2"></i>
                        Nenhum montador com pendências para hoje!
                    </div>
                `;
                
                document.getElementById('totalPendentes').textContent = '0';
                document.getElementById('totalEnviados').textContent = '5';
                document.getElementById('totalIgnorados').textContent = '2';
                document.getElementById('totalPrestadores').textContent = '12';
            }, 1000);
            
        } catch (error) {
            console.error('Erro ao carregar dados do dashboard:', error);
            NotificationSystem.error('Erro ao carregar dados do dashboard');
        }
    }
    
    static async loadPrestadores(container) {
        const prestadoresHTML = `
            <div class="prestadores-page">
                <div class="page-header mb-4">
                    <h2><i class="fas fa-user-tie text-primary me-2"></i> Prestadores de Serviço</h2>
                    <p class="text-muted">Gerencie prestadores e envie boletins de serviço</p>
                </div>
                
                <!-- Navegação por Tabs -->
                <ul class="nav nav-tabs" id="prestadoresTabs" role="tablist">
                    <li class="nav-item" role="presentation">
                        <button class="nav-link active" id="enviar-boletins-tab" data-bs-toggle="tab" data-bs-target="#enviar-boletins" type="button" role="tab">
                            <i class="fas fa-paper-plane me-2"></i> Enviar Boletins
                        </button>
                    </li>
                    <li class="nav-item" role="presentation">
                        <button class="nav-link" id="gerenciar-prestadores-tab" data-bs-toggle="tab" data-bs-target="#gerenciar-prestadores" type="button" role="tab">
                            <i class="fas fa-users-cog me-2"></i> Gerenciar Prestadores
                        </button>
                    </li>
                    <li class="nav-item" role="presentation">
                        <button class="nav-link" id="historico-envios-tab" data-bs-toggle="tab" data-bs-target="#historico-envios" type="button" role="tab">
                            <i class="fas fa-history me-2"></i> Histórico
                        </button>
                    </li>
                    <li class="nav-item" role="presentation">
                        <button class="nav-link" id="editor-pdf-tab" data-bs-toggle="tab" data-bs-target="#editor-pdf" type="button" role="tab">
                            <i class="fas fa-file-pdf me-2"></i> Editor PDF
                        </button>
                    </li>
                </ul>
                
                <div class="tab-content" id="prestadoresTabContent">
                    <!-- Tab Enviar Boletins -->
                    <div class="tab-pane fade show active" id="enviar-boletins" role="tabpanel">
                        ${PrestadoresManager.getEnviarBoletinsHTML()}
                    </div>
                    
                    <!-- Tab Gerenciar Prestadores -->
                    <div class="tab-pane fade" id="gerenciar-prestadores" role="tabpanel">
                        ${PrestadoresManager.getGerenciarPrestadoresHTML()}
                    </div>
                    
                    <!-- Tab Histórico -->
                    <div class="tab-pane fade" id="historico-envios" role="tabpanel">
                        ${PrestadoresManager.getHistoricoHTML()}
                    </div>
                    
                    <!-- Tab Editor PDF -->
                    <div class="tab-pane fade" id="editor-pdf" role="tabpanel">
                        ${PrestadoresManager.getEditorPdfHTML()}
                    </div>
                </div>
            </div>
        `;
        
        container.innerHTML = prestadoresHTML;
        
        // Inicializar funcionalidades dos prestadores
        await PrestadoresManager.init();
    }
    
    static async loadMontadores(container) {
        const montadoresHTML = `
            <div class="montadores-page">
                <div class="page-header mb-4">
                    <h2><i class="fas fa-hard-hat text-primary me-2"></i> Montadores</h2>
                    <p class="text-muted">Gerencie montadores e envie pagamentos de montagem</p>
                </div>
                
                <!-- Navegação por Tabs -->
                <ul class="nav nav-tabs" id="montadoresTabs" role="tablist">
                    <li class="nav-item" role="presentation">
                        <button class="nav-link active" id="enviar-pagamentos-tab" data-bs-toggle="tab" data-bs-target="#enviar-pagamentos" type="button" role="tab">
                            <i class="fas fa-money-bill-wave me-2"></i> Enviar Pagamentos
                        </button>
                    </li>
                    <li class="nav-item" role="presentation">
                        <button class="nav-link" id="gerenciar-montadores-tab" data-bs-toggle="tab" data-bs-target="#gerenciar-montadores" type="button" role="tab">
                            <i class="fas fa-users-cog me-2"></i> Gerenciar Montadores
                        </button>
                    </li>
                    <li class="nav-item" role="presentation">
                        <button class="nav-link" id="historico-montagens-tab" data-bs-toggle="tab" data-bs-target="#historico-montagens" type="button" role="tab">
                            <i class="fas fa-history me-2"></i> Histórico
                        </button>
                    </li>
                </ul>
                
                <div class="tab-content" id="montadoresTabContent">
                    <div class="tab-pane fade show active" id="enviar-pagamentos" role="tabpanel">
                        <div class="mt-4">
                            <h4>Enviar Pagamentos de Montagem</h4>
                            <p class="text-muted">Em desenvolvimento...</p>
                        </div>
                    </div>
                    <div class="tab-pane fade" id="gerenciar-montadores" role="tabpanel">
                        <div class="mt-4">
                            <h4>Gerenciar Montadores</h4>
                            <p class="text-muted">Em desenvolvimento...</p>
                        </div>
                    </div>
                    <div class="tab-pane fade" id="historico-montagens" role="tabpanel">
                        <div class="mt-4">
                            <h4>Histórico de Montagens</h4>
                            <p class="text-muted">Em desenvolvimento...</p>
                        </div>
                    </div>
                </div>
            </div>
        `;
        
        container.innerHTML = montadoresHTML;
    }
    
    static toggleSidebar() {
        const sidebar = document.getElementById('sidebar');
        const overlay = document.getElementById('sidebarOverlay');
        
        sidebar.classList.toggle('show');
        overlay.classList.toggle('show');
    }
    
    static closeSidebar() {
        const sidebar = document.getElementById('sidebar');
        const overlay = document.getElementById('sidebarOverlay');
        
        sidebar.classList.remove('show');
        overlay.classList.remove('show');
    }
}

// ===== AUTHENTICATION =====
class AuthManager {
    static deviceCheckInterval = null;
    static isCheckingLogin = false;
    static currentDeviceCode = null;
    
    static async initializeAuth() {
        const token = SessionManager.getToken();
        const user = SessionManager.getUser();
        
        if (token && user) {
            // Verificar se o token ainda é válido
            try {
                // TODO: Implementar verificação de token com a API
                showMainApp(user);
                return true;
            } catch (error) {
                console.log('Token inválido, redirecionando para login');
                SessionManager.clearSession();
            }
        }
        
        showLoginScreen();
        return false;
    }
    
    static async login() {
        Logger.info('🔐 Iniciando processo de login...');
        
        // Limpar verificações anteriores
        if (AuthManager.deviceCheckInterval) {
            Logger.info('🧹 Limpando verificações anteriores...');
            clearInterval(AuthManager.deviceCheckInterval);
            AuthManager.deviceCheckInterval = null;
            AuthManager.currentDeviceCode = null;
        }
        
        try {
            NotificationSystem.showSpinner('Iniciando login com Office 365...');
            Logger.info('📡 Fazendo requisição para /auth/login');
            
            // Iniciar device code flow
            const response = await APIClient.post('/auth/login');
            Logger.info('📡 Resposta do /auth/login:', response);
            
            if (!response.success) {
                Logger.error('❌ Erro na resposta do login:', response);
                throw new Error(response.message || 'Erro ao iniciar login');
            }
            
            Logger.info('✅ Device code gerado com sucesso:', response.data);
            NotificationSystem.hideSpinner();
            
            // Mostrar mensagem do device code
            const deviceInfo = document.getElementById('loginMessage');
            const deviceData = response.data;
            deviceInfo.innerHTML = `
                <div class="alert alert-info">
                    <h6><i class="fas fa-info-circle me-2"></i>Para completar o login:</h6>
                    <ol class="mb-2">
                        <li>Acesse <strong><a href="${deviceData.verification_uri}" target="_blank">${deviceData.verification_uri}</a></strong></li>
                        <li>Digite o código: <strong>${deviceData.user_code}</strong></li>
                        <li>Aguarde a confirmação</li>
                    </ol>
                    <div class="text-center">
                        <button id="checkLoginButton" class="btn btn-primary btn-sm">
                            <i class="fas fa-sync-alt me-1"></i>Verificar Login
                        </button>
                    </div>
                </div>
            `;
            
            // Configurar botão de verificação
            const checkButton = document.getElementById('checkLoginButton');
            if (checkButton) {
                Logger.info('✅ Botão Verificar Login encontrado, adicionando listener');
                checkButton.addEventListener('click', () => {
                    Logger.info('🖱️ Botão Verificar Login clicado!');
                    AuthManager.checkDeviceLogin(deviceData.device_code);
                });
            } else {
                Logger.error('❌ Botão Verificar Login não encontrado!');
            }
            
            // Auto-verificar periodicamente
            Logger.info('⏰ Configurando auto-verificação a cada', deviceData.interval || 5, 'segundos');
            AuthManager.deviceCheckInterval = setInterval(() => {
                AuthManager.checkDeviceLogin(deviceData.device_code);
            }, (deviceData.interval * 1000) || 5000);
            
            // Timeout de 10 minutos para parar verificações automáticas
            setTimeout(() => {
                if (AuthManager.deviceCheckInterval) {
                    Logger.info('⏰ Timeout atingido, parando verificações automáticas');
                    clearInterval(AuthManager.deviceCheckInterval);
                    AuthManager.deviceCheckInterval = null;
                    AuthManager.currentDeviceCode = null;
                }
            }, 10 * 60 * 1000); // 10 minutos
            
        } catch (error) {
            Logger.error('❌ Erro no login:', error);
            console.error('Erro no login:', error);
            NotificationSystem.error('Erro ao iniciar login: ' + error.message);
            NotificationSystem.hideSpinner();
        }
    }
    
    static async checkDeviceLogin(deviceCode) {
        // Evitar múltiplas verificações simultâneas
        if (AuthManager.isCheckingLogin) {
            Logger.debug('⏸️ Verificação já em andamento, aguardando...');
            return;
        }
        
        // Se o código mudou, parar verificações anteriores
        if (AuthManager.currentDeviceCode && AuthManager.currentDeviceCode !== deviceCode) {
            Logger.info('� Novo device code detectado, limpando verificações anteriores');
            clearInterval(AuthManager.deviceCheckInterval);
            AuthManager.currentDeviceCode = null;
        }
        
        AuthManager.isCheckingLogin = true;
        AuthManager.currentDeviceCode = deviceCode;
        Logger.info('�🔍 Verificando status do device login...');
        
        try {
            const response = await APIClient.post('/auth/verify', { device_code: deviceCode });
            Logger.info('📡 Resposta do /auth/verify:', response);
            
            if (response.success && response.data && response.data.access_token) {
                // Login concluído
                Logger.info('✅ Login concluído com sucesso!');
                clearInterval(AuthManager.deviceCheckInterval);
                AuthManager.deviceCheckInterval = null;
                AuthManager.currentDeviceCode = null;
                
                SessionManager.saveToken(response.data.access_token);
                SessionManager.saveUser(response.data.user);
                
                showMainApp(response.data.user);
                NotificationSystem.success('Login realizado com sucesso!');
                
            } else if (response.error && !response.pending) {
                // Erro real
                Logger.error('❌ Erro no login:', response.error);
                clearInterval(AuthManager.deviceCheckInterval);
                AuthManager.deviceCheckInterval = null;
                AuthManager.currentDeviceCode = null;
                NotificationSystem.error('Erro no login: ' + response.error);
            } else {
                // Aguardando autorização
                Logger.debug('⏳ Aguardando autorização do usuário...');
            }
            
        } catch (error) {
            Logger.error('❌ Erro ao verificar device login:', error);
            clearInterval(AuthManager.deviceCheckInterval);
            AuthManager.deviceCheckInterval = null;
            AuthManager.currentDeviceCode = null;
            console.error('Erro ao verificar login:', error);
            NotificationSystem.error('Erro ao verificar login: ' + error.message);
        } finally {
            AuthManager.isCheckingLogin = false;
        }
    }
    
    static logout() {
        SessionManager.clearSession();
        NotificationSystem.info('Logout realizado com sucesso!');
    }
}

// ===== UI FUNCTIONS =====
function showLoginScreen() {
    document.getElementById('loginScreen').classList.remove('d-none');
    document.getElementById('mainApp').classList.add('d-none');
}

function showMainApp(user) {
    document.getElementById('loginScreen').classList.add('d-none');
    document.getElementById('mainApp').classList.remove('d-none');
    
    // Atualizar informações do usuário
    document.getElementById('userName').textContent = user.name;
    document.getElementById('topBarUserName').textContent = user.name;
    
    // Carregar página inicial
    PageManager.navigateTo('dashboard');
}

// ===== EVENT LISTENERS =====
document.addEventListener('DOMContentLoaded', function() {
    // Inicializar sistema de logs
    LogViewer.init();
    Logger.info('🚀 Aplicação iniciada');
    
    // Login button
    document.getElementById('loginButton').addEventListener('click', AuthManager.login);
    
    // Logout buttons
    document.getElementById('logoutButton').addEventListener('click', AuthManager.logout);
    document.getElementById('logoutButtonTop').addEventListener('click', AuthManager.logout);
    
    // Sidebar navigation
    document.querySelectorAll('[data-page]').forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const page = this.getAttribute('data-page');
            PageManager.navigateTo(page);
        });
    });
    
    // Mobile menu toggle
    document.getElementById('menuToggle').addEventListener('click', PageManager.toggleSidebar);
    document.getElementById('sidebarToggle').addEventListener('click', PageManager.toggleSidebar);
    
    // Sidebar overlay click (mobile)
    document.getElementById('sidebarOverlay').addEventListener('click', PageManager.closeSidebar);
    
    // Initialize authentication
    AuthManager.initializeAuth();
});

// ===== GLOBAL ERROR HANDLER =====
window.addEventListener('error', function(e) {
    console.error('Global error:', e.error);
    NotificationSystem.error('Ocorreu um erro inesperado. Verifique o console para mais detalhes.');
});

window.addEventListener('unhandledrejection', function(e) {
    Logger.error('Unhandled promise rejection:', e.reason);
    console.error('Unhandled promise rejection:', e.reason);
    NotificationSystem.error('Erro na aplicação: ' + e.reason);
});

// ===== LOG VIEWER =====
class LogViewer {
    static init() {
        const showLogsButton = document.getElementById('showLogsButton');
        const refreshLogsButton = document.getElementById('refreshLogsButton');
        const clearLogsButton = document.getElementById('clearLogsButton');
        
        if (showLogsButton) {
            showLogsButton.addEventListener('click', () => this.showLogs());
        }
        
        if (refreshLogsButton) {
            refreshLogsButton.addEventListener('click', () => this.refreshLogs());
        }
        
        if (clearLogsButton) {
            clearLogsButton.addEventListener('click', () => this.clearLogs());
        }
    }
    
    static showLogs() {
        this.refreshLogs();
        const modal = new bootstrap.Modal(document.getElementById('logsModal'));
        modal.show();
    }
    
    static refreshLogs() {
        const logs = Logger.getLogs();
        const container = document.getElementById('logsContainer');
        
        if (!container) return;
        
        const logHtml = logs.map(log => {
            const levelColor = this.getLevelColor(log.level);
            const dataStr = log.data ? ` | ${JSON.stringify(log.data)}` : '';
            
            return `
                <div style="color: ${levelColor}; margin-bottom: 5px;">
                    <strong>[${log.timestamp}]</strong> 
                    <span style="background: ${levelColor}20; padding: 2px 6px; border-radius: 3px;">
                        ${log.level.toUpperCase()}
                    </span> 
                    ${log.message}${dataStr}
                </div>
            `;
        }).join('');
        
        container.innerHTML = logHtml || '<div class="text-muted">Nenhum log encontrado</div>';
        container.scrollTop = container.scrollHeight;
    }
    
    static clearLogs() {
        Logger.clearLogs();
        this.refreshLogs();
        NotificationSystem.success('Logs limpos com sucesso');
    }
    
    static getLevelColor(level) {
        const colors = {
            'error': '#dc3545',
            'warn': '#fd7e14',
            'info': '#0d6efd',
            'debug': '#6c757d'
        };
        return colors[level.toLowerCase()] || '#6c757d';
    }
}

// ===== UTILITY FUNCTIONS =====
function formatDate(date) {
    return new Date(date).toLocaleDateString('pt-BR');
}

function formatCurrency(value) {
    return new Intl.NumberFormat('pt-BR', {
        style: 'currency',
        currency: 'BRL'
    }).format(value);
}

function formatStatus(status) {
    const statusMap = {
        'Em Aberto': 'status-open',
        'Pago': 'status-paid',
        'Cancelado': 'status-cancelled',
        'N.F. RECEBIDA': 'status-received'
    };
    
    const cssClass = statusMap[status] || 'status-open';
    return `<span class="status-badge ${cssClass}">${status}</span>`;
}

// ===== PRESTADORES MANAGER =====
class PrestadoresManager {
    static prestadores = [];
    static configuracoes = {};
    static manualEntries = [];
    
    static async init() {
        Logger.info('🏢 Inicializando módulo de prestadores...');
        
        // Carregar dados iniciais
        await this.loadPrestadores();
        await this.loadConfiguracoes();
        
        // Configurar event listeners
        this.setupEventListeners();
        
        Logger.info('✅ Módulo de prestadores inicializado');
    }
    
    static async loadPrestadores() {
        try {
            const response = await APIClient.get('/prestadores');
            this.prestadores = response || [];
            Logger.info(`📋 ${this.prestadores.length} prestadores carregados`);
        } catch (error) {
            Logger.error('❌ Erro ao carregar prestadores:', error);
            this.prestadores = [];
        }
    }
    
    static async loadConfiguracoes() {
        try {
            const response = await APIClient.get('/prestadores/config');
            this.configuracoes = response?.data || {};
            Logger.info('⚙️ Configurações carregadas:', this.configuracoes);
        } catch (error) {
            Logger.error('❌ Erro ao carregar configurações:', error);
            this.configuracoes = {};
        }
    }
    
    static preencherConfiguracoesEmail() {
        // Preencher campos com configurações salvas
        if (this.configuracoes) {
            const ccInput = document.getElementById('prestadorCC');
            const subjectInput = document.getElementById('prestadorSubject');
            const bodyInput = document.getElementById('prestadorBody');
            
            if (ccInput && this.configuracoes.prestador_cc) {
                ccInput.value = this.configuracoes.prestador_cc;
            }
            
            if (subjectInput && this.configuracoes.prestador_subject) {
                subjectInput.value = this.configuracoes.prestador_subject;
            }
            
            if (bodyInput && this.configuracoes.prestador_body) {
                bodyInput.value = this.configuracoes.prestador_body;
            }
            
            Logger.info('✅ Campos de email preenchidos com configurações salvas');
        }
    }
    
    static setupEventListeners() {
        // Event listeners para tabs
        document.addEventListener('shown.bs.tab', (e) => {
            const tabId = e.target.getAttribute('data-bs-target');
            if (tabId === '#gerenciar-prestadores') {
                this.refreshPrestadoresList();
            } else if (tabId === '#historico-envios') {
                this.loadHistorico();
            } else if (tabId === '#enviar-boletins') {
                this.preencherConfiguracoesEmail();
            }
        });
        
        // Event listener para expansão da blacklist
        document.addEventListener('shown.bs.collapse', (e) => {
            if (e.target.id === 'blacklist-section') {
                this.loadBlacklist();
            }
        });
        
        // Configurar listeners após DOM estar pronto
        setTimeout(() => {
            this.setupFormListeners();
        }, 100);
    }
    
    static setupFormListeners() {
        // Formulário manual de boletins
        const manualForm = document.getElementById('manualBoletimForm');
        if (manualForm) {
            manualForm.addEventListener('submit', (e) => {
                e.preventDefault();
                this.adicionarBoletimManual();
            });
        }
        
        // Formulário novo prestador
        const novoPrestadorForm = document.getElementById('novoPrestadorForm');
        if (novoPrestadorForm) {
            novoPrestadorForm.addEventListener('submit', (e) => {
                e.preventDefault();
                this.criarNovoPrestador();
            });
        }
        
        // Cálculo automático do valor total
        const valorInput = document.getElementById('valorInput');
        const valorExtraInput = document.getElementById('valorExtraInput');
        
        if (valorInput && valorExtraInput) {
            const updateTotal = () => {
                const valor = parseFloat(valorInput.value) || 0;
                const valorExtra = parseFloat(valorExtraInput.value) || 0;
                const total = valor + valorExtra;
                const displayElement = document.getElementById('valorTotalDisplay');
                if (displayElement) {
                    displayElement.value = `R$ ${total.toFixed(2)}`;
                }
            };
            
            valorInput.addEventListener('input', updateTotal);
            valorExtraInput.addEventListener('input', updateTotal);
        }
        
        // Popular selects de prestadores
        this.populatePrestadorSelects();
    }
    
    static getEnviarBoletinsHTML() {
        return `
            <div class="mt-4">
                <h4><i class="fas fa-paper-plane me-2"></i>Envio de Boletins de Serviço</h4>
                
                <!-- Método de Input -->
                <ul class="nav nav-pills mb-4" id="inputMethodTabs" role="tablist">
                    <li class="nav-item" role="presentation">
                        <button class="nav-link active" id="manual-tab" data-bs-toggle="pill" data-bs-target="#manual-input" type="button" role="tab">
                            <i class="fas fa-edit me-2"></i>Lançamento Manual
                        </button>
                    </li>
                    <li class="nav-item" role="presentation">
                        <button class="nav-link" id="excel-tab" data-bs-toggle="pill" data-bs-target="#excel-input" type="button" role="tab">
                            <i class="fas fa-file-excel me-2"></i>Importar via Excel
                        </button>
                    </li>
                </ul>
                
                <div class="tab-content" id="inputMethodContent">
                    <!-- Lançamento Manual -->
                    <div class="tab-pane fade show active" id="manual-input" role="tabpanel">
                        <div class="card">
                            <div class="card-header">
                                <h5 class="mb-0">Adicionar Boletim Manualmente</h5>
                            </div>
                            <div class="card-body">
                                <form id="manualBoletimForm">
                                    <div class="row">
                                        <div class="col-md-6 mb-3">
                                            <label class="form-label">Prestador *</label>
                                            <select class="form-select" id="prestadorSelect" required>
                                                <option value="">Selecione um prestador</option>
                                            </select>
                                        </div>
                                        <div class="col-md-6 mb-3">
                                            <label class="form-label">Período *</label>
                                            <input type="text" class="form-control" id="periodoInput" placeholder="Ex: Janeiro/2024" required>
                                        </div>
                                    </div>
                                    <div class="row">
                                        <div class="col-md-4 mb-3">
                                            <label class="form-label">O.S *</label>
                                            <input type="text" class="form-control" id="osInput" placeholder="Número da O.S." required>
                                        </div>
                                        <div class="col-md-4 mb-3">
                                            <label class="form-label">Modalidade</label>
                                            <input type="text" class="form-control" id="modalidadeInput" placeholder="Tipo de serviço">
                                        </div>
                                        <div class="col-md-4 mb-3">
                                            <label class="form-label">Data de Execução *</label>
                                            <input type="date" class="form-control" id="dataExecucaoInput" required>
                                        </div>
                                    </div>
                                    <div class="row">
                                        <div class="col-md-4 mb-3">
                                            <label class="form-label">Valor (R$) *</label>
                                            <input type="number" class="form-control" id="valorInput" step="0.01" min="0" required>
                                        </div>
                                        <div class="col-md-4 mb-3">
                                            <label class="form-label">Valor Extra (R$)</label>
                                            <input type="number" class="form-control" id="valorExtraInput" step="0.01" min="0" value="0">
                                        </div>
                                        <div class="col-md-4 mb-3">
                                            <label class="form-label">Valor Total</label>
                                            <input type="text" class="form-control" id="valorTotalDisplay" readonly>
                                        </div>
                                    </div>
                                    <div class="mb-3">
                                        <label class="form-label">Motivo Valor Extra</label>
                                        <input type="text" class="form-control" id="motivoExtraInput" placeholder="Justificativa para valor extra">
                                    </div>
                                    <button type="submit" class="btn btn-success">
                                        <i class="fas fa-plus me-2"></i>Adicionar à Lista
                                    </button>
                                </form>
                            </div>
                        </div>
                        
                        <!-- Lista de Entradas Manuais -->
                        <div id="manualEntriesList" class="mt-4" style="display: none;">
                            <div class="card">
                                <div class="card-header d-flex justify-content-between align-items-center">
                                    <h5 class="mb-0">Lista para Envio</h5>
                                    <button type="button" class="btn btn-outline-danger btn-sm" onclick="PrestadoresManager.clearManualEntries()">
                                        <i class="fas fa-trash me-1"></i>Limpar Lista
                                    </button>
                                </div>
                                <div class="card-body">
                                    <div class="table-responsive">
                                        <table class="table table-sm" id="manualEntriesTable">
                                            <thead>
                                                <tr>
                                                    <th>Prestador</th>
                                                    <th>Período</th>
                                                    <th>O.S.</th>
                                                    <th>Modalidade</th>
                                                    <th>Data</th>
                                                    <th>Valor Total</th>
                                                    <th>Ações</th>
                                                </tr>
                                            </thead>
                                            <tbody></tbody>
                                        </table>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                    
                    <!-- Importar via Excel -->
                    <div class="tab-pane fade" id="excel-input" role="tabpanel">
                        <div class="card">
                            <div class="card-header">
                                <h5 class="mb-0">Importar Planilha Excel</h5>
                            </div>
                            <div class="card-body">
                                <div class="mb-3">
                                    <label class="form-label">Arquivo Excel</label>
                                    <input type="file" class="form-control" id="excelFileInput" accept=".xlsx,.xls">
                                    <div class="form-text">
                                        Colunas obrigatórias: nome_prestador, periodo, data_execucao, o_s
                                    </div>
                                </div>
                                <button type="button" class="btn btn-primary" onclick="PrestadoresManager.processExcel()">
                                    <i class="fas fa-upload me-2"></i>Processar Excel
                                </button>
                                
                                <div id="excelPreview" class="mt-4" style="display: none;">
                                    <!-- Preview do Excel será inserido aqui -->
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                
                <!-- Seção de Envio -->
                <div id="envioSection" class="mt-4" style="display: none;">
                    <hr>
                    <h4><i class="fas fa-rocket me-2"></i>Disparar E-mails de Serviço</h4>
                    
                    <!-- Configurações de Envio -->
                    <div class="card mb-4">
                        <div class="card-header">
                            <h5 class="mb-0">
                                <i class="fas fa-cog me-2"></i>Configurações de Envio
                                <button class="btn btn-outline-info btn-sm float-end" type="button" data-bs-toggle="collapse" data-bs-target="#variaveis-info">
                                    <i class="fas fa-info-circle me-1"></i>Variáveis Disponíveis
                                </button>
                            </h5>
                        </div>
                        <div class="collapse" id="variaveis-info">
                            <div class="card-body bg-light">
                                <h6>Variáveis Disponíveis:</h6>
                                <ul class="mb-0">
                                    <li><code>{{nome_prestador}}</code> - Nome do prestador</li>
                                    <li><code>{{periodo}}</code> - Período do serviço</li>
                                    <li><code>{{saudacao}}</code> - Saudação baseada no horário</li>
                                    <li><code>{{lote_id}}</code> - ID do lote gerado</li>
                                </ul>
                            </div>
                        </div>
                        <div class="card-body">
                            <div class="row">
                                <div class="col-md-12 mb-3">
                                    <label class="form-label">CC (Cópia)</label>
                                    <input type="email" class="form-control" id="prestadorCC" placeholder="email1@empresa.com, email2@empresa.com">
                                    <small class="form-text text-muted">Use vírgula para separar múltiplos emails</small>
                                </div>
                                <div class="col-md-12 mb-3">
                                    <label class="form-label">Assunto</label>
                                    <input type="text" class="form-control" id="prestadorSubject" placeholder="Ex: Boletim de Serviços - {{periodo}}">
                                    <small class="form-text text-muted">Use variáveis como {{nome_prestador}} e {{periodo}}</small>
                                </div>
                                <div class="col-md-12 mb-3">
                                    <label class="form-label">Corpo do E-mail</label>
                                    <textarea class="form-control" id="prestadorBody" rows="4" placeholder="Ex: {{saudacao}}, segue em anexo o boletim referente ao período {{periodo}}."></textarea>
                                    <small class="form-text text-muted">Escreva a mensagem que acompanhará o PDF</small>
                                </div>
                            </div>
                        </div>
                    </div>
                    
                    <!-- Botão de Envio -->
                    <div class="text-end">
                        <button type="button" class="btn btn-success btn-lg" onclick="PrestadoresManager.enviarBoletins()">
                            <i class="fas fa-paper-plane me-2"></i>ENVIAR E-MAILS PENDENTES
                        </button>
                    </div>
                </div>
            </div>
        `;
    }
    
    static getGerenciarPrestadoresHTML() {
        return `
            <div class="mt-4">
                <h4><i class="fas fa-users-cog me-2"></i>Gerenciar Prestadores</h4>
                
                <!-- Blacklist de O.S. -->
                <div class="card mb-4">
                    <div class="card-header">
                        <h5 class="mb-0">
                            <i class="fas fa-ban me-2"></i>Blacklist de O.S.
                            <button class="btn btn-outline-primary btn-sm float-end" type="button" data-bs-toggle="collapse" data-bs-target="#blacklist-section">
                                <i class="fas fa-eye me-1"></i>Ver/Gerenciar
                            </button>
                        </h5>
                    </div>
                    <div class="collapse" id="blacklist-section">
                        <div class="card-body">
                            <!-- Adicionar à Blacklist -->
                            <div class="row mb-4">
                                <div class="col-md-4">
                                    <label class="form-label">Prestador</label>
                                    <select class="form-select" id="blacklistPrestadorSelect">
                                        <option value="">Selecione um prestador</option>
                                    </select>
                                </div>
                                <div class="col-md-4">
                                    <label class="form-label">Números das O.S. (separados por vírgula)</label>
                                    <input type="text" class="form-control" id="blacklistOsInput" placeholder="12345, 12346, 12347">
                                </div>
                                <div class="col-md-4">
                                    <label class="form-label">Motivo (opcional)</label>
                                    <input type="text" class="form-control" id="blacklistMotivoInput" placeholder="Motivo da blacklist">
                                </div>
                            </div>
                            <button type="button" class="btn btn-warning mb-4" onclick="PrestadoresManager.adicionarBlacklist()">
                                <i class="fas fa-ban me-2"></i>Adicionar à Blacklist
                            </button>
                            
                            <!-- Lista da Blacklist -->
                            <div id="blacklistList">
                                <!-- Lista será carregada dinamicamente -->
                            </div>
                        </div>
                    </div>
                </div>
                
                <!-- Cadastrar Novo Prestador -->
                <div class="card mb-4">
                    <div class="card-header">
                        <h5 class="mb-0">Adicionar Novo Prestador</h5>
                    </div>
                    <div class="card-body">
                        <form id="novoPrestadorForm">
                            <div class="row">
                                <div class="col-md-6 mb-3">
                                    <label class="form-label">Nome *</label>
                                    <input type="text" class="form-control" id="nomeNovoPrestador" required>
                                </div>
                                <div class="col-md-6 mb-3">
                                    <label class="form-label">E-mail Principal *</label>
                                    <input type="email" class="form-control" id="emailNovoPrestador" required>
                                </div>
                            </div>
                            <div class="row">
                                <div class="col-md-6 mb-3">
                                    <label class="form-label">E-mails Adicionais</label>
                                    <input type="text" class="form-control" id="emailsAdicionaisNovoPrestador" placeholder="email2@empresa.com, email3@empresa.com">
                                    <div class="form-text">Digite os emails adicionais separados por vírgula</div>
                                </div>
                                <div class="col-md-6 mb-3">
                                    <label class="form-label">Número do Fornecedor *</label>
                                    <input type="text" class="form-control" id="fornecedorIdNovoPrestador" required>
                                </div>
                            </div>
                            <div class="row">
                                <div class="col-md-6 mb-3">
                                    <label class="form-label">Regra de Envio</label>
                                    <select class="form-select" id="regraEnvioNovoPrestador">
                                        <option value="Nenhuma">Nenhuma</option>
                                        <option value="Semanal">Semanal</option>
                                        <option value="Mensal (Dia Fixo)">Mensal (Dia Fixo)</option>
                                        <option value="Quinzenal">Quinzenal</option>
                                    </select>
                                </div>
                                <div class="col-md-6 mb-3">
                                    <label class="form-label">Dias de Envio</label>
                                    <input type="text" class="form-control" id="diasEnvioNovoPrestador" placeholder="Ex: Segunda-feira ou 5,20">
                                    <div class="form-text">Para semanal: dia da semana. Para mensal/quinzenal: dias do mês</div>
                                </div>
                            </div>
                            <button type="submit" class="btn btn-success">
                                <i class="fas fa-plus me-2"></i>Adicionar Prestador
                            </button>
                        </form>
                    </div>
                </div>
                
                <!-- Lista de Prestadores Cadastrados -->
                <div class="card">
                    <div class="card-header d-flex justify-content-between align-items-center">
                        <h5 class="mb-0">Prestadores Cadastrados</h5>
                        <button type="button" class="btn btn-outline-primary btn-sm" onclick="PrestadoresManager.refreshPrestadoresList()">
                            <i class="fas fa-sync-alt me-1"></i>Atualizar Lista
                        </button>
                    </div>
                    <div class="card-body">
                        <div id="prestadoresList">
                            <!-- Lista será carregada dinamicamente -->
                        </div>
                    </div>
                </div>
            </div>
        `;
    }
    
    static getHistoricoHTML() {
        return `
            <div class="mt-4">
                <h4><i class="fas fa-history me-2"></i>Histórico de Lotes Enviados</h4>
                
                <div class="card">
                    <div class="card-header d-flex justify-content-between align-items-center">
                        <div>
                            <label class="form-label mb-0 me-3">Filtrar por Status:</label>
                            <select class="form-select d-inline-block" id="statusFilter" style="width: auto;" onchange="PrestadoresManager.loadHistorico()">
                                <option value="Todos">Todos</option>
                                <option value="Em Aberto">Em Aberto</option>
                                <option value="Pago">Pago</option>
                                <option value="Cancelado">Cancelado</option>
                                <option value="N.F. RECEBIDA">N.F. RECEBIDA</option>
                            </select>
                        </div>
                        <button type="button" class="btn btn-outline-primary btn-sm" onclick="PrestadoresManager.loadHistorico()">
                            <i class="fas fa-sync-alt me-1"></i>Atualizar
                        </button>
                    </div>
                    <div class="card-body">
                        <div id="historicoList">
                            <div class="text-center py-4">
                                <div class="spinner-border text-primary" role="status">
                                    <span class="visually-hidden">Carregando...</span>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        `;
    }
    
    static getEditorPdfHTML() {
        return `
            <div class="mt-4">
                <h4><i class="fas fa-file-pdf me-2"></i>Editor de Template do PDF</h4>
                
                <div class="card">
                    <div class="card-header d-flex justify-content-between align-items-center">
                        <h5 class="mb-0">Template HTML do PDF</h5>
                        <div>
                            <button type="button" class="btn btn-info btn-sm me-2" onclick="PrestadoresManager.previewTemplate()">
                                <i class="fas fa-eye me-1"></i>Preview
                            </button>
                            <button type="button" class="btn btn-success btn-sm" onclick="PrestadoresManager.salvarTemplate()">
                                <i class="fas fa-save me-1"></i>Salvar Template
                            </button>
                        </div>
                    </div>
                    <div class="card-body">
                        <textarea class="form-control" id="templateEditor" rows="20" style="font-family: monospace; font-size: 14px;">
                            <!-- Template será carregado aqui -->
                        </textarea>
                        <div class="form-text">
                            Você pode usar HTML e CSS para customizar o template do PDF. Variáveis disponíveis: {{nome_prestador}}, {{periodo}}, {{items}}, {{total_geral}}, {{saudacao}}, {{lote_id}}
                        </div>
                    </div>
                </div>
            </div>
        `;
    }
    
    // Métodos de funcionalidade (serão implementados a seguir)
    static async refreshPrestadoresList() {
        Logger.info('🔄 Atualizando lista de prestadores...');
        
        try {
            await this.loadPrestadores();
            this.populatePrestadorSelects();
            this.renderPrestadoresList();
            NotificationSystem.success('Lista de prestadores atualizada!');
        } catch (error) {
            Logger.error('❌ Erro ao atualizar prestadores:', error);
            NotificationSystem.error('Erro ao atualizar lista de prestadores');
        }
    }
    
    static populatePrestadorSelects() {
        const selects = ['prestadorSelect', 'blacklistPrestadorSelect'];
        
        selects.forEach(selectId => {
            const select = document.getElementById(selectId);
            if (select) {
                select.innerHTML = '<option value="">Selecione um prestador</option>';
                this.prestadores.forEach(prestador => {
                    const option = document.createElement('option');
                    option.value = prestador.id; // Usar ID ao invés do nome
                    option.textContent = prestador.nome;
                    option.dataset.nome = prestador.nome; // Guardar nome no dataset se necessário
                    select.appendChild(option);
                });
            }
        });
    }
    
    static renderPrestadoresList() {
        const container = document.getElementById('prestadoresList');
        if (!container) return;
        
        if (this.prestadores.length === 0) {
            container.innerHTML = '<div class="alert alert-info">Nenhum prestador cadastrado.</div>';
            return;
        }
        
        const html = this.prestadores.map(prestador => `
            <div class="card mb-3">
                <div class="card-header">
                    <h6 class="mb-0">${prestador.nome} - ID: ${prestador.id}</h6>
                </div>
                <div class="card-body">
                    <div class="row">
                        <div class="col-md-6">
                            <p><strong>E-mail Principal:</strong> ${prestador.email}</p>
                            ${prestador.emails_adicionais ? `<p><strong>E-mails Adicionais:</strong> ${prestador.emails_adicionais}</p>` : ''}
                            <p><strong>Fornecedor ID:</strong> ${prestador.fornecedor_id}</p>
                        </div>
                        <div class="col-md-6">
                            <p><strong>Regra de Envio:</strong> ${prestador.regra_envio || 'Nenhuma'}</p>
                            ${prestador.dias_envio ? `<p><strong>Dias de Envio:</strong> ${prestador.dias_envio}</p>` : ''}
                        </div>
                    </div>
                    <div class="mt-3">
                        <button class="btn btn-outline-primary btn-sm me-2" onclick="PrestadoresManager.editarPrestador(${prestador.id})">
                            <i class="fas fa-edit me-1"></i>Editar
                        </button>
                        <button class="btn btn-outline-danger btn-sm" onclick="PrestadoresManager.deletarPrestador(${prestador.id}, '${prestador.nome}')">
                            <i class="fas fa-trash me-1"></i>Excluir
                        </button>
                    </div>
                </div>
            </div>
        `).join('');
        
        container.innerHTML = html;
    }
    
    static adicionarBoletimManual() {
        const form = document.getElementById('manualBoletimForm');
        const formData = new FormData(form);
        
        const prestadorSelect = document.getElementById('prestadorSelect');
        const prestadorId = prestadorSelect.value;
        const prestadorNome = prestadorSelect.options[prestadorSelect.selectedIndex]?.dataset.nome || prestadorSelect.options[prestadorSelect.selectedIndex]?.textContent;
        
        const periodo = document.getElementById('periodoInput').value;
        const os = document.getElementById('osInput').value;
        const modalidade = document.getElementById('modalidadeInput').value;
        const dataExecucao = document.getElementById('dataExecucaoInput').value;
        const valor = parseFloat(document.getElementById('valorInput').value) || 0;
        const valorExtra = parseFloat(document.getElementById('valorExtraInput').value) || 0;
        const motivoExtra = document.getElementById('motivoExtraInput').value;
        
        if (!prestadorId || !periodo || !os || !dataExecucao || valor <= 0) {
            NotificationSystem.error('Preencha todos os campos obrigatórios!');
            return;
        }
        
        const boletim = {
            nome_prestador: prestadorNome,
            periodo: periodo,
            o_s: os,
            modalidade: modalidade || 'Serviço',
            data_execucao: dataExecucao,
            valor_custo_prestador: valor,
            valor_extra: valorExtra,
            motivo_extra: motivoExtra,
            valor_total: valor + valorExtra
        };
        
        this.manualEntries.push(boletim);
        this.renderManualEntriesList();
        this.showEnvioSection();
        
        // Limpar formulário
        form.reset();
        document.getElementById('valorTotalDisplay').value = '';
        
        NotificationSystem.success('Boletim adicionado à lista!');
        Logger.info('📝 Boletim adicionado:', boletim);
    }
    
    static renderManualEntriesList() {
        const container = document.getElementById('manualEntriesList');
        const tbody = document.getElementById('manualEntriesTable').querySelector('tbody');
        
        if (this.manualEntries.length === 0) {
            container.style.display = 'none';
            return;
        }
        
        container.style.display = 'block';
        
        tbody.innerHTML = this.manualEntries.map((entry, index) => `
            <tr>
                <td>${entry.nome_prestador}</td>
                <td>${entry.periodo}</td>
                <td>${entry.o_s}</td>
                <td>${entry.modalidade}</td>
                <td>${formatDate(entry.data_execucao)}</td>
                <td>${formatCurrency(entry.valor_total)}</td>
                <td>
                    <button class="btn btn-outline-danger btn-sm" onclick="PrestadoresManager.removerBoletimManual(${index})">
                        <i class="fas fa-trash"></i>
                    </button>
                </td>
            </tr>
        `).join('');
    }
    
    static removerBoletimManual(index) {
        this.manualEntries.splice(index, 1);
        this.renderManualEntriesList();
        
        if (this.manualEntries.length === 0) {
            document.getElementById('envioSection').style.display = 'none';
        }
        
        NotificationSystem.success('Boletim removido da lista!');
    }
    
    static showEnvioSection() {
        const section = document.getElementById('envioSection');
        if (section) {
            section.style.display = 'block';
            
            // Carregar configurações nos campos
            document.getElementById('ccInput').value = this.configuracoes.prestador_cc || '';
            document.getElementById('assuntoInput').value = this.configuracoes.prestador_subject || '';
            document.getElementById('corpoEmailInput').value = this.configuracoes.prestador_body || '';
        }
    }
    
    static clearManualEntries() {
        this.manualEntries = [];
        document.getElementById('manualEntriesList').style.display = 'none';
        document.getElementById('envioSection').style.display = 'none';
        NotificationSystem.success('Lista limpa!');
    }
    
    static async criarNovoPrestador() {
        const nome = document.getElementById('nomeNovoPrestador').value;
        const email = document.getElementById('emailNovoPrestador').value;
        const emailsAdicionais = document.getElementById('emailsAdicionaisNovoPrestador').value;
        const fornecedorId = document.getElementById('fornecedorIdNovoPrestador').value;
        const regraEnvio = document.getElementById('regraEnvioNovoPrestador').value;
        const diasEnvio = document.getElementById('diasEnvioNovoPrestador').value;
        
        if (!nome || !email || !fornecedorId) {
            NotificationSystem.error('Preencha todos os campos obrigatórios!');
            return;
        }
        
        try {
            NotificationSystem.showSpinner('Criando prestador...');
            
            const dados = {
                nome,
                email,
                emails_adicionais: emailsAdicionais || null,
                fornecedor_id: fornecedorId,
                regra_envio: regraEnvio,
                dias_envio: diasEnvio || null
            };
            
            const response = await APIClient.post('/prestadores', dados);
            
            if (response.success) {
                NotificationSystem.success('Prestador criado com sucesso!');
                document.getElementById('novoPrestadorForm').reset();
                await this.refreshPrestadoresList();
            } else {
                NotificationSystem.error('Erro ao criar prestador: ' + response.message);
            }
            
        } catch (error) {
            Logger.error('❌ Erro ao criar prestador:', error);
            NotificationSystem.error('Erro ao criar prestador: ' + error.message);
        } finally {
            NotificationSystem.hideSpinner();
        }
    }
    
    static async processExcel() {
        // Implementar processamento de Excel
        NotificationSystem.info('Funcionalidade de Excel em desenvolvimento...');
    }
    
    static async enviarBoletins() {
        try {
            Logger.info('🚀 Iniciando envio de boletins...');
            
            // Coletar dados do formulário de configuração
            const prestadorCC = document.getElementById('prestadorCC')?.value || '';
            const prestadorSubject = document.getElementById('prestadorSubject')?.value || 'Boletim de Serviços';
            const prestadorBody = document.getElementById('prestadorBody')?.value || '';
            
            // Usar boletins manuais já adicionados
            const boletins = [...this.manualEntries];
            
            if (boletins.length === 0) {
                NotificationSystem.error('Adicione pelo menos um boletim para enviar!');
                return;
            }
            
            // Validar campos obrigatórios
            for (let i = 0; i < boletins.length; i++) {
                const boletim = boletins[i];
                if (!boletim.nome_prestador || !boletim.periodo || !boletim.o_s) {
                    NotificationSystem.error(`Boletim ${i + 1}: Preencha os campos obrigatórios (Prestador, Período, O.S.)`);
                    return;
                }
            }
            
            const dadosEnvio = {
                boletins: boletins,
                configuracao: {
                    prestador_cc: prestadorCC,
                    prestador_subject: prestadorSubject,
                    prestador_body: prestadorBody
                }
            };
            
            Logger.info(`📤 Enviando ${boletins.length} boletins...`);
            NotificationSystem.info(`Enviando ${boletins.length} boletins... Aguarde.`);
            
            const response = await APIClient.post('/prestadores/enviar-boletins', dadosEnvio);
            
            if (response.success) {
                NotificationSystem.success(`✅ ${response.enviados} boletins enviados com sucesso!`);
                
                if (response.errors && response.errors.length > 0) {
                    Logger.warning('⚠️ Alguns erros ocorreram:', response.errors);
                    NotificationSystem.warning(`Alguns erros: ${response.errors.slice(0, 3).join(', ')}`);
                }
                
                // Limpar lista de boletins manuais
                this.clearManualEntries();
                
                // Atualizar histórico
                const historicoTab = document.getElementById('historico-envios-tab');
                if (historicoTab) {
                    setTimeout(() => {
                        historicoTab.click();
                    }, 1000);
                }
                
                Logger.info('✅ Envio de boletins concluído com sucesso');
                
            } else {
                throw new Error(response.message || 'Erro desconhecido no envio');
            }
            
        } catch (error) {
            Logger.error('❌ Erro no envio de boletins:', error);
            NotificationSystem.error('Erro ao enviar boletins: ' + error.message);
        }
    }
    
    static async adicionarBlacklist() {
        const osNumeros = document.getElementById('blacklistOsInput')?.value?.trim();
        const prestadorId = document.getElementById('blacklistPrestadorSelect')?.value;
        const motivo = document.getElementById('blacklistMotivoInput')?.value?.trim() || 'Sem motivo especificado';
        
        if (!osNumeros || !prestadorId) {
            NotificationSystem.error('Preencha o número da O.S. e selecione o prestador!');
            return;
        }
        
        try {
            // Suporte para múltiplas O.S. separadas por vírgula 
            const osArray = osNumeros.split(',').map(os => os.trim()).filter(os => os);
            Logger.info(`🚫 Adicionando O.S. ${osArray.join(', ')} à blacklist...`);
            
            const blacklistData = {
                prestador_id: parseInt(prestadorId),
                os_numbers: osArray, // Backend espera 'os_numbers' (inglês)
                motivo: motivo
            };
            
            Logger.info(`📤 Dados sendo enviados:`, blacklistData);
            
            await APIClient.post('/prestadores/blacklist/batch', blacklistData);
            
            NotificationSystem.success(`${osArray.length} O.S. adicionadas à blacklist com sucesso!`);
            
            // Limpar formulário
            document.getElementById('blacklistOsInput').value = '';
            document.getElementById('blacklistMotivoInput').value = '';
            
            // Recarregar lista de blacklist
            await this.loadBlacklist();
            
            Logger.info('✅ O.S. adicionada à blacklist com sucesso');
            
        } catch (error) {
            Logger.error('❌ Erro ao adicionar O.S. à blacklist:', error);
            NotificationSystem.error('Erro ao adicionar à blacklist: ' + error.message);
        }
    }
    
    static async loadBlacklist() {
        try {
            Logger.info('🔄 Carregando blacklist...');
            
            const response = await APIClient.get('/prestadores/blacklist');
            const blacklist = response.data || [];
            
            const blacklistContainer = document.getElementById('blacklistList');
            if (!blacklistContainer) return;
            
            if (blacklist.length === 0) {
                blacklistContainer.innerHTML = `
                    <div class="alert alert-info text-center">
                        <i class="bi bi-info-circle me-2"></i>
                        Nenhuma O.S. na blacklist.
                    </div>
                `;
                return;
            }
            
            let html = '<div class="table-responsive"><table class="table table-striped table-hover">';
            html += `
                <thead class="table-dark">
                    <tr>
                        <th>O.S.</th>
                        <th>Prestador</th>
                        <th>Motivo</th>
                        <th>Data Adição</th>
                        <th>Ações</th>
                    </tr>
                </thead>
                <tbody>
            `;
            
            blacklist.forEach(item => {
                const dataAdicao = new Date(item.data_adicao).toLocaleDateString('pt-BR');
                html += `
                    <tr>
                        <td><code>${item.os_numero}</code></td>
                        <td>${item.prestador_nome || 'N/A'}</td>
                        <td>${item.motivo || 'Sem motivo'}</td>
                        <td>${dataAdicao}</td>
                        <td>
                            <button type="button" class="btn btn-outline-danger btn-sm" onclick="PrestadoresManager.removerBlacklist('${item.prestador_id}', '${item.os_numero}')" title="Remover da Blacklist">
                                <i class="bi bi-trash"></i> Remover
                            </button>
                        </td>
                    </tr>
                `;
            });
            
            html += '</tbody></table></div>';
            blacklistContainer.innerHTML = html;
            
            Logger.info(`✅ Blacklist carregada: ${blacklist.length} itens`);
            
        } catch (error) {
            Logger.error('❌ Erro ao carregar blacklist:', error);
            const blacklistContainer = document.getElementById('blacklistList');
            if (blacklistContainer) {
                blacklistContainer.innerHTML = `
                    <div class="alert alert-danger">
                        <i class="bi bi-exclamation-triangle me-2"></i>
                        Erro ao carregar blacklist: ${error.message}
                    </div>
                `;
            }
        }
    }
    
    static async removerBlacklist(prestadorId, osNumero) {
        if (confirm(`Tem certeza que deseja remover a O.S. ${osNumero} da blacklist?`)) {
            try {
                await APIClient.delete(`/prestadores/blacklist/${prestadorId}/${osNumero}`);
                NotificationSystem.success(`O.S. ${osNumero} removida da blacklist!`);
                await this.loadBlacklist();
            } catch (error) {
                Logger.error('❌ Erro ao remover da blacklist:', error);
                NotificationSystem.error('Erro ao remover da blacklist: ' + error.message);
            }
        }
    }
    
    static async loadHistorico() {
        try {
            Logger.info('🔄 Carregando histórico de envios...');
            
            const statusFilter = document.getElementById('statusFilter')?.value || '';
            let url = '/prestadores/historico';
            if (statusFilter && statusFilter !== 'Todos') {
                url += `?status_filter=${encodeURIComponent(statusFilter)}`;
            }
            
            const response = await APIClient.get(url);
            const historicoData = response.data;
            const historico = historicoData.lotes || [];
            
            const historicoList = document.getElementById('historicoList');
            if (!historicoList) return;
            
            if (!historico || historico.length === 0) {
                historicoList.innerHTML = `
                    <div class="alert alert-info text-center">
                        <i class="bi bi-info-circle me-2"></i>
                        Nenhum histórico de envio encontrado.
                    </div>
                `;
                return;
            }
            
            // Renderizar como cards conforme o sistema original
            let html = '';
            
            historico.forEach(lote => {
                const dataEnvio = new Date(lote.data_envio).toLocaleDateString('pt-BR');
                const valorFormatado = lote.valor_total ? 
                    new Intl.NumberFormat('pt-BR', {style: 'currency', currency: 'BRL'}).format(lote.valor_total) : 
                    'R$ 0,00';
                    
                let statusBadge = 'secondary';
                if (lote.status === 'Em Aberto') statusBadge = 'warning';
                else if (lote.status === 'Pago') statusBadge = 'success';
                else if (lote.status === 'Cancelado') statusBadge = 'danger';
                else if (lote.status === 'N.F. RECEBIDA') statusBadge = 'info';
                
                html += `
                    <div class="card mb-3">
                        <div class="card-header">
                            <div class="row align-items-center">
                                <div class="col-md-2">
                                    <strong>Lote #${lote.id}</strong>
                                </div>
                                <div class="col-md-3">
                                    <strong>${lote.prestador_nome}</strong>
                                </div>
                                <div class="col-md-2">
                                    ${valorFormatado}
                                </div>
                                <div class="col-md-2">
                                    ${dataEnvio}
                                </div>
                                <div class="col-md-3 text-end">
                                    <span class="badge bg-${statusBadge} me-2">${lote.status}</span>
                                    <button class="btn btn-sm btn-outline-primary" onclick="PrestadoresManager.toggleLoteDetails(${lote.id})">
                                        <i class="bi bi-chevron-down" id="chevron-${lote.id}"></i> Ver Detalhes
                                    </button>
                                </div>
                            </div>
                        </div>
                        <div class="card-body collapse" id="lote-details-${lote.id}">
                            <div id="os-table-${lote.id}">
                                <div class="text-center">
                                    <div class="spinner-border text-primary" role="status">
                                        <span class="visually-hidden">Carregando...</span>
                                    </div>
                                </div>
                            </div>
                            <hr>
                            <div class="row">
                                <div class="col-md-6">
                                    <label class="form-label">Alterar Status do Lote:</label>
                                    <select class="form-select mb-2" id="status-select-${lote.id}">
                                        <option value="Em Aberto" ${lote.status === 'Em Aberto' ? 'selected' : ''}>Em Aberto</option>
                                        <option value="Pago" ${lote.status === 'Pago' ? 'selected' : ''}>Pago</option>
                                        <option value="Cancelado" ${lote.status === 'Cancelado' ? 'selected' : ''}>Cancelado</option>
                                        <option value="N.F. RECEBIDA" ${lote.status === 'N.F. RECEBIDA' ? 'selected' : ''}>N.F. RECEBIDA</option>
                                    </select>
                                    <button class="btn btn-success btn-sm" onclick="PrestadoresManager.salvarStatusLote(${lote.id})">
                                        <i class="bi bi-check"></i> Salvar Status
                                    </button>
                                    ${lote.tem_anexo ? 
                                        `<button class="btn btn-info btn-sm ms-2" onclick="PrestadoresManager.downloadAnexo(${lote.id})">
                                            <i class="bi bi-download"></i> Baixar N.F.
                                        </button>` : ''
                                    }
                                </div>
                                <div class="col-md-6 text-end">
                                    <button class="btn btn-danger btn-sm" onclick="PrestadoresManager.excluirLote(${lote.id})">
                                        <i class="bi bi-trash"></i> Excluir Lote
                                    </button>
                                </div>
                            </div>
                        </div>
                    </div>
                `;
            });
            
            historicoList.innerHTML = html;
            
            Logger.info(`✅ Histórico carregado: ${historico.length} lotes`);
            
        } catch (error) {
            Logger.error('❌ Erro ao carregar histórico:', error);
            const historicoList = document.getElementById('historicoList');
            if (historicoList) {
                historicoList.innerHTML = `
                    <div class="alert alert-danger">
                        <i class="bi bi-exclamation-triangle me-2"></i>
                        Erro ao carregar histórico: ${error.message}
                    </div>
                `;
            }
        }
    }
    
    // Método para expandir/colapsar detalhes do lote
    static async toggleLoteDetails(loteId) {
        const detailsDiv = document.getElementById(`lote-details-${loteId}`);
        const chevron = document.getElementById(`chevron-${loteId}`);
        const osTable = document.getElementById(`os-table-${loteId}`);
        
        if (detailsDiv.classList.contains('show')) {
            detailsDiv.classList.remove('show');
            chevron.classList.remove('bi-chevron-up');
            chevron.classList.add('bi-chevron-down');
        } else {
            detailsDiv.classList.add('show');
            chevron.classList.remove('bi-chevron-down');
            chevron.classList.add('bi-chevron-up');
            
            // Carregar O.S. do lote se ainda não carregou
            if (osTable.innerHTML.includes('spinner-border')) {
                await this.carregarOsDoLote(loteId);
            }
        }
    }
    
    // Método para carregar O.S. de um lote específico
    static async carregarOsDoLote(loteId) {
        try {
            const response = await APIClient.get(`/prestadores/historico/${loteId}/os`);
            const osData = response.data;
            const osTable = document.getElementById(`os-table-${loteId}`);
            
            if (!osData || osData.length === 0) {
                osTable.innerHTML = '<div class="alert alert-warning">Não há O.S. detalhadas para este lote.</div>';
                return;
            }
            
            let tableHtml = `
                <div class="table-responsive">
                    <table class="table table-sm table-striped">
                        <thead>
                            <tr>
                                <th>O.S.</th>
                                <th>Data Execução</th>
                                <th>Modalidade</th>
                                <th>Valor</th>
                                <th>Valor Extra</th>
                                <th>Motivo Extra</th>
                            </tr>
                        </thead>
                        <tbody>
            `;
            
            osData.forEach(os => {
                const detalhes = typeof os.detalhes === 'object' ? os.detalhes : JSON.parse(os.detalhes || '{}');
                
                // Extrair valores dos campos (suporta diferentes formatos)
                const valorBase = detalhes.valor_custo_prestador || detalhes.valor || 0;
                const valorExtra = detalhes.valor_extra || 0;
                const motivoExtra = detalhes.motivo_extra || detalhes.motivo_valor_extra || '-';
                
                // Formatar valores em moeda brasileira
                const valorFormatado = parseFloat(valorBase).toLocaleString('pt-BR', {style: 'currency', currency: 'BRL'});
                const valorExtraFormatado = valorExtra > 0 ? parseFloat(valorExtra).toLocaleString('pt-BR', {style: 'currency', currency: 'BRL'}) : '-';
                
                // Formatar data de execução
                let dataExecucao = '-';
                if (detalhes.data_execucao) {
                    try {
                        const date = new Date(detalhes.data_execucao);
                        if (!isNaN(date.getTime())) {
                            dataExecucao = date.toLocaleDateString('pt-BR');
                        } else {
                            dataExecucao = detalhes.data_execucao;
                        }
                    } catch {
                        dataExecucao = detalhes.data_execucao;
                    }
                }
                
                tableHtml += `
                    <tr>
                        <td><code>${os.os_numero}</code></td>
                        <td>${dataExecucao}</td>
                        <td>${detalhes.modalidade || '-'}</td>
                        <td>${valorFormatado}</td>
                        <td>${valorExtraFormatado}</td>
                        <td>${motivoExtra}</td>
                    </tr>
                `;
            });
            
            tableHtml += '</tbody></table></div>';
            osTable.innerHTML = tableHtml;
            
        } catch (error) {
            Logger.error('Erro ao carregar O.S. do lote:', error);
            const osTable = document.getElementById(`os-table-${loteId}`);
            osTable.innerHTML = '<div class="alert alert-danger">Erro ao carregar O.S. do lote.</div>';
        }
    }
    
    // Método para salvar status do lote
    static async salvarStatusLote(loteId) {
        try {
            const statusSelect = document.getElementById(`status-select-${loteId}`);
            const novoStatus = statusSelect.value;
            
            const response = await APIClient.put(`/prestadores/historico/${loteId}/status`, {
                status: novoStatus
            });
            
            if (response.success) {
                NotificationSystem.success(`Status do Lote #${loteId} atualizado para "${novoStatus}"!`);
                await this.loadHistorico(); // Recarregar histórico
            } else {
                throw new Error(response.message || 'Erro ao atualizar status');
            }
            
        } catch (error) {
            Logger.error('Erro ao salvar status do lote:', error);
            NotificationSystem.error('Erro ao atualizar status: ' + error.message);
        }
    }
    
    // Método para excluir lote
    static async excluirLote(loteId) {
        if (!confirm(`Tem certeza que deseja excluir o Lote #${loteId} e todas as suas O.S.?`)) {
            return;
        }
        
        try {
            const response = await APIClient.delete(`/prestadores/historico/${loteId}`);
            
            if (response.success) {
                NotificationSystem.success(`Lote #${loteId} excluído com sucesso!`);
                await this.loadHistorico(); // Recarregar histórico
            } else {
                throw new Error(response.message || 'Erro ao excluir lote');
            }
            
        } catch (error) {
            Logger.error('Erro ao excluir lote:', error);
            NotificationSystem.error('Erro ao excluir lote: ' + error.message);
        }
    }
    
    // Método para download de anexo
    static async downloadAnexo(loteId) {
        try {
            const response = await APIClient.get(`/prestadores/historico/${loteId}/anexo`, {
                responseType: 'blob'
            });
            
            // Criar link de download
            const blob = new Blob([response]);
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `nf_lote_${loteId}.pdf`;
            document.body.appendChild(a);
            a.click();
            window.URL.revokeObjectURL(url);
            document.body.removeChild(a);
            
        } catch (error) {
            Logger.error('Erro ao fazer download do anexo:', error);
            NotificationSystem.error('Erro ao fazer download: ' + error.message);
        }
    }
    
    static async editarPrestador(id) {
        try {
            Logger.info(`🔍 Carregando dados do prestador ${id}...`);
            
            // Buscar dados do prestador
            const prestador = await APIClient.get(`/prestadores/${id}`);
            
            if (!prestador || !prestador.id) {
                NotificationSystem.error('Prestador não encontrado!');
                return;
            }
            
            // Criar modal dinamicamente
            const modalHtml = `
                <div class="modal fade" id="editarPrestadorModal" tabindex="-1">
                    <div class="modal-dialog modal-lg">
                        <div class="modal-content">
                            <div class="modal-header">
                                <h5 class="modal-title">Editar Prestador - ${prestador.nome}</h5>
                                <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                            </div>
                            <div class="modal-body">
                                <form id="editarPrestadorForm">
                                    <input type="hidden" id="editPrestadorId" value="${prestador.id}">
                                    
                                    <div class="row">
                                        <div class="col-md-6 mb-3">
                                            <label class="form-label">Nome *</label>
                                            <input type="text" class="form-control" id="editNome" value="${prestador.nome}" required>
                                        </div>
                                        <div class="col-md-6 mb-3">
                                            <label class="form-label">Email Principal *</label>
                                            <input type="email" class="form-control" id="editEmail" value="${prestador.email}" required>
                                        </div>
                                    </div>
                                    
                                    <div class="row">
                                        <div class="col-md-6 mb-3">
                                            <label class="form-label">Fornecedor ID</label>
                                            <input type="text" class="form-control" id="editFornecedorId" value="${prestador.fornecedor_id || ''}" placeholder="ID do fornecedor (opcional)">
                                        </div>
                                        <div class="col-md-6 mb-3">
                                            <label class="form-label">Regra de Envio</label>
                                            <select class="form-select" id="editRegraEnvio" required>
                                                <option value="Nenhuma" ${prestador.regra_envio === 'Nenhuma' ? 'selected' : ''}>Nenhuma</option>
                                                <option value="Semanal" ${prestador.regra_envio === 'Semanal' ? 'selected' : ''}>Semanal</option>
                                                <option value="Mensal (Dia Fixo)" ${prestador.regra_envio === 'Mensal (Dia Fixo)' ? 'selected' : ''}>Mensal (Dia Fixo)</option>
                                                <option value="Quinzenal" ${prestador.regra_envio === 'Quinzenal' ? 'selected' : ''}>Quinzenal</option>
                                            </select>
                                        </div>
                                    </div>
                                    
                                    <div class="row">
                                        <div class="col-md-6 mb-3">
                                            <label class="form-label">Dias de Envio</label>
                                            <input type="text" class="form-control" id="editDiasEnvio" value="${prestador.dias_envio || ''}" placeholder="Ex: Segunda-feira, 15,30">
                                            <small class="form-text text-muted">Para semanal: nome do dia. Para mensal: dias do mês separados por vírgula.</small>
                                        </div>
                                        <div class="col-md-6 mb-3">
                                            <label class="form-label">Emails Adicionais</label>
                                            <textarea class="form-control" id="editEmailsAdicionais" rows="2" placeholder="email1@exemplo.com, email2@exemplo.com">${prestador.emails_adicionais || ''}</textarea>
                                        </div>
                                    </div>
                                </form>
                            </div>
                            <div class="modal-footer">
                                <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancelar</button>
                                <button type="button" class="btn btn-primary" onclick="PrestadoresManager.salvarEdicaoPrestador()">
                                    <i class="fas fa-save me-2"></i>Salvar Alterações
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
            `;
            
            // Remover modal anterior se existir
            const existingModal = document.getElementById('editarPrestadorModal');
            if (existingModal) {
                existingModal.remove();
            }
            
            // Adicionar modal ao DOM
            document.body.insertAdjacentHTML('beforeend', modalHtml);
            
            // Mostrar modal
            const modal = new bootstrap.Modal(document.getElementById('editarPrestadorModal'));
            modal.show();
            
            // Remover modal do DOM após fechar
            document.getElementById('editarPrestadorModal').addEventListener('hidden.bs.modal', function() {
                this.remove();
            });
            
            Logger.info('✅ Modal de edição carregado com sucesso');
            
        } catch (error) {
            Logger.error('❌ Erro ao carregar dados do prestador:', error);
            NotificationSystem.error('Erro ao carregar prestador: ' + error.message);
        }
    }
    
    static async salvarEdicaoPrestador() {
        try {
            const id = document.getElementById('editPrestadorId').value;
            const dados = {
                nome: document.getElementById('editNome').value.trim(),
                email: document.getElementById('editEmail').value.trim(),
                fornecedor_id: document.getElementById('editFornecedorId').value.trim() || null,
                regra_envio: document.getElementById('editRegraEnvio').value,
                dias_envio: document.getElementById('editDiasEnvio').value.trim() || null,
                emails_adicionais: document.getElementById('editEmailsAdicionais').value.trim() || null
            };
            
            // Validações básicas
            if (!dados.nome || !dados.email) {
                NotificationSystem.error('Nome e email são obrigatórios!');
                return;
            }
            
            if (!dados.email.includes('@')) {
                NotificationSystem.error('Email inválido!');
                return;
            }
            
            Logger.info(`💾 Salvando alterações do prestador ${id}...`);
            
            await APIClient.put(`/prestadores/${id}`, dados);
            
            NotificationSystem.success('Prestador atualizado com sucesso!');
            
            // Fechar modal
            const modal = bootstrap.Modal.getInstance(document.getElementById('editarPrestadorModal'));
            modal.hide();
            
            // Atualizar lista
            await this.refreshPrestadoresList();
            
            Logger.info('✅ Prestador atualizado com sucesso');
            
        } catch (error) {
            Logger.error('❌ Erro ao salvar prestador:', error);
            NotificationSystem.error('Erro ao salvar: ' + error.message);
        }
    }
    
    static async deletarPrestador(id, nome) {
        if (confirm(`Tem certeza que deseja excluir o prestador "${nome}"?`)) {
            try {
                await APIClient.delete(`/prestadores/${id}`);
                NotificationSystem.success('Prestador excluído com sucesso!');
                await this.refreshPrestadoresList();
            } catch (error) {
                Logger.error('❌ Erro ao excluir prestador:', error);
                NotificationSystem.error('Erro ao excluir prestador: ' + error.message);
            }
        }
    }
    
    static async verDetalhesLote(loteId) {
        try {
            Logger.info(`🔍 Buscando detalhes do lote ${loteId}...`);
            const response = await APIClient.get(`/prestadores/historico/${loteId}/os`);
            const osData = response.data;
            
            let html = `
                <div class="modal fade" id="detalhesLoteModal" tabindex="-1">
                    <div class="modal-dialog modal-lg">
                        <div class="modal-content">
                            <div class="modal-header">
                                <h5 class="modal-title">Detalhes do Lote #${loteId}</h5>
                                <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
                            </div>
                            <div class="modal-body">
                                <div class="table-responsive">
                                    <table class="table table-sm">
                                        <thead>
                                            <tr>
                                                <th>O.S.</th>
                                                <th>Modalidade</th>
                                                <th>Data Execução</th>
                                                <th>Valor</th>
                                                <th>Status</th>
                                            </tr>
                                        </thead>
                                        <tbody>
            `;
            
            osData.forEach(os => {
                // Extrair detalhes (pode ser objeto ou string JSON)
                const detalhes = typeof os.detalhes === 'object' ? os.detalhes : JSON.parse(os.detalhes || '{}');
                
                // Extrair valor (suporta múltiplos formatos)
                const valorBase = detalhes.valor_custo_prestador || detalhes.valor || 0;
                const valor = new Intl.NumberFormat('pt-BR', {style: 'currency', currency: 'BRL'}).format(valorBase);
                
                // Formatar data
                let dataExecucao = '-';
                if (detalhes.data_execucao) {
                    try {
                        const date = new Date(detalhes.data_execucao);
                        if (!isNaN(date.getTime())) {
                            dataExecucao = date.toLocaleDateString('pt-BR');
                        } else {
                            dataExecucao = detalhes.data_execucao;
                        }
                    } catch {
                        dataExecucao = detalhes.data_execucao;
                    }
                }
                
                html += `
                    <tr>
                        <td>${os.os_numero || detalhes.o_s || '-'}</td>
                        <td>${detalhes.modalidade || '-'}</td>
                        <td>${dataExecucao}</td>
                        <td>${valor}</td>
                        <td><span class="badge bg-secondary">${detalhes.status || 'Enviado'}</span></td>
                    </tr>
                `;
            });
            
            html += `
                                        </tbody>
                                    </table>
                                </div>
                            </div>
                            <div class="modal-footer">
                                <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Fechar</button>
                            </div>
                        </div>
                    </div>
                </div>
            `;
            
            document.body.insertAdjacentHTML('beforeend', html);
            const modal = new bootstrap.Modal(document.getElementById('detalhesLoteModal'));
            modal.show();
            
            // Remover modal após fechar
            document.getElementById('detalhesLoteModal').addEventListener('hidden.bs.modal', function() {
                this.remove();
            });
            
        } catch (error) {
            Logger.error('❌ Erro ao carregar detalhes do lote:', error);
            NotificationSystem.error('Erro ao carregar detalhes: ' + error.message);
        }
    }
    
    static async downloadAnexo(loteId) {
        try {
            Logger.info(`📥 Baixando anexo do lote ${loteId}...`);
            const response = await fetch(`/api/prestadores/historico/${loteId}/anexo`, {
                headers: {'Authorization': `Bearer ${localStorage.getItem('access_token')}`}
            });
            
            if (!response.ok) throw new Error('Erro ao baixar anexo');
            
            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `lote_${loteId}.pdf`;
            a.click();
            
            NotificationSystem.success('Anexo baixado com sucesso!');
        } catch (error) {
            Logger.error('❌ Erro ao baixar anexo:', error);
            NotificationSystem.error('Erro ao baixar anexo: ' + error.message);
        }
    }
    
    static async excluirLote(loteId) {
        if (confirm('Tem certeza que deseja excluir este lote do histórico?')) {
            try {
                await APIClient.delete(`/prestadores/historico/${loteId}`);
                NotificationSystem.success('Lote excluído com sucesso!');
                await this.loadHistorico();
            } catch (error) {
                Logger.error('❌ Erro ao excluir lote:', error);
                NotificationSystem.error('Erro ao excluir lote: ' + error.message);
            }
        }
    }

    static async salvarTemplate() {
        NotificationSystem.info('Funcionalidade de template em desenvolvimento...');
    }
    
    static async previewTemplate() {
        NotificationSystem.info('Funcionalidade de preview em desenvolvimento...');
    }
}

// Export global functions for use in HTML
window.PageManager = PageManager;
window.NotificationSystem = NotificationSystem;
window.APIClient = APIClient;
window.PrestadoresManager = PrestadoresManager;
window.formatDate = formatDate;
window.formatCurrency = formatCurrency;
window.formatStatus = formatStatus;