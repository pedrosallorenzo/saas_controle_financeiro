import json
from datetime import date, timedelta
import anthropic
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.models.transaction import Transaction

SYSTEM_PROMPT_PARSER = """
Você é um assistente financeiro que extrai informações estruturadas de frases em português brasileiro.

Dado um texto do usuário, retorne APENAS um JSON válido com a seguinte estrutura:
{{
  "tipo": "receita" | "despesa" | null,
  "valor": número ou null,
  "categoria": string ou null,
  "data": "YYYY-MM-DD" ou null,
  "descricao": string ou null,
  "confianca": "alta" | "media" | "baixa" | "nenhuma"
}}

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


async def parse_transaction(text: str, user_id: str) -> dict:
    client = anthropic.AsyncAnthropic()
    today = date.today()

    message = await client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=300,
        system=SYSTEM_PROMPT_PARSER.format(
            today=today.isoformat(),
            yesterday=(today - timedelta(days=1)).isoformat(),
            last_monday=(today - timedelta(days=today.weekday() + 7)).isoformat(),
        ),
        messages=[{"role": "user", "content": text}],
    )

    raw = message.content[0].text.strip()
    return json.loads(raw)


async def ask_financial_question(question: str, user_id: str, db: AsyncSession) -> str:
    today = date.today()
    first_day = date(today.year, today.month, 1)

    result = await db.execute(
        select(Transaction.type, func.sum(Transaction.amount).label("total"))
        .where(Transaction.user_id == user_id, Transaction.date >= first_day)
        .group_by(Transaction.type)
    )
    rows = result.all()

    receitas = float(next((r.total for r in rows if r.type == "receita"), 0))
    despesas = float(next((r.total for r in rows if r.type == "despesa"), 0))

    financial_context = (
        f"Mês: {today.strftime('%B/%Y')}\n"
        f"Receitas: R$ {receitas:,.2f}\n"
        f"Despesas: R$ {despesas:,.2f}\n"
        f"Saldo: R$ {receitas - despesas:,.2f}"
    )

    client = anthropic.AsyncAnthropic()
    message = await client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=200,
        system=SYSTEM_PROMPT_ASK.format(financial_context=financial_context),
        messages=[{"role": "user", "content": question}],
    )
    return message.content[0].text.strip()
