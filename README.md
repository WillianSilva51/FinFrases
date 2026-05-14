# 💰 FinFrases

[![Python](https://img.shields.io/badge/Python-3.13-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-Enabled-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![MongoDB](https://img.shields.io/badge/MongoDB-Database-47A248?style=for-the-badge&logo=mongodb&logoColor=white)](https://www.mongodb.com/)
![Redis](https://img.shields.io/badge/Redis-Cache-DC382D?style=for-the-badge&logo=redis&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Enabled-2496ED?style=for-the-badge&logo=docker&logoColor=white)
[![License](https://img.shields.io/github/license/WillianSilva51/FinFrases?color=blue&style=for-the-badge)](https://github.com/WillianSilva51/FinFrases/blob/main/LICENSE)

Uma API aberta e gratuita para frases de mentalidade financeira, investimentos e educação financeira, totalmente em português (PT-BR).

Este projeto foi criado para preencher a lacuna de APIs brasileiras voltadas ao nicho de finanças, oferecendo conteúdo curado de grandes nomes como Luiz Barsi, Warren Buffett, Nathalia Arcuri e outros.

*Inicialmente construído em Java/Spring Boot, o projeto foi refatorado para Python/FastAPI visando máxima agilidade, performance assíncrona e integração facilitada com ecossistemas de dados.*

## 💻 Instalação e Desenvolvimento

Como o projeto utiliza Docker, você pode subir o ambiente completo (Frontend, API, MongoDB e Redis) rapidamente.

1. **Clone o repositório:**

<!-- end list -->

```bash
git clone https://github.com/williiansilva51/finfrases.git
```

1. **Configure as variáveis de ambiente:**
    Faça uma cópia do arquivo `.env-example` para `.env` e preencha com as credenciais (as senhas padrão já funcionam localmente).

2. **Suba os containers:**

<!-- end list -->

```bash
podman-compose up -d
# ou
docker-compose up -d
```

3. **Acessar a aplicação:**
    - A aplicação estará disponível na porta `8000`. Acesse `http://localhost:8000/api/docs` para testar os endpoints.

    - O frontend estará disponível em `http://localhost:8080`.

## 📄 Licença

Este projeto está sob a licença [**MIT**](./LICENSE).

-----

Desenvolvido por [Willian Silva](https://github.com/WillianSilva51)
