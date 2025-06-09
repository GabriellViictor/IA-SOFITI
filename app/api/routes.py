from typing import List
from fastapi import APIRouter, HTTPException
from app.core.rbc_engine import AtendimentoRecommender
from app.schemas.schemas import (
    LocalInput,
    AcomodacaoInput,
    ProcedimentoInput,
    RecomendacaoItem
)

router = APIRouter()
atendimento_recommender = AtendimentoRecommender()

def validar_campos_obrigatorios(campos: dict):
    campos_vazios = [k for k, v in campos.items() if v is None or (isinstance(v, str) and not v.strip())]
    if campos_vazios:
        raise HTTPException(
            status_code=422,
            detail=[{"campo": campo, "mensagem": "Campo obrigatório ausente ou vazio"} for campo in campos_vazios]
        )

@router.post("/recommend/local", response_model=List[RecomendacaoItem])
async def recommend_local(data: LocalInput):
    validar_campos_obrigatorios({
        "tipogui": data.tipogui,
        "codcon": data.codcon,
        "codmed": data.codmed
    })
    try:
        recs = atendimento_recommender.recommend_local(data.tipogui, data.codcon, data.codmed, top_n=10000)
        if not recs:
            raise HTTPException(status_code=204, detail="Nenhuma recomendação encontrada.")
        return recs
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))

@router.post("/recommend/acomodacao", response_model=List[RecomendacaoItem])
async def recommend_acomoda(data: AcomodacaoInput):
    validar_campos_obrigatorios({
        "tipogui": data.tipogui,
        "codcon": data.codcon,
        "codloc": data.codloc,
        "codmed": data.codmed
    })
    try:
        recs = atendimento_recommender.recommend_acomoda(
            data.tipogui, data.codcon, data.codloc, data.codmed, top_n=10000
        )
        if not recs:
            raise HTTPException(status_code=204, detail="Nenhuma recomendação encontrada.")
        return recs
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))

@router.post("/recommend/procedimentos", response_model=List[RecomendacaoItem])
async def recommend_procedimentos(data: ProcedimentoInput):
    validar_campos_obrigatorios({
        "tipogui": data.tipogui,
        "codcon": data.codcon,
        "codloc": data.codloc,
        "acomoda": data.acomoda,
        "codmed": data.codmed
    })
    try:
        recs = atendimento_recommender.recommend_proced(
            data.tipogui, data.codcon, data.codloc, data.acomoda, data.codmed, top_n=10000
        )
        if not recs:
            raise HTTPException(status_code=204, detail="Nenhuma recomendação encontrada.")
        return recs
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))

