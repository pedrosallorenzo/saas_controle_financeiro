# Backend — SaaS Finanças

FastAPI + SQLAlchemy + Supabase + Anthropic

## Setup local

```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# preencher .env com as credenciais reais
uvicorn app.main:app --reload
```

## Migrations

```bash
alembic upgrade head
```

## Testes

```bash
pytest
```

API disponível em `http://localhost:8000` — documentação automática em `/docs`.
