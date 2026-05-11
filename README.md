# SaaS Finanças

Controle financeiro pessoal por linguagem natural.

## Estrutura

```
backend/   FastAPI + SQLAlchemy + Supabase + Anthropic
frontend/  Next.js 14 + TypeScript + Tailwind + shadcn/ui
docs/      Arquitetura, wireframes e casos de teste da IA
```

## Quick start

```bash
# Backend
cd backend
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # preencher credenciais
uvicorn app.main:app --reload

# Frontend (outro terminal)
cd frontend
npm install
cp .env.local.example .env.local   # preencher credenciais
npm run dev
```

Leia `docs/ARQUITETURA_MVP.md` antes de qualquer coisa.
