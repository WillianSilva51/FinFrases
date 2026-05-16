# Política de Segurança

## Versões Suportadas

Atualmente, apenas a versão mais recente da API recebe atualizações de segurança e correções de bugs.

| Versão | Suportada |
| :--- | :--- |
| 1.0.0 | ✅ Sim |
| < 1.0.0 | ❌ Não |

## Reportar uma Vulnerabilidade

Se descobrir uma vulnerabilidade de segurança neste projeto, por favor siga estes passos:

1. **Não abra um "Issue" público:** Reportar publicamente pode expor os utilizadores a riscos antes de uma correção estar disponível.
2. **Contacto Direto:** Envie os detalhes da vulnerabilidade por e-mail para **[antonio.oliveira051@gmail.com](mailto:antonio.oliveira051@gmail.com)**.
3. **Detalhes Necessários:** Por favor, inclua uma descrição clara, passos para reproduzir o problema e, se possível, sugestões de correção.
4. **Prazo:** O mantenedor tentará responder num prazo razoável para confirmar a receção e discutir os próximos passos.

## Medidas de Segurança Implementadas

### 1. Autenticação via Chave de API

A API utiliza um cabeçalho personalizado `X-API-Key` para autenticar operações administrativas (como a criação de novas frases).

* A verificação utiliza `secrets.compare_digest` para prevenir ataques de tempo (timing attacks).
* É fortemente recomendado gerar chaves seguras com alta entropia utilizando comandos como `openssl rand -base64 64`.

### 2. Gestão de Variáveis de Ambiente

* As credenciais sensíveis, como `MONGO_URI` e `API_KEY`, são carregadas através de um ficheiro `.env` e nunca devem ser incluídas diretamente no código-fonte.
* O ficheiro `.env-example` é fornecido apenas como referência de estrutura.

### 3. Segurança em Contentores (Docker)

* O `Dockerfile` utiliza uma estratégia de construção em múltiplas etapas (*multi-stage build*) para reduzir o tamanho da imagem final e a superfície de ataque.
* A aplicação é executada sob um utilizador não-privilegiado (`appuser`), evitando permissões de root dentro do contentor.

### 4. Middleware de Segurança

* A API utiliza `CORSMiddleware` para gerir acessos de origens cruzadas. Em ambientes de produção, recomenda-se restringir `allow_origins=["*"]` apenas aos domínios necessários.

## Boas Práticas para Implementação

* **Proteja a sua API Key:** Nunca partilhe a sua chave de produção ou a inclua em repositórios públicos.
* **HTTPS:** Utilize sempre um proxy reverso (como Nginx ou Traefik) com certificados SSL/TLS para garantir que as chaves de API não são transmitidas em texto simples pela rede.
* **Base de Dados:** Certifique-se de que a instância do MongoDB possui autenticação ativa e está isolada da rede pública.
