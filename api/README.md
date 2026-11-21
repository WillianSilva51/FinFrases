# 💰 FinFrases API

[![Logo](../assets/images/logo.png)](https://github.com/WillianSilva51/FinFrases)

A **FinFrases API** fornece um banco de dados curado e de alta performance de citações sobre investimentos, educação financeira, poupança e psicologia do dinheiro.

## 📑 Sumário

- [✨ Funcionalidades](#-funcionalidades)
- [🚀 Tecnologias e Infraestrutura](#-tecnologias-e-infraestrutura)
- [⚙️ Configuração do Ambiente](#️-configuração-do-ambiente)
- [🔧 Como Executar (Podman / Docker)](#-como-executar-podman--docker)
- [🕒 Uso (Endpoints)](#-uso-endpoints)
  - [Endpoints Públicos](#endpoints-públicos)
  - [Endpoints Administrativos](#endpoints-administrativos-requerem-api-key)
  - [Listar frases](#listar-frases-com-suporte-a-filtros-e-paginação)
  - [Frases Aleatórias](#frases-aleatórias)
  - [Frase do Dia](#frase-do-dia-com-cache)
- [📨 Newsletter da Frase Diária](#-newsletter-da-frase-diária)
- [🔐 Administração](#-administração)
  - [Como criar uma API Key](#como-criar-uma-api-key)

---

## ✨ Funcionalidades

- **Banco de Dados Curado**: Frases verificadas de grandes nomes do mercado financeiro e literatura.
- **Filtros Avançados**: Busca flexível por autor, categoria (tags), fonte ou status de verificação.
- **Resultados Aleatórios**: Endpoint dedicado para obter inspiração randômica com agregação nativa.
- **Frase do Dia**: Endpoint com performance otimizada utilizando padrão *Cache-Aside*, fornecendo a frase diária em milissegundos sem sobrecarregar o banco.
- **Documentação Automática**: Interface interativa completa via **Scalar / Swagger UI**.
- **Segurança e Autenticação**: Endpoints administrativos protegidos por chave secreta (`X-API-KEY`) e validação rigorosa de dados via **Pydantic**.
- **Newsletter e Assinaturas**: Sistema de inscrição e desinscrição de usuários para receber frases diárias por e-mail, com validação de token e feedback visual.

## 🚀 Tecnologias e Infraestrutura

- **Linguagem & Framework**: Python 3.13+ e FastAPI (100% assíncrono).
- **Bancos de Dados**:
  - MongoDB (via Beanie ODM) para armazenamento persistente.
  - Redis para sistema de cache em memória e rate limiting.
- **Mensageria**: RabbitMQ para filas de mensagens assíncronas.
- **Gerenciamento**: `uv` para resolução de dependências ultra-rápida e Pydantic para validação rigorosa de dados.
- **Deploy & Segurança**: Orquestração via `docker-compose` operando em modo rootless e proxy reverso automático com Caddy (HTTPS nativo).

---

## ⚙️ Configuração do Ambiente

Antes de iniciar a aplicação, crie um arquivo `.env` na raiz do projeto baseado no `.env-example` fornecido:

```bash
cp .env.example .env
```

## 🔧 Como Executar (Podman / Docker)

A infraestrutura foi projetada para rodar de forma isolada e segura. Os volumes já estão configurados com o sufixo `:Z` no `compose.yml` para garantir compatibilidade nativa com as políticas do SELinux.

Construa e suba os contêineres em segundo plano:

```bash
docker-compose up -d
```

O servidor web (Caddy) interceptará o tráfego e repassará para a API internamente.

Acesse a documentação interativa em:

Local: <https://localhost:443/api/docs>

Produção: <https://seu-dominio.com/api/docs>

## 🕒 Uso (Endpoints)

### Endpoints Públicos

| Método | Endpoint | Descrição |
| --- | --- | --- |
| `GET` | `/api/v1/quotes` | Lista frases com filtros e paginação |
| `GET` | `/api/v1/quotes/{id}` | Retorna uma frase específica pelo ID |
| `GET` | `/api/v1/quotes/random` | Retorna frases aleatórias |
| `GET` | `/api/v1/quotes/today` | Retorna a frase do dia |
| `GET` | `/api/v1/health` | Verifica o status da API |
| `POST` | `/api/v1/subscribers` | Inscreve um novo assinante para a frase do dia |
| `POST` | `/api/v1/subscribers/unsubscribe` | Desinscreve um assinante usando o token de validação |

### Endpoints Administrativos (Requerem API Key)

| Método | Endpoint | Descrição |
| --- | --- | --- |
| `POST` | `/api/v1/quotes` | Cria uma nova frase |
| `PUT` | `/api/v1/quotes/{id}` | Atualiza uma frase existente |
| `DELETE` | `/api/v1/quotes/{id}` | Deleta uma frase existente |

### Listar frases (Com suporte a filtros e paginação)

Retorna uma lista de frases. Você pode filtrar via *Query Parameters*.
`GET /api/v1/quotes?limit=10&skip=0`

**Filtros disponíveis:**

| Parâmetro | Tipo | Descrição |
| --- | --- | --- |
| `author` | string | Filtra por autor exato |
| `tags` | string | Filtra por uma ou mais tags (case-insensitive) |
| `exclude_tags` | string | Exclui frases com as tags especificadas |
| `source` | string | Filtra por fonte exata |
| `verified` | boolean | Filtra por frases verificadas (true) ou não verificadas (false) |
| `sort_by` | string | Ordena os resultados por um campo específico (case-insensitive) |
| `order` | string | Define a ordem de classificação: 'asc' para ascendente e 'desc' para descendente |
| `search` | string | Realiza uma busca textual nos campos de conteúdo, autor e fonte. |

*Exemplo: `GET /api/v1/quotes?tags=INVESTIMENTOS&author=Warren Buffett`*

### Frases Aleatórias

Retorna uma ou mais frases aleatórias utilizando agregação nativa do MongoDB.
`GET /api/v1/quotes/random?size=1`

### Frase do Dia (Com Cache)

Retorna a frase oficial do dia. O resultado é cacheado no Redis e atualizado automaticamente à meia-noite.
`GET /api/v1/quotes/today`

**Exemplo de Resposta:**

```json
[
  {
    "_id": "65d4f8a9e4b0a1b2c3d4e5f6",
    "content": "O preço é o que você paga; o valor é o que você leva.",
    "author": "Warren Buffett",
    "tags": ["INVESTIMENTOS"],
    "source": "Carta aos Acionistas, 2008",
    "verified": true,
    "created_at": "2026-03-27T10:00:00Z"
  }
]
```

**Categorias (Tags) disponíveis:** `GERAL`, `INVESTIMENTOS`, `POUPANCA`, `PSICOLOGIA`, `DIVIDENDOS`, `EDUCACAO`, `EMPREENDEDORISMO`, `ACAO`, `FIIS`.

## 📨 Newsletter da Frase Diária

A newsletter da frase do dia permite que os usuários se inscrevam para receber a frase oficial do dia diretamente no e-mail. A inscrição é feita através do endpoint `/api/v1/subscribers` e a desinscrição via `/api/v1/subscribers/unsubscribe` com validação de token.

Com o sistema de mensageria RabbitMQ, o envio de e-mails é processado de forma assíncrona, garantindo que a API permaneça responsiva mesmo durante picos de envio.

## 🔐 Administração

Para criar novas frases, é necessário enviar um `POST` para `/api/v1/quotes` contendo o payload validado pelo Pydantic.

```json
{
  "_id": "65d4f8a9e4b0a1b2c3d4e5f6",
  "content": "O risco vem de não saber o que você está fazendo.",
  "author": "Warren Buffett",
  "tags": ["INVESTIMENTOS"],
  "source": "Livro: O Investidor Inteligente",
  "verified": true
}
```

Para atualizar ou deletar frases, utilize os endpoints `PUT /api/v1/quotes/{id}` e `DELETE /api/v1/quotes/{id}`.

### Como criar uma API Key

1. Instale em sua máquina o OpenSSL (<https://www.openssl.org/>).
2. Execute o comando abaixo para gerar uma chave aleatória segura com 64 bytes (512 bits) de entropia e imprimi-la no terminal:

```bash
openssl rand -hex 64
```

> [!IMPORTANT]
> A saída terá aproximadamente 128 caracteres, pois está codificada em Hexadecimal.

3. Coloque a chave gerada no campo `API_KEY` do arquivo `.env` e reinicie os containers para aplicar a nova chave.
