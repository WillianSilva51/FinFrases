# 💰 FinFrases

[![Python](https://img.shields.io/badge/Python-3.13-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-Enabled-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![MongoDB](https://img.shields.io/badge/MongoDB-Database-47A248?style=for-the-badge&logo=mongodb&logoColor=white)](https://www.mongodb.com/)
![Redis](https://img.shields.io/badge/Redis-Cache-DC382D?style=for-the-badge&logo=redis&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Enabled-2496ED?style=for-the-badge&logo=docker&logoColor=white)
[![License](https://img.shields.io/github/license/WillianSilva51/FinFrases?color=blue&style=for-the-badge)](https://github.com/WillianSilva51/FinFrases/blob/main/LICENSE)

[![Logo](./assets/images/logo.png)](https://github.com/WillianSilva51/FinFrases)

Uma plataforma aberta e gratuita de frases de mentalidade financeira, investimentos e educação, totalmente em português (PT-BR).

Este projeto foi criado para preencher a lacuna de ecossistemas brasileiros voltados ao nicho de finanças, oferecendo conteúdo curado de grandes nomes como Luiz Barsi, Warren Buffett, Nathalia Arcuri e outros.

*Inicialmente construído em Java/Spring Boot, o sistema foi totalmente refatorado para Python visando uma arquitetura assíncrona, maior agilidade no desenvolvimento e integração facilitada com pipelines de dados.*

---

## 🗂️ Estrutura do Repositório

Este é um *monorepo* que reúne os serviços necessários para executar o FinFrases.

Cada módulo possui sua própria documentação técnica:

- ⚙️ [**`/api`**](./api/README.md): Backend assíncrono desenvolvido em FastAPI, responsável pelas regras de negócio, paginação, integração com MongoDB e cache distribuído com Redis.
- 🖥️ [**`/frontend`**](./frontend/README.md): Interface de usuário para visualização, busca e interação com as frases curadas.

> Consulte o README de cada módulo para obter informações sobre configuração, desenvolvimento, estrutura interna e detalhes técnicos específicos.

---

## 🏗️ Arquitetura do Sistema

```mermaid
---
title: Arquitetura da Aplicação FinFrases
config:
  architecture:
    randomize: true
---
architecture-beta
    group internet(internet)[Internet]
        service user(internet)[User] in internet
    
    group frontend(cloud)[Frontend]
        service client(cloud)[Client] in frontend

    group backend(cloud)[Backend]
        service proxy(server)[Caddy Reverse Proxy] in backend
        service api(server)[API] in backend
    
    group data(server)[Data]
        service mongodb(database)[MongoDB] in data
        service redis(database)[Redis] in data


    user:T --> L:client
    user:R --> L:proxy

    client:B --> T:proxy

    proxy:R --> L:api

    api:B --> T:mongodb
    api:R --> L:redis
```

---

## 🚀 Quick Start (Instalação via Docker)

A forma mais rápida de rodar o projeto localmente é utilizando o Docker Compose, que orquestra e sobe automaticamente a API, o Frontend, o banco de dados (MongoDB) e o cache (Redis).

**1. Clone o repositório:**

```bash
git clone https://github.com/williiansilva51/finfrases.git
cd finfrases
```

**2. Variáveis de Ambiente:**
Faça uma cópia do arquivo de configuração na pasta da API e preencha com as credenciais necessárias (para desenvolvimento local, os valores padrão são suficientes).

```bash
cp api/.env-example api/.env

```

**3. Suba os containers:**

```bash
podman-compose up -d --build
# ou (dependendo do seu ecossistema)
docker compose up -d --build

```

**4. Acesse a aplicação:**
Com os containers rodando, os serviços estarão disponíveis em:

- 🌐 **Frontend Web:** `https://localhost:443`
- 📚 **Documentação da API (Scalar):** `https://localhost:443/api/docs`

---

## 🤝 Como Contribuir

Sugestões de novas frases, correções ortográficas e melhorias no código são muito bem-vindas!

1. Faça um *Fork* do projeto.
2. Crie uma *Branch* para sua modificação (`git checkout -b feature/NovaFuncionalidade`).
3. Faça o *Commit* das suas alterações (`git commit -m 'Add: nova funcionalidade'`).
4. Faça o *Push* para a branch (`git push origin feature/NovaFuncionalidade`).
5. Abra um *Pull Request*.

## 📄 Licença

Este projeto é de código aberto e está sob a licença **[MIT](./LICENSE)**.

---

Desenvolvido por [Willian Silva](https://github.com/WillianSilva51)
