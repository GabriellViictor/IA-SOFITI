# app/schemas.py

from pydantic import BaseModel
from typing import List, Union


class LocalInput(BaseModel):
    tipogui: str
    codcon: str
    codmed: str

class AcomodacaoInput(BaseModel):
    tipogui: str
    codcon: str
    codloc: str
    codmed: str

class ProcedimentoInput(BaseModel):
    tipogui: str
    codcon: str
    codloc: str
    acomoda: str
    codmed: str


class RecomendacaoList(BaseModel):
    Recomendacoes: List[str]

class RecomendacaoListPRO(BaseModel):
    Recomendacoes: List[str]
    Recomendacoes_6MO: List[str]

class AutoInput(BaseModel):
    tipogui: str
    codcon: str

class AutoOutput(BaseModel):
    local_recomendado: str
    acomodacao_recomendada: str
    procedimento_recomendado: List[str]

class RecomendacaoItem(BaseModel):
    code: str
    description: str

class RecomendacaoProcedimentoResponse(BaseModel):
    recomendacoes_geral: List[RecomendacaoItem]
    recomendacoes_6_meses: List[RecomendacaoItem]