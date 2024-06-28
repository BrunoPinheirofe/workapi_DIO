from uuid import uuid4

from fastapi import APIRouter, Body, HTTPException, status
from pydantic import UUID4
from sqlalchemy import select

from workoutapi.centro_treinamento.models import CentroTreinamentoModel
from workoutapi.centro_treinamento.schemas import (
    CentroTreinamentoIn,
    CentroTreinamentoOut,
)
from workoutapi.contrib.dependencies import DatabaseDependency

rounter = APIRouter()


@rounter.post(
    path='/',
    summary='cadastrar novo centro de treinamentos',
    status_code=status.HTTP_201_CREATED,
    response_model=CentroTreinamentoOut,
)
async def post(
    db_session: DatabaseDependency,
    centro_treinamento_in: CentroTreinamentoIn = Body(...),
) -> CentroTreinamentoOut:
    centro_treinamento_out = CentroTreinamentoOut(
        id=uuid4(), **centro_treinamento_in.model_dump()
    )
    centro_treinamento_model: CentroTreinamentoModel = CentroTreinamentoModel(
        **centro_treinamento_out.model_dump()
    )
    db_session.add(centro_treinamento_model)
    await db_session.commit()
    return centro_treinamento_out


@rounter.get(
    path='/',
    summary='consultar todos os centros de treinamento',
    status_code=status.HTTP_200_OK,
    response_model=list[CentroTreinamentoOut],
)
async def query(db_session: DatabaseDependency) -> list[CentroTreinamentoOut]:
    centroTreinamentos: list[CentroTreinamentoOut] = (await db_session.execute(select(CentroTreinamentoModel))).scalars().all()  # type: ignore
    return centroTreinamentos


async def get_by_id(
    id: UUID4, db_session: DatabaseDependency
) -> CentroTreinamentoOut | dict:
    CentroTreinamento: CentroTreinamentoOut = (
        (await db_session.execute(select(CentroTreinamentoModel).filter_by(id=id)))
        .scalars()
        .first()
    )  # type: ignore
    if not CentroTreinamento:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'CentroTreinamento não encontrada com o id: {id}',
        )
    return CentroTreinamento
