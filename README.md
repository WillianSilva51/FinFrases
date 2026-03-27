# 💰 FinFrases API

Uma API aberta e gratuita para frases de mentalidade financeira, investimentos e educação financeira, totalmente em português (PT-BR).

Este projeto foi criado para preencher a lacuna de APIs brasileiras voltadas ao nicho de finanças, oferecendo conteúdo curado de grandes nomes como Luiz Barsi, Warren Buffett, Nathalia Arcuri e outros.

*Inicialmente construído em Java/Spring Boot, o projeto foi refatorado para Python/FastAPI visando máxima agilidade, performance assíncrona e integração facilitada com ecossistemas de dados.*

## ✨ Funcionalidades

* **Banco de Dados Curado**: Frases verificadas sobre investimentos, psicologia financeira e poupança.
* **Filtros Avançados**: Busca flexível por autor, categoria (tags) ou fonte da frase.
* **Resultados Aleatórios**: Endpoint dedicado para obter inspiração randômica.
* **Frase do Dia (Nova)**: Endpoint com performance otimizada utilizando padrão *Cache-Aside* para fornecer a frase diária sem sobrecarregar o banco.
* **Documentação Automática**: Interface interativa via **Swagger/OpenAPI**.

## 🚀 Tecnologias

* **Python 3.13+** e **FastAPI**: Alta performance, código limpo e requisições 100% assíncronas.
* **MongoDB & Beanie**: Armazenamento de documentos utilizando um ODM assíncrono poderoso.
* **Redis**: Sistema de cache em memória para endpoints de alta demanda.
* **Pydantic**: Tipagem estática rigorosa e validação de dados automática.
* **uv**: Gerenciador de pacotes ultra-rápido para o ecossistema Python.
* **Docker & Podman**: Ambiente isolado e orquestração de containers (API, Mongo e Redis).

## 🛠️ Uso (Endpoints)

A documentação completa e interativa pode ser acessada localmente em: `http://localhost:8000/api/docs` ou `http://localhost:8000/api/redoc` para visualização alternativa.

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
    "id": "65d4f8a9e4b0a1b2c3d4e5f6",
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

## 💻 Instalação e Desenvolvimento

Como o projeto utiliza Docker, você pode subir o ambiente completo (API, MongoDB e Redis) rapidamente.

1. **Clone o repositório:**

<!-- end list -->

```bash
git clone https://github.com/williiansilva51/finfrases.git
cd finfrases/api
```

2. **Configure as variáveis de ambiente:**
    Faça uma cópia do arquivo `.env-example` para `.env` e preencha com as credenciais (as senhas padrão já funcionam localmente).

3.  **Suba os containers:**

<!-- end list -->

```bash
podman-compose up -d
# ou
docker-compose up -d
```

4.  **Acesse a API:**
    A aplicação estará disponível na porta `8000`. Acesse `http://localhost:8000/api/docs` para testar os endpoints.

## 🔐 Administração

Para criar novas frases, é necessário enviar um `POST` para `/api/v1/quotes/` contendo o payload validado pelo Pydantic.

```json
{
  "content": "O risco vem de não saber o que você está fazendo.",
  "author": "Warren Buffett",
  "tags": ["INVESTIMENTOS"],
  "source": "Livro: O Investidor Inteligente",
  "verified": true
}
```

## 📄 Licença

Este projeto está sob a licença **MIT**.

-----

Desenvolvido por [Willian Silva](https://github.com/WillianSilva51)