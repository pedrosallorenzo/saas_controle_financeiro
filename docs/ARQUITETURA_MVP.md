# Documento de Arquitetura — SaaS Controle Financeiro (MVP)

> **Leia este arquivo antes de qualquer coisa.**
> Ele contém todas as decisões técnicas, regras de código, estrutura do projeto e contexto de produto.
> Não tome decisões de arquitetura sem consultar este documento primeiro.

---

## 1. Contexto do Produto

SaaS de controle financeiro pessoal onde o diferencial principal é **registrar e consultar finanças por linguagem natural**. O usuário digita "Gastei 42 no almoço hoje" e o sistema interpreta, confirma e salva automaticamente.

**Hipótese central a validar no MVP:**
> "As pessoas querem registrar e consultar finanças por linguagem natural, sem preencher formulários."

**Público-alvo inicial:** estudantes, estagiários, jovens CLT, freelancers.

**6 telas do MVP (em ordem de prioridade):**
1. Auth (login/cadastro)
2. Onboarding (3 perguntas)
3. Lançamento por linguagem natural + card de confirmação
4. Dashboard (saldo, receitas, despesas, top categorias)
5. Lista de transações (editar/deletar)
6. Pergunte à IA (consultas conversacionais)

**Fora do MVP — não implementar ainda:**
metas, orçamentos, relatórios, WhatsApp, exportação, planos pagos, filtros avançados, comparações históricas, gráficos elaborados, Open Finance.

---

## 2. Stack Tecnológica

### Decisão geral
Python no backend, React no frontend. Separação clara entre API e UI.

### Backend
| Componente | Escolha | Motivo |
|---|---|---|
| Framework | **FastAPI** | Async nativo, tipagem com Pydantic, documentação automática (OpenAPI), performance |
| ORM | **SQLAlchemy 2.x + Alembic** | Maduro, migrations confiáveis, bem suportado pelo Claude Code |
| Banco de dados | **PostgreSQL** (via Supabase) | SQL robusto, Supabase dá hosting gerenciado + auth + storage grátis no início |
| Autenticação | **Supabase Auth** | Pronto, seguro, suporta JWT, email/password, magic link. Não construir do zero. |
| IA (parsing NL) | **API Anthropic (claude-sonnet-4-20250514)** | Já têm conta. Melhor custo-benefício para tarefas de parsing estruturado. |
| Validação | **Pydantic v2** | Já vem com FastAPI, tipagem forte |
| Cache | **Redis** (Upstash — serverless) | Rate limiting de chamadas à API de IA. Simples de integrar. |
| Testes | **pytest + httpx** | Padrão Python, httpx para testar endpoints async |

### Frontend
| Componente | Escolha | Motivo |
|---|---|---|
| Framework | **Next.js 14+ (App Router)** | SSR quando necessário, rotas simples, deploy trivial na Vercel |
| Linguagem | **TypeScript** | Tipagem forte evita bugs bobos, especialmente com dados financeiros |
| Estilo | **Tailwind CSS** | Produtividade alta, sem inventar CSS do zero |
| Componentes | **shadcn/ui** | Componentes acessíveis, customizáveis, não opiniosos demais |
| Estado global | **Zustand** | Simples, leve, sem boilerplate do Redux |
| Fetch / Cache | **TanStack Query (React Query)** | Gerencia loading, error, cache de chamadas à API |
| Formulários | **React Hook Form + Zod** | Validação tipada, sem re-renders desnecessários |

### Infraestrutura
| Componente | Escolha | Motivo |
|---|---|---|
| Hosting backend | **Railway** | Deploy Python/Docker simples, plano grátis generoso para MVP, escala depois |
| Hosting frontend | **Vercel** | Integração nativa com Next.js, deploy automático via GitHub |
| Banco (managed) | **Supabase** (free tier → pro quando precisar) | PostgreSQL gerenciado, backups automáticos |
| Cache (managed) | **Upstash Redis** | Serverless, free tier suficiente para MVP |
| Monitoramento | **Sentry** (free tier) | Captura erros em produção automaticamente |
| Variáveis de ambiente | `.env` local + Railway/Vercel env vars em produção | Nunca commitar secrets |

---

## 3. Estrutura de Pastas

```
saas-financas/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py                  # FastAPI app, CORS, routers
│   │   ├── config.py                # Settings via pydantic-settings
│   │   ├── database.py              # Engine, SessionLocal, Base
│   │   ├── deps.py                  # Dependências injetáveis (get_db, get_current_user)
│   │   ├── models/                  # SQLAlchemy models (tabelas)
│   │   │   ├── __init__.py
│   │   │   ├── user.py
│   │   │   ├── transaction.py
│   │   │   └── category.py
│   │   ├── schemas/                 # Pydantic schemas (request/response)
│   │   │   ├── __init__.py
│   │   │   ├── transaction.py
│   │   │   ├── category.py
│   │   │   └── ai.py
│   │   ├── routers/                 # Endpoints organizados por domínio
│   │   │   ├── __init__.py
│   │   │   ├── auth.py
│   │   │   ├── transactions.py
│   │   │   ├── categories.py
│   │   │   ├── dashboard.py
│   │   │   └── ai.py
│   │   └── services/                # Lógica de negócio (separada dos routers)
│   │       ├── __init__.py
│   │       ├── ai_parser.py         # Integração com API Anthropic
│   │       ├── dashboard.py
│   │       └── rate_limiter.py
│   ├── migrations/                  # Alembic migrations
│   ├── tests/
│   │   ├── conftest.py
│   │   ├── test_ai_parser.py        # Testa as 30 frases do JSON de teste
│   │   ├── test_transactions.py
│   │   └── test_dashboard.py
│   ├── .env.example
│   ├── requirements.txt
│   ├── Dockerfile
│   └── README.md
│
├── frontend/
│   ├── src/
│   │   ├── app/                     # Next.js App Router
│   │   │   ├── (auth)/
│   │   │   │   ├── login/page.tsx
│   │   │   │   └── cadastro/page.tsx
│   │   │   ├── (app)/               # Rotas protegidas
│   │   │   │   ├── layout.tsx       # Layout com nav bottom tabs
│   │   │   │   ├── dashboard/page.tsx
│   │   │   │   ├── lancamento/page.tsx
│   │   │   │   ├── transacoes/page.tsx
│   │   │   │   └── perguntar/page.tsx
│   │   │   ├── onboarding/page.tsx
│   │   │   └── layout.tsx
│   │   ├── components/
│   │   │   ├── ui/                  # shadcn/ui (gerado automaticamente)
│   │   │   ├── transaction-card.tsx # Card de confirmação pós-IA
│   │   │   ├── nl-input.tsx         # Campo de linguagem natural
│   │   │   ├── dashboard-stats.tsx
│   │   │   └── transaction-list.tsx
│   │   ├── lib/
│   │   │   ├── api.ts               # Axios/fetch configurado com base URL
│   │   │   ├── auth.ts              # Helpers de autenticação Supabase
│   │   │   └── utils.ts
│   │   ├── store/
│   │   │   └── useAppStore.ts       # Zustand store
│   │   └── types/
│   │       └── index.ts             # Tipos TypeScript globais
│   ├── public/
│   ├── .env.local.example
│   ├── next.config.ts
│   ├── tailwind.config.ts
│   └── package.json
│
├── docs/
│   ├── ARQUITETURA_MVP.md           # Este arquivo
│   ├── wireframes_mvp.html          # Wireframes das 6 telas
│   └── test_frases_ia.json          # 30 frases de teste com JSON esperado
│
├── .gitignore
└── README.md
```

---

## 4. Modelo de Dados

### Tabela: `users`
```sql
id              UUID PRIMARY KEY DEFAULT gen_random_uuid()
supabase_id     TEXT UNIQUE NOT NULL        -- ID vindo do Supabase Auth
email           TEXT UNIQUE NOT NULL
name            TEXT
profile         TEXT                        -- estudante | estagiario | clt | freelancer | outro
objective       TEXT                        -- controlar | economizar | sair_do_vermelho
income_type     TEXT                        -- salario | estagio | freelance | variado
onboarding_done BOOLEAN DEFAULT FALSE
created_at      TIMESTAMPTZ DEFAULT NOW()
updated_at      TIMESTAMPTZ DEFAULT NOW()
```

### Tabela: `categories`
```sql
id          UUID PRIMARY KEY DEFAULT gen_random_uuid()
user_id     UUID REFERENCES users(id) ON DELETE CASCADE
name        TEXT NOT NULL                   -- "Alimentação", "Transporte", etc.
slug        TEXT NOT NULL                   -- "alimentacao", "transporte"
icon        TEXT                            -- emoji ou nome de ícone
is_default  BOOLEAN DEFAULT FALSE           -- criada pelo onboarding da IA
created_at  TIMESTAMPTZ DEFAULT NOW()

UNIQUE(user_id, slug)
```

### Tabela: `transactions`
```sql
id              UUID PRIMARY KEY DEFAULT gen_random_uuid()
user_id         UUID REFERENCES users(id) ON DELETE CASCADE
category_id     UUID REFERENCES categories(id) ON DELETE SET NULL
type            TEXT NOT NULL CHECK (type IN ('receita', 'despesa'))
amount          NUMERIC(12, 2) NOT NULL CHECK (amount > 0)
description     TEXT
date            DATE NOT NULL
raw_input       TEXT                        -- frase original digitada pelo usuário
ai_confidence   TEXT CHECK (ai_confidence IN ('alta', 'media', 'baixa'))
created_at      TIMESTAMPTZ DEFAULT NOW()
updated_at      TIMESTAMPTZ DEFAULT NOW()

-- Índices para performance nas queries mais comuns
INDEX idx_transactions_user_date ON transactions(user_id, date DESC)
INDEX idx_transactions_user_type ON transactions(user_id, type)
```

### Regras de negócio críticas
- `amount` é sempre positivo. O `type` define se é entrada ou saída.
- `raw_input` é salvo para debugging e melhoria do prompt da IA.
- `ai_confidence = 'baixa'` deve acionar destaque visual no card de confirmação.
- Soft delete não é necessário no MVP — deletar é deletar.

---

## 5. Endpoints da API

### Auth
```
POST /auth/register          -- cria user no Supabase + row na tabela users
POST /auth/login             -- delega ao Supabase, retorna JWT
POST /auth/logout
POST /auth/reset-password
```

### Onboarding
```
POST /onboarding/complete    -- salva perfil + dispara criação de categorias pela IA
GET  /onboarding/status      -- retorna se onboarding_done = true
```

### Transações
```
GET    /transactions                  -- lista paginada, filtro por mês
POST   /transactions                  -- cria transação (formulário manual)
GET    /transactions/{id}
PATCH  /transactions/{id}             -- edição parcial
DELETE /transactions/{id}
```

### IA
```
POST /ai/parse               -- recebe texto livre, retorna JSON estruturado (NÃO salva)
POST /ai/ask                 -- recebe pergunta, retorna resposta em texto
```

### Dashboard
```
GET /dashboard/summary       -- saldo, receitas, despesas do mês corrente
GET /dashboard/top-categories -- top N categorias do mês com valores
```

### Categorias
```
GET  /categories             -- lista categorias do usuário
POST /categories             -- cria categoria personalizada
```

---

## 6. Integração com a API Anthropic

### Serviço: `ai_parser.py`

**Prompt do sistema para parsing de transações:**

```python
SYSTEM_PROMPT_PARSER = """
Você é um assistente financeiro que extrai informações estruturadas de frases em português brasileiro.

Dado um texto do usuário, retorne APENAS um JSON válido com a seguinte estrutura:
{
  "tipo": "receita" | "despesa" | null,
  "valor": número ou null,
  "categoria": string ou null,
  "data": "YYYY-MM-DD" ou null,
  "descricao": string ou null,
  "confianca": "alta" | "media" | "baixa" | "nenhuma"
}

Categorias disponíveis: alimentacao, transporte, moradia, saude, educacao, lazer,
compras, assinaturas, academia, servicos, transferencia, salario, freelance,
investimentos, outros.

Regras:
- Se não houver valor na frase, retorne valor: null e confianca: "baixa"
- Se a frase não for uma transação financeira, retorne confianca: "nenhuma" e o resto null
- Data padrão quando não mencionada: data de hoje ({today})
- "ontem" = {yesterday}, "semana passada" = {last_monday}
- Valores com vírgula decimal: 25,50 = 25.50
- Ponto pode ser separador de milhar: 1.847,32 = 1847.32
- "k" informal: 1,5k = 1500
- Retorne APENAS o JSON, sem texto adicional, sem markdown, sem explicação
"""
```

**Função de parsing:**

```python
import anthropic
from datetime import date, timedelta
import json

async def parse_transaction(text: str, user_id: str) -> dict:
    client = anthropic.AsyncAnthropic()
    today = date.today()
    
    message = await client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=300,
        system=SYSTEM_PROMPT_PARSER.format(
            today=today.isoformat(),
            yesterday=(today - timedelta(days=1)).isoformat(),
            last_monday=(today - timedelta(days=today.weekday() + 7)).isoformat()
        ),
        messages=[{"role": "user", "content": text}]
    )
    
    raw = message.content[0].text.strip()
    return json.loads(raw)
```

### Serviço: consultas conversacionais (`ai_ask`)

```python
SYSTEM_PROMPT_ASK = """
Você é um assistente financeiro pessoal. Responda perguntas do usuário sobre
seus dados financeiros de forma simples, direta e em português.

Dados disponíveis do usuário (mês atual):
{financial_context}

Regras:
- Respostas curtas, máximo 3 frases
- Use valores em reais com formatação brasileira (R$ 1.234,56)
- Seja direto, sem introduções desnecessárias
- Se não tiver dados suficientes, diga isso claramente
"""
```

### Rate limiting (obrigatório desde o dia 1)
```python
# Limites por usuário por dia
LIMITS = {
    "parse": 50,     # 50 lançamentos por linguagem natural/dia (free)
    "ask": 20,       # 20 perguntas/dia (free)
}
# Implementar com Redis (Upstash). Chave: f"rate:{user_id}:{action}:{date}"
```

---

## 7. Segurança

### Regras inegociáveis
- Todo endpoint (exceto auth) exige JWT válido do Supabase no header `Authorization: Bearer {token}`
- Toda query filtra por `user_id` — nunca retornar dados de outros usuários
- Variáveis de ambiente: NUNCA commitar `.env`, usar `.env.example` com chaves vazias
- HTTPS sempre — Railway e Vercel já fornecem por padrão
- Logs nunca devem conter valores financeiros ou tokens JWT
- CORS configurado apenas para o domínio do frontend em produção

### Validação de inputs
- Pydantic valida todos os campos na entrada da API
- `amount` nunca negativo (o tipo define receita/despesa)
- `date` não pode ser mais de 5 anos no passado (evita lixo)
- Texto de linguagem natural: máximo 500 caracteres

---

## 8. Variáveis de Ambiente

### Backend (`.env`)
```env
# Banco
DATABASE_URL=postgresql+asyncpg://user:pass@host:5432/dbname

# Supabase
SUPABASE_URL=https://xxx.supabase.co
SUPABASE_SERVICE_ROLE_KEY=xxx        # nunca expor no frontend

# Anthropic
ANTHROPIC_API_KEY=sk-ant-xxx

# Redis
UPSTASH_REDIS_URL=rediss://xxx
UPSTASH_REDIS_TOKEN=xxx

# App
ENVIRONMENT=development              # development | production
CORS_ORIGINS=http://localhost:3000
```

### Frontend (`.env.local`)
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_SUPABASE_URL=https://xxx.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=xxx   # chave pública, pode expor
```

---

## 9. Fluxo de Desenvolvimento (Ordem de Implementação)

Siga esta ordem. Não pule etapas — cada uma é base da próxima.

```
Semana 1-2: Fundação
  [ ] Repositório Git com estrutura de pastas
  [ ] Backend: FastAPI rodando com health check
  [ ] Banco: Supabase criado, tabelas criadas via Alembic
  [ ] Auth: cadastro e login funcionando com Supabase Auth
  [ ] Frontend: Next.js + Tailwind + shadcn configurados
  [ ] Frontend: telas de login e cadastro consumindo a API

Semana 3-4: CRUD base
  [ ] Backend: endpoints CRUD de transações (sem IA ainda)
  [ ] Backend: endpoint de categorias
  [ ] Frontend: lista de transações funcional
  [ ] Frontend: formulário manual de lançamento (fallback da IA)
  [ ] Testes: pytest cobrindo endpoints principais

Semana 5-6: IA (coração do produto)
  [ ] Backend: serviço ai_parser integrado com API Anthropic
  [ ] Backend: endpoint POST /ai/parse testado com as 30 frases do JSON
  [ ] Backend: rate limiting com Redis implementado
  [ ] Frontend: campo de linguagem natural + card de confirmação
  [ ] Frontend: fluxo completo — digita → confirma → salva → lista atualiza

Semana 7-8: Dashboard + Consultas
  [ ] Backend: endpoints de dashboard (summary + top-categories)
  [ ] Backend: serviço ai_ask para consultas conversacionais
  [ ] Frontend: dashboard com 3 números + top categorias
  [ ] Frontend: tela "Pergunte à IA"

Semana 9-10: Onboarding + Polimento
  [ ] Backend: fluxo de onboarding com criação de categorias pela IA
  [ ] Frontend: telas de onboarding (3 perguntas)
  [ ] Estados vazios (usuário sem dados)
  [ ] Telas de erro e loading states
  [ ] Responsividade mobile
  [ ] Deploy: backend no Railway, frontend na Vercel

Semana 11-12: Beta fechado
  [ ] 10-20 usuários amigos
  [ ] Monitoramento com Sentry
  [ ] Coleta de feedback
  [ ] Correção de bugs encontrados em uso real
```

---

## 10. Testes

### Arquivo de referência
O arquivo `docs/test_frases_ia.json` contém 30 frases com JSON esperado.
Use-o como suite de regressão para o prompt da IA.

### Como rodar os testes de IA
```python
# tests/test_ai_parser.py
import pytest
import json
from app.services.ai_parser import parse_transaction

with open("docs/test_frases_ia.json") as f:
    TEST_CASES = json.load(f)["casos_de_teste"]

@pytest.mark.asyncio
@pytest.mark.parametrize("caso", TEST_CASES)
async def test_parse_frase(caso):
    if caso["output_esperado"]["confianca"] == "nenhuma":
        result = await parse_transaction(caso["input"])
        assert result["tipo"] is None
        return
    
    result = await parse_transaction(caso["input"])
    expected = caso["output_esperado"]
    
    assert result["tipo"] == expected["tipo"]
    if expected["valor"] is not None:
        assert abs(result["valor"] - expected["valor"]) < 0.01
    assert result["categoria"] == expected["categoria"]
```

### Cobertura mínima aceitável antes do beta
- Todos os endpoints de transações: 80%+
- ai_parser: 100% das 30 frases passando
- Auth: fluxos de cadastro e login

---

## 11. Decisões Registradas (ADRs simplificados)

| Decisão | Escolha | Alternativa descartada | Motivo |
|---|---|---|---|
| Backend language | Python | Node.js | Time domina Python |
| Backend framework | FastAPI | Django | Mais leve para API, async nativo |
| ORM | SQLAlchemy | Prisma/Tortoise | Mais maduro, melhor suporte Python |
| Auth | Supabase Auth | Auth próprio | Não reinventar a roda, segurança garantida |
| Frontend | Next.js | Vue/Nuxt | Ecossistema React maior, Claude Code tem mais contexto |
| IA | Anthropic Claude | OpenAI GPT | Já têm conta, melhor para JSON estruturado |
| Hosting backend | Railway | AWS | Menos overhead para MVP, escala depois |
| Cache/Rate limit | Upstash Redis | In-memory | Persiste entre restarts, serverless simples |
| Estado frontend | Zustand | Redux | Sem boilerplate, suficiente para MVP |

---

## 12. Como Usar Este Documento com Claude Code

Ao iniciar uma sessão no Claude Code, cole o seguinte como primeira mensagem:

```
Leia o arquivo docs/ARQUITETURA_MVP.md antes de qualquer coisa.
Ele contém todas as decisões de arquitetura, stack, modelo de dados e
ordem de implementação deste projeto.

Após ler, confirme que entendeu e me diga qual é a próxima tarefa
pendente com base no checklist da Seção 9 (Fluxo de Desenvolvimento).
```

A partir daí, referencie sempre este documento quando houver dúvidas de decisão.
Se o Claude Code sugerir algo que conflite com este documento, questione antes de aceitar.
```
