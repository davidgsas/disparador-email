# 🎨 PLANEJAMENTO DO NOVO FRONT-END BOOTSTRAP

## 🎯 OBJETIVOS

1. **Manter 100% das funcionalidades atuais**
2. **Interface minimalista e profissional**
3. **Bootstrap 5.3 como base**
4. **Substituir completamente o Streamlit**
5. **Adaptar back-end para servir API REST**

## 🏗️ ARQUITETURA DO NOVO SISTEMA

### Frontend (Bootstrap)
```
frontend/
├── index.html                    # Página principal SPA
├── assets/
│   ├── css/
│   │   ├── bootstrap.min.css     # Bootstrap 5.3
│   │   └── style.css             # Estilos customizados
│   ├── js/
│   │   ├── bootstrap.bundle.min.js
│   │   ├── axios.min.js          # Cliente HTTP
│   │   └── app.js                # Lógica principal
│   └── images/
│       └── logo.png              # Logo da empresa
└── components/                   # Componentes reutilizáveis (HTML templates)
    ├── dashboard.html
    ├── prestadores.html
    ├── montadores.html
    └── modals.html
```

### Backend (FastAPI)
```
├── main.py                       # Servidor FastAPI principal
├── api/
│   ├── __init__.py
│   ├── auth.py                   # Rotas de autenticação
│   ├── prestadores.py            # Rotas de prestadores
│   ├── montadores.py             # Rotas de montadores
│   └── dashboard.py              # Rotas do dashboard
├── models/                       # Modelos Pydantic
│   ├── __init__.py
│   ├── prestador.py
│   ├── montador.py
│   └── common.py
└── utils/                        # Utilitários
    ├── __init__.py
    ├── email_sender.py
    ├── pdf_generator.py
    └── auth_utils.py
```

## 🎨 DESIGN SYSTEM

### Paleta de Cores
```css
:root {
  /* Cores Primárias */
  --primary-color: #003366;      /* Azul Novo Mundo */
  --primary-light: #0066cc;
  --primary-dark: #001122;
  
  /* Cores Secundárias */
  --secondary-color: #6c757d;
  --success-color: #28a745;
  --warning-color: #ffc107;
  --danger-color: #dc3545;
  --info-color: #17a2b8;
  
  /* Neutros */
  --light-bg: #f8f9fa;
  --white: #ffffff;
  --text-primary: #333333;
  --text-secondary: #666666;
  --border-color: #dee2e6;
}
```

### Tipografia
- **Font Family:** 'Inter', 'Segoe UI', sans-serif
- **Font Sizes:** Sistema modular 1.125 (18px base)
- **Font Weights:** 400 (regular), 500 (medium), 600 (semibold), 700 (bold)

### Componentes Principais
1. **Sidebar Navigation** - Menu lateral fixo
2. **Top Bar** - Barra superior com usuário logado
3. **Cards** - Containers para conteúdo
4. **Tables** - Tabelas responsivas
5. **Forms** - Formulários com validação
6. **Modals** - Janelas de diálogo
7. **Alerts** - Notificações e mensagens

## 📱 ESTRUTURA DE PÁGINAS

### 1. Tela de Login
```html
<div class="login-container">
  <div class="login-card">
    <img src="logo.png" alt="Novo Mundo" class="login-logo">
    <h2>Disparador de Email</h2>
    <button class="btn btn-primary btn-lg">
      <i class="fas fa-microsoft"></i>
      Entrar com Office 365
    </button>
  </div>
</div>
```

### 2. Layout Principal (Pós-Login)
```html
<div class="main-layout">
  <!-- Sidebar -->
  <nav class="sidebar">
    <div class="sidebar-header">
      <img src="logo.png" alt="Logo">
      <h4>Disparador Email</h4>
    </div>
    <ul class="nav-menu">
      <li><a href="#dashboard">Dashboard</a></li>
      <li><a href="#prestadores">Prestadores</a></li>
      <li><a href="#montadores">Montadores</a></li>
    </ul>
    <div class="sidebar-footer">
      <div class="user-info">
        <span>user@email.com</span>
        <button class="btn-logout">Sair</button>
      </div>
    </div>
  </nav>
  
  <!-- Conteúdo Principal -->
  <main class="content">
    <div class="content-wrapper">
      <!-- Conteúdo dinâmico aqui -->
    </div>
  </main>
</div>
```

### 3. Dashboard de Pendências
```html
<div class="dashboard-page">
  <div class="page-header">
    <h1><i class="fas fa-calendar-check"></i> Dashboard de Pendências</h1>
    <p class="text-muted">Acompanhe os envios pendentes para hoje</p>
  </div>
  
  <div class="row">
    <!-- Card Prestadores -->
    <div class="col-xl-6">
      <div class="card">
        <div class="card-header">
          <h5><i class="fas fa-user-tie"></i> Prestadores Pendentes</h5>
        </div>
        <div class="card-body" id="prestadores-pendentes">
          <!-- Lista dinâmica -->
        </div>
      </div>
    </div>
    
    <!-- Card Montadores -->
    <div class="col-xl-6">
      <div class="card">
        <div class="card-header">
          <h5><i class="fas fa-hard-hat"></i> Montadores Pendentes</h5>
        </div>
        <div class="card-body" id="montadores-pendentes">
          <!-- Lista dinâmica -->
        </div>
      </div>
    </div>
  </div>
</div>
```

### 4. Seção Prestadores
```html
<div class="prestadores-page">
  <!-- Navegação por Tabs -->
  <ul class="nav nav-tabs" role="tablist">
    <li class="nav-item">
      <a class="nav-link active" data-bs-toggle="tab" href="#enviar-boletins">
        <i class="fas fa-paper-plane"></i> Enviar Boletins
      </a>
    </li>
    <li class="nav-item">
      <a class="nav-link" data-bs-toggle="tab" href="#gerenciar-prestadores">
        <i class="fas fa-users-cog"></i> Gerenciar Prestadores
      </a>
    </li>
    <li class="nav-item">
      <a class="nav-link" data-bs-toggle="tab" href="#historico-envios">
        <i class="fas fa-history"></i> Histórico
      </a>
    </li>
    <li class="nav-item">
      <a class="nav-link" data-bs-toggle="tab" href="#editor-pdf">
        <i class="fas fa-file-pdf"></i> Editor PDF
      </a>
    </li>
  </ul>
  
  <div class="tab-content">
    <!-- Conteúdo das abas -->
  </div>
</div>
```

## 🔄 CONVERSÃO DE FUNCIONALIDADES

### Dashboard de Pendências
**Streamlit → Bootstrap**
- `st.subheader()` → `<h5 class="card-title">`
- `st.success()` → `<div class="alert alert-success">`
- `st.columns()` → `<div class="row"><div class="col-...">`
- `st.button()` → `<button class="btn btn-primary">`

### Formulários
**Streamlit → Bootstrap**
- `st.form()` → `<form class="needs-validation">`
- `st.text_input()` → `<input type="text" class="form-control">`
- `st.selectbox()` → `<select class="form-select">`
- `st.number_input()` → `<input type="number" class="form-control">`
- `st.date_input()` → `<input type="date" class="form-control">`
- `st.text_area()` → `<textarea class="form-control">`
- `st.file_uploader()` → `<input type="file" class="form-control">`

### Tabelas e Dados
**Streamlit → Bootstrap**
- `st.dataframe()` → `<table class="table table-striped">`
- `st.data_editor()` → Tabela com inputs inline
- `st.expander()` → `<div class="accordion">`
- `st.tabs()` → `<ul class="nav nav-tabs">`

### Mensagens e Notificações
**Streamlit → Bootstrap**
- `st.success()` → Toast/Alert success
- `st.error()` → Toast/Alert danger  
- `st.warning()` → Toast/Alert warning
- `st.info()` → Toast/Alert info
- `st.spinner()` → Spinner/Loading overlay

## 🛠️ COMPONENTES CUSTOMIZADOS

### 1. Data Table Component
```javascript
class DataTable {
  constructor(containerId, data, columns, options = {}) {
    this.container = document.getElementById(containerId);
    this.data = data;
    this.columns = columns;
    this.options = options;
    this.render();
  }
  
  render() {
    // Renderiza tabela Bootstrap com paginação, filtros, etc.
  }
}
```

### 2. Form Builder Component
```javascript
class FormBuilder {
  constructor(formId, fields, validationRules) {
    this.form = document.getElementById(formId);
    this.fields = fields;
    this.validationRules = validationRules;
    this.init();
  }
  
  init() {
    // Constrói formulário com validação Bootstrap
  }
}
```

### 3. Modal Manager
```javascript
class ModalManager {
  static show(title, content, size = 'modal-lg') {
    // Gerencia modals dinâmicos
  }
  
  static confirm(message, callback) {
    // Modal de confirmação
  }
}
```

### 4. Notification System
```javascript
class NotificationSystem {
  static success(message, duration = 5000) {
    // Toast de sucesso
  }
  
  static error(message, duration = 8000) {
    // Toast de erro
  }
  
  static showSpinner(message = 'Carregando...') {
    // Overlay de loading
  }
}
```

## 📡 API ENDPOINTS (FastAPI)

### Autenticação
```python
POST /api/auth/login          # Iniciar login Office 365
GET  /api/auth/callback       # Callback OAuth
POST /api/auth/refresh        # Refresh token
POST /api/auth/logout         # Logout
GET  /api/auth/me             # Dados do usuário
```

### Dashboard
```python
GET  /api/dashboard/pendencias        # Lista pendências hoje
POST /api/dashboard/ignorar-envio     # Ignorar envio específico
```

### Prestadores
```python
GET    /api/prestadores                    # Listar prestadores
POST   /api/prestadores                    # Criar prestador
PUT    /api/prestadores/{id}               # Atualizar prestador
DELETE /api/prestadores/{id}               # Deletar prestador

POST   /api/prestadores/enviar-boletins    # Enviar boletins
GET    /api/prestadores/historico          # Histórico lotes
POST   /api/prestadores/upload-excel       # Upload Excel

GET    /api/prestadores/blacklist          # Lista blacklist
POST   /api/prestadores/blacklist          # Adicionar à blacklist
DELETE /api/prestadores/blacklist/{id}     # Remover da blacklist
```

### Montadores
```python
GET    /api/montadores                     # Listar montadores
POST   /api/montadores                     # Criar montador
PUT    /api/montadores/{id}                # Atualizar montador
DELETE /api/montadores/{id}                # Deletar montador

POST   /api/montadores/enviar-pagamentos   # Enviar pagamentos
GET    /api/montadores/historico           # Histórico envios
POST   /api/montadores/upload-excel        # Upload Excel

GET    /api/montadores/blacklist           # Lista blacklist
POST   /api/montadores/blacklist           # Adicionar à blacklist
DELETE /api/montadores/blacklist/{id}      # Remover da blacklist
```

### Utilitários
```python
GET  /api/config                    # Configurações atuais
POST /api/config                    # Salvar configurações
GET  /api/templates/pdf/{tipo}      # Template PDF atual
POST /api/templates/pdf/{tipo}      # Salvar template PDF
```

## 🔐 GERENCIAMENTO DE ESTADO

### Client-Side State
```javascript
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
```

### Session Management
```javascript
class SessionManager {
  static saveToken(token) {
    localStorage.setItem('auth_token', token);
  }
  
  static getToken() {
    return localStorage.getItem('auth_token');
  }
  
  static clearSession() {
    localStorage.clear();
    window.location.href = '/login';
  }
}
```

## 📋 CHECKLIST DE MIGRAÇÃO

### ✅ Funcionalidades Críticas
- [ ] Login Office 365 com device flow
- [ ] Dashboard pendências com regras automáticas
- [ ] Formulários manuais completos (prestadores/montadores)
- [ ] Upload e processamento Excel
- [ ] Sistema de blacklist (O.S. e boletins)
- [ ] Configuração de emails múltiplos
- [ ] Templates de email configuráveis
- [ ] Geração de PDF personalizado
- [ ] Histórico completo com filtros
- [ ] Editor inline de detalhes
- [ ] Sistema de status e anexos
- [ ] Validações e verificações de duplicata

### ✅ Componentes de UI
- [ ] Sidebar navigation responsiva
- [ ] Sistema de tabs/navegação
- [ ] Tabelas com paginação e filtros
- [ ] Formulários com validação
- [ ] Modals para ações secundárias
- [ ] Sistema de notificações
- [ ] Loading states e spinners
- [ ] Upload de arquivos com drag & drop

### ✅ Integração Backend
- [ ] Conversão para FastAPI
- [ ] Endpoints REST completos
- [ ] Autenticação JWT
- [ ] Upload de arquivos
- [ ] Geração de PDF server-side
- [ ] Envio de emails via Graph API
- [ ] Configurações persistentes

## 🚀 CRONOGRAMA DE IMPLEMENTAÇÃO

### Fase 1: Estrutura Base (2-3 dias)
1. Configurar FastAPI backend
2. Criar layout Bootstrap básico
3. Implementar autenticação Office 365
4. Sistema de roteamento frontend

### Fase 2: Dashboard e Core (3-4 dias)
1. Dashboard de pendências
2. Sistema de notificações
3. Navegação entre páginas
4. Estado da aplicação

### Fase 3: Prestadores (4-5 dias)
1. Formulários de prestadores
2. Sistema de envio de boletins
3. Histórico e gerenciamento
4. Editor de PDF

### Fase 4: Montadores (4-5 dias)
1. Formulários de montadores
2. Sistema de pagamentos
3. Histórico e gerenciamento
4. Cálculos de comissão

### Fase 5: Polimento e Testes (2-3 dias)
1. Testes de todas as funcionalidades
2. Otimizações de performance
3. Validações finais
4. Deploy e documentação

**Total Estimado: 15-20 dias**

Esta estrutura garante que TODAS as funcionalidades atuais serão mantidas com uma interface muito mais moderna e profissional!
