# 💰 FinFrases API

[![Logo](../assets/images/logo.png)](https://github.com/WillianSilva51/FinFrases)

A **FinFrases API** fornece um banco de dados curado e de alta performance de citações sobre investimentos, educação financeira, poupança e psicologia do dinheiro.

## ✨ Funcionalidades

* **Banco de Dados Curado**: Frases verificadas de grandes nomes do mercado financeiro e literatura.
* **Filtros Avançados**: Busca flexível por autor, categoria (tags), fonte ou status de verificação.
* **Resultados Aleatórios**: Endpoint dedicado para obter inspiração randômica com agregação nativa.
* **Frase do Dia**: Endpoint com performance otimizada utilizando padrão *Cache-Aside*, fornecendo a frase diária em milissegundos sem sobrecarregar o banco.
* **Documentação Automática**: Interface interativa completa via **Scalar / Swagger UI**.

## 🚀 Tecnologias e Infraestrutura

* **Linguagem & Framework**: Python 3.13+ e FastAPI (100% assíncrono).
* **Bancos de Dados**:
  * MongoDB (via Beanie ODM) para armazenamento persistente.
  * Redis para sistema de cache em memória e rate limiting.
* **Gerenciamento**: `uv` para resolução de dependências ultra-rápida e Pydantic para validação rigorosa de dados.
* **Deploy & Segurança**: Orquestração via `docker-compose` operando em modo rootless e proxy reverso automático com Caddy (HTTPS nativo).

---

## ⚙️ Configuração do Ambiente

Antes de iniciar a aplicação, crie um arquivo `.env` na raiz do projeto baseado no `.env-example` fornecido:

```bash
cp .env-example .env
```

## 🛠️ Como Executar (Podman / Docker)

A infraestrutura foi projetada para rodar de forma isolada e segura. Os volumes já estão configurados com o sufixo `:Z` no `compose.yml` para garantir compatibilidade nativa com as políticas do SELinux.

Construa e suba os contêineres em segundo plano:

```bash
docker-compose up -d
```

O servidor web (Caddy) interceptará o tráfego e repassará para a API internamente.

Acesse a documentação interativa em:

Local: <https://localhost:443/api/docs>

Produção: <https://seu-dominio.com/api/docs>

## 🛠️ Uso (Endpoints)

### Endpoints Públicos

| Método | Endpoint | Descrição |
| --- | --- | --- |
| `GET` | `/api/v1/quotes` | Lista frases com filtros e paginação |
| `GET` | `/api/v1/quotes/{id}` | Retorna uma frase específica pelo ID |
| `GET` | `/api/v1/quotes/random` | Retorna frases aleatórias |
| `GET` | `/api/v1/quotes/today` | Retorna a frase do dia |
| `GET` | `/api/v1/health` | Verifica o status da API |

### Endpoints Administrativos (Requerem API Key)

| Método | Endpoint | Descrição |
| --- | --- | --- |
| `POST` | `/api/v1/quotes` | Cria uma nova frase |
| `PUT` | `/api/v1/quotes/{id}` | Atualiza uma frase existente |
| `DELETE` | `/api/v1/quotes/{id}` | Deleta uma frase existente |

### Listar frases (Com suporte a filtros e paginação)

Retorna uma lista de frases. Você pode filtrar via *Query Parameters*.
`GET /api/v1/quotes?limit=10&skip=0`

**Filtros disponíveis:** `author`, `tags`, `source`, `verified`.
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
openssl rand -base64 64
```

> [!IMPORTANT]
> A saída terá aproximadamente 88 caracteres, pois está codificada em Base64.

3. Coloque a chave gerada no campo `API_KEY` do arquivo `.env` e reinicie os containers para aplicar a nova chave.
