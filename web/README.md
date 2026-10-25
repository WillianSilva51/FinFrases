# 💡 FinFrases - Frontend

O **FinFrases** é uma aplicação web moderna, modular e responsiva voltada para a exibição, busca e gerenciamento de frases motivacionais e educacionais sobre finanças, investimentos, empreendedorismo e mindset. O projeto consome a API REST do **FinFrases**, oferecendo suporte a cache local, filtros avançados, tema claro/escuro e área de autenticação administrativa.

---

## 🚀 Funcionalidades

- 📅 **Frase do Dia**: Exibe a frase diária com cache automático via `localStorage` e expiração calculada até a meia-noite (UTC).
- 🎲 **Frases Aleatórias**: Permite ao usuário gerar frases aleatórias sob demanda de forma rápida.
- 🔍 **Pesquisa Avançada com Filtros**:
  - Busca por palavra-chave, autor ou conteúdo da frase.
  - Filtro por categoria/tag específica.
  - Filtro por status de verificação (frases verificadas/não verificadas).
  - Ordenação por conteúdo, autor, tags, data de criação ou atualização (ordem ascendente ou descendente).
- 📄 **Paginação Dinâmica**: Navegação paginada para os resultados da pesquisa.
- 🏷️ **Categorização Visual por Tags**: Tags estilizadas com cores distintas de acordo com a categoria (*investimentos*, *poupança*, *dividendos*, *FIIs*, *psicologia*, *educação*, *empreendedorismo*, *ação*, *geral*).
- 🔐 **Autenticação Administrativa**: Tela de login com validação da chave secreta (`X-API-KEY`) diretamente no servidor e persistência segura em `sessionStorage`.
- 👁️ **Alternância de Visibilidade de Senha**: Botão integrado ao campo de texto para exibir/ocultar a chave secreta.
- 🌓 **Suporte a Tema Escuro/Claro**: Alternância de tema integrada ao `localStorage` e detecção automática da preferência do sistema (`prefers-color-scheme`).
- 📱 **Design Responsivo & Menu Mobile**: Menu hamburguer e layout otimizado para dispositivos móveis, tablets e desktops.
- 🚫 **Página de Erro 404**: Tela estilizada para tratamento de navegação em rotas inválidas.

---

## 🛠️ Tecnologias Utilizadas

- **HTML5**: Estruturação semântica da página com atributos acessíveis (`aria-*`, `data-page`).
- **Tailwind CSS (v4)**: Estilização utilitária de última geração, com suporte nativo a variantes de temas e otimização.
- **JavaScript ES Modules (ESM)**: Arquitetura modularizada baseada em camadas (API Services, Domain Models, Page Controllers, Componentes de UI e Utilitários).
- **Google Fonts & Icons**: Fonte *Inter* e ícones *Material Symbols Outlined*.

---

## 📁 Estrutura do Projeto

```text
/
├── 404.html                   # Página de erro para rotas não encontradas
├── index.html                 # Página principal (Frase do Dia / Frase Aleatória)
├── search.html                # Página de pesquisa de frases e filtros
├── login.html                 # Página de login para a área administrativa
├── css/
│   ├── input.css              # Arquivo de entrada do Tailwind CSS (v4)
│   └── output.css             # CSS compilado final
└── js/
    ├── main.js                # Entry Point global (Router de páginas e scripts globais)
    ├── api/
    │   ├── client.js          # Cliente HTTP baixo nível, manipulação de fetch e cache
    │   ├── quoteService.js    # Serviço da entidade Quote e mapeamento JSON
    │   └── authService.js     # Validação de chave secreta com o servidor
    ├── components/
    │   ├── theme.js           # Gerenciamento do tema escuro/claro
    │   ├── hamburger.js       # Controle do menu responsivo (mobile)
    │   ├── quoteCard.js       # Componente de renderização dos cards de frases
    │   ├── filters.js         # Controle de exibição/ocultação do painel de filtros
    │   ├── tagsElements.js    # Gerador de tags/badges estilizadas por categoria
    │   ├── visibilityKey.js   # Alternador de visibilidade do campo de senha
    │   └── paginationContainer.js # Gerador de navegação de paginação
    ├── pages/
    │   ├── mainPage.js        # Controller da página principal (index.html)
    │   ├── searchPage.js      # Controller da página de busca (search.html)
    │   └── loginPage.js       # Controller da página de login (login.html)
    ├── config/
    │   └── constants.js       # Configuração de URLs de ambiente (Local vs Produção)
    └── utils/
        ├── sanitizer.js       # Sanitizador contra ataques XSS (escapeHtml)
        └── midnight.js        # Calculadora de timestamp para expiração do cache à meia-noite UTC
```

---

## ✅ Checklist de Desenvolvimento

- [x] Desenvolver página principal com alternância entre Frase do Dia e Frase Aleatória.
- [x] Criar sistema de cache para a Frase do Dia até a meia-noite (UTC).
- [x] Desenvolver página de pesquisa de frases com filtros por tags, texto, ordenação e status de verificação.
- [x] Implementar paginação para a exibição dos resultados de busca.
- [x] Implementar arquitetura de navegação modular por página via `data-page` com *lazy loading* de módulos.
- [x] Implementar sistema de login e validação da chave secreta via API (`X-API-KEY`).
- [ ] Desenvolver o painel administrativo (`admin.html`).
- [ ] Implementar operações de criação, edição e exclusão de frases (CRUD) no painel de administração.

---

## 🔧 Configuração e Execução

### 1. Pré-requisitos

Para executar a aplicação em modo de desenvolvimento, você só precisa de um navegador moderno e de um servidor estático simples (como a extensão **Live Server** no VS Code ou o comando `python -m http.server`).

Caso vá modificar estilos usando o Tailwind CSS v4, certifique-se de ter o **Node.js** instalado.

### 2. Rodando o Projeto

#### Opção A: Servidor HTTP Simples

1. Clone o repositório:

   ```bash
   git clone https://github.com/WillianSilva51/FinFrases.git
   ```

2. Abra a pasta do projeto em seu servidor estático local.
3. Acesse `http://localhost:5500/index.html` (ou a porta utilizada pelo seu servidor).

#### Opção B: Compilando o Tailwind CSS v4

Para atualizar o arquivo `css/output.css` após alterações em classes utilitárias ou no `css/input.css`:

```bash
npx @tailwindcss/cli -i ./css/input.css -o ./css/output.css --watch
```

---

## 🌐 Integração com a API

A aplicação se conecta dinamicamente ao ambiente correto com base no host de execução:

- **Ambiente Local**: `/api/v1/quotes/` (redirecionado automaticamente quando rodado em `localhost`, `127.0.0.1` ou `[::1]`).
- **Ambiente de Produção**: `https://api.finfrases.developer.li/v1/quotes/`

### Principais Endpoints Consumidos

| Método | Endpoint | Descrição |
| :--- | :--- | :--- |
| `GET` | `/v1/quotes/today` | Retorna a frase do dia. |
| `GET` | `/v1/quotes/random` | Retorna uma frase aleatória. |
| `GET` | `/v1/quotes/?search=...` | Busca frases com filtros (busca, tags, verificação, paginação e ordenação). |
| `POST` | `/v1/quotes/` | Validação de chave de autenticação (envio de cabeçalho `X-API-KEY`). |

---

## 📄 Licença

Todos os direitos reservados © **FinFrases 2026**.
