# 💰 FinFrases API

Uma API aberta e gratuita para frases de mentalidade financeira, investimentos e educação financeira, totalmente em português (PT-BR).

Este projeto foi criado para preencher a lacuna de APIs brasileiras voltadas ao nicho de finanças, oferecendo conteúdo curado de grandes nomes como Luiz Barsi, Warren Buffett, Nathalia Arcuri e outros.

## ✨ Funcionalidades

* **Banco de Dados Curado**: Frases verificadas sobre investimentos, psicologia financeira e poupança.
* **Filtros Avançados**: Busca por autor ou categorias (tags).
* **Resultados Aleatórios**: Endpoint dedicado para obter inspiração randômica.
* **Paginação Nativa**: Respostas otimizadas para performance em apps e bots.
* **Documentação Moderna**: Interface interativa via **Scalar**.

## 🚀 Tecnologias

* **Java 25** e **Spring Boot 4.0.2**.
* **MongoDB**: Armazenamento flexível de documentos.
* **Caffeine Cache**: Performance ultraveloz para requisições frequentes.
* **MapStruct & Lombok**: Código limpo e eficiente.
* **Docker & Podman**: Ambiente isolado e reprodutível.

## 🛠️ Uso (Endpoints)

A documentação completa e interativa pode ser acessada localmente em: `http://localhost:8080/docs`.

### Listar frases (Paginado)

Retorna uma lista de frases verificadas.
`GET /v1/quotes`

### Frases Aleatórias

Retorna uma ou mais frases aleatórias.
`GET /v1/quotes/random?size=1`

**Exemplo de Resposta:**

```json
[
  {
    "id": "65d4f8a9e4b0a1b2c3d4e5f6",
    "content": "O preço é o que você paga; o valor é o que você leva.",
    "author": "Warren Buffett",
    "tags": ["INVESTIMENTOS"],
    "source": "Carta aos Acionistas, 2008"
  }
]

```

### Buscar por Autor

`GET /v1/quotes/author/{author}`

### Buscar por Categoria

`GET /v1/quotes/category/{category}`

**Categorias disponíveis:** `INVESTIMENTOS`, `POUPANCA`, `PSICOLOGIA`, `DIVIDENDOS`, `EDUCACAO`, `EMPREENDEDORISMO`, `ACAO`, `FIIS`.

## 💻 Instalação e Desenvolvimento

Como o projeto utiliza Docker, você pode subir o ambiente completo (API + MongoDB) rapidamente.

1. **Clone o repositório:**
```bash
git clone https://github.com/williiansilva51/finfrases.git
cd finfrases

```


2. **Suba os containers:**
```bash
podman-compose up -d
# ou
docker-compose up -d

```


3. **Acesse a API:**
A aplicação estará disponível em `http://localhost:8080`.

## 🔐 Administração

Para criar novas frases, é necessário enviar um `POST` para `/v1/quotes` com a chave de administrador configurada no ambiente.

```json
{
  "content": "O risco vem de não saber o que você está fazendo.",
  "author": "Warren Buffett",
  "tags": ["INVESTIMENTOS"],
  "source": "Livro: O Investidor Inteligente"
}

```

## 📄 Licença

Este projeto está sob a licença **MIT**.

---

Desenvolvido por [Willian Silva](https://www.google.com/search?q=https://github.com/williiansilva51).
