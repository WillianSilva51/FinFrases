# 💡 FinFrases - Frontend

O **FinFrases** é uma aplicação web moderna e responsiva voltada para a exibição de frases motivacionais e educacionais sobre finanças, investimentos, empreendedorismo e mindset. O projeto consome a API do **FinFrases** e exibe frases diárias e aleatórias com suporte a temas claro/escuro e sistema de cache local.

---

## 🚀 Funcionalidades

- 📅 **Frase do Dia**: Exibe uma frase diária com cache automático via `localStorage` até a meia-noite (UTC).
- 🎲 **Frases Aleatórias**: Permite ao usuário gerar frases aleatórias sob demanda.
- 🏷️ **Categorização por Tags**: Renderização dinâmica de tags coloridas de acordo com o tópico da frase (*investimentos*, *poupança*, *dividendos*, *FIIs*, etc.).
- 🌓 **Suporte a Tema Escuro/Claro**: Alternância de tema integrada ao `localStorage` e detecção da preferência do sistema (`prefers-color-scheme`).
- 📱 **Design Responsivo**: Menu hamburguer e layout otimizado para dispositivos móveis e desktops.
- 🚫 **Página de Erro 404**: Tela estilizada para navegação de rotas inválidas.

---

## 🛠️ Tecnologias Utilizadas

- **HTML5**: Estruturação semântica da página.
- **Tailwind CSS (v4)**: Estilização utilitária moderna e responsiva.
- **JavaScript (ES Modules)**: Lógica do cliente modularizada e assíncrona.
- **Google Fonts**: Fonte *Inter* e ícones *Material Symbols Outlined*.

---

## ✅ Checklist de Funcionalidades Futuras

- [ ] Desenvolver página de pesquisa de frases com filtros por tags e palavras-chave e outros tipos de filtros.
- [ ] Implementar sistema de login e autenticação do admin.
- [ ] Adicionar funcionalidades de gerenciamento das frases via painel administrativo.

## 📁 Estrutura do Projeto

```text
/
├── 404.html           # Página de erro para rotas não encontradas
├── index.html         # Página principal (Frase do Dia / Frase Aleatória)
├── search.html        # Página de busca de frases
├── css/
│   ├── input.css      # Arquivo de entrada do Tailwind CSS
│   └── output.css     # CSS compilado final
└── js/
    ├── mainPage.js    # Entry point para a página principal
    ├── searchPage.js  # Entry point para a página de busca
    ├── quote.js       # Requisições à API, regras de negócio e manipulação do DOM de frases
    ├── theme.js       # Gerenciamento de tema claro/escuro
    ├── hamburger.js   # Controle do menu responsivo (mobile)
    └── utils.js       # Funções utilitárias (cálculo de expiração de cache)
```

---

## 🔧 Configuração e Execução

### 1. Pré-requisitos

Para abrir a aplicação, você só precisa de um navegador moderno ou de uma extensão de servidor local (como a **Live Server** no VS Code).

Caso deseje alterar estilos no Tailwind CSS, será necessário ter o **Node.js** instalado para rodar a CLI do Tailwind.

### 2. Rodando o Projeto

#### Opção A: Servidor HTTP Simples (Sem Node.js)

1. Clone ou baixe o repositório.
2. Abra a pasta do projeto em um servidor local (ex: via *Live Server* ou extensão equivalente).
3. Acesse `http://localhost:5500/index.html` no navegador.

#### Opção B: Compilando o Tailwind CSS (Desenvolvimento)

Se você for modificar classes no HTML ou no `css/input.css`, rode a CLI do Tailwind v4 para atualizar o `css/output.css`:

```bash
npx @tailwindcss/cli -i ./css/input.css -o ./css/output.css --watch
```

---

## 🌐 Integração com a API

A aplicação consome a API REST do **FinFrases**:

- **Ambiente de Produção**: `https://api.finfrases.developer.li/v1/quotes/`
- **Ambiente Local**: `/api/v1/quotes/` (redirecionado automaticamente quando rodado em `localhost` ou `127.0.0.1`).

### Endpoints Utilizados

- `GET /v1/quotes/today` — Busca a frase do dia.
- `GET /v1/quotes/random` — Busca uma frase aleatória.

---

## 📄 Licença

Direitos reservados © **FinFrases 2026**.
