from typing import Optional
from pydantic import BaseModel, field_validator


class ParseRequest(BaseModel):
    text: str

    @field_validator("text")
    @classmethod
    def validate_length(cls, v: str) -> str:
        if len(v) > 500:
            raise ValueError("text deve ter no máximo 500 caracteres")
        return v


class ParseResponse(BaseModel):
    tipo: Optional[str]
    valor: Optional[float]
    categoria: Optional[str]
    data: Optional[str]
    descricao: Optional[str]
    confianca: str


class AskRequest(BaseModel):
    question: str


class AskResponse(BaseModel):
    answer: str
