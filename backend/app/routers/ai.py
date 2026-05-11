from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.deps import get_db, get_current_user
from app.schemas.ai import AskRequest, AskResponse, ParseRequest, ParseResponse
from app.services.ai_parser import parse_transaction, ask_financial_question
from app.services.rate_limiter import check_rate_limit

router = APIRouter()


@router.post("/parse", response_model=ParseResponse)
async def parse_nl(
    body: ParseRequest,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    if not await check_rate_limit(str(current_user.id), "parse"):
        raise HTTPException(status_code=429, detail="Limite diário de lançamentos atingido")
    return await parse_transaction(body.text, str(current_user.id))


@router.post("/ask", response_model=AskResponse)
async def ask_ai(
    body: AskRequest,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    if not await check_rate_limit(str(current_user.id), "ask"):
        raise HTTPException(status_code=429, detail="Limite diário de perguntas atingido")
    answer = await ask_financial_question(body.question, str(current_user.id), db)
    return AskResponse(answer=answer)
