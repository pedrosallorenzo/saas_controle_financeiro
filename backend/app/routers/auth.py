from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
from app.deps import get_db
from app.models.user import User
from app.config import settings
import httpx

router = APIRouter()


class RegisterRequest(BaseModel):
    email: str
    password: str
    name: str | None = None


class LoginRequest(BaseModel):
    email: str
    password: str


@router.post("/register", status_code=201)
async def register(body: RegisterRequest, db: AsyncSession = Depends(get_db)):
    async with httpx.AsyncClient() as client:
        resp = await client.post(
            f"{settings.supabase_url}/auth/v1/signup",
            headers={
                "apikey": settings.supabase_service_role_key,
                "Content-Type": "application/json",
            },
            json={"email": body.email, "password": body.password},
        )
    if resp.status_code not in (200, 201):
        raise HTTPException(status_code=400, detail=resp.json().get("msg", "Erro no cadastro"))

    data = resp.json()
    supabase_user = data.get("user") or data
    user = User(supabase_id=supabase_user["id"], email=body.email, name=body.name)
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return {"message": "Usuário criado com sucesso", "user_id": str(user.id)}


@router.post("/login")
async def login(body: LoginRequest):
    async with httpx.AsyncClient() as client:
        resp = await client.post(
            f"{settings.supabase_url}/auth/v1/token?grant_type=password",
            headers={
                "apikey": settings.supabase_service_role_key,
                "Content-Type": "application/json",
            },
            json={"email": body.email, "password": body.password},
        )
    if resp.status_code != 200:
        raise HTTPException(status_code=401, detail="Credenciais inválidas")
    return resp.json()


@router.post("/logout")
async def logout():
    return {"message": "Logout realizado"}


@router.post("/reset-password")
async def reset_password(email: str):
    async with httpx.AsyncClient() as client:
        await client.post(
            f"{settings.supabase_url}/auth/v1/recover",
            headers={
                "apikey": settings.supabase_service_role_key,
                "Content-Type": "application/json",
            },
            json={"email": email},
        )
    return {"message": "E-mail de recuperação enviado"}
