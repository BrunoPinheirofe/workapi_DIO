from uuid import uuid4

from fastapi import APIRouter, Body, HTTPException, status
from pydantic import UUID4
from sqlalchemy.future import select

from workoutapi.atleta.models import AtletaModel
from workoutapi.atleta.schemas import AtletaIn, AtletaOut, AtletaUpdate
from workoutapi.categoria.models import CategoriaModel
from workoutapi.centro_treinamento.models import CentroTreinamentoModel
from workoutapi.contrib.dependencies import DatabaseDependency
from datetime import datetime

rounter = APIRouter()


@rounter.post(
    path="/",
    summary="cadastrar nova atleta",
    status_code=status.HTTP_201_CREATED,
    response_model=AtletaOut,
)
async def post(
    db_session: DatabaseDependency, atleta_in: AtletaIn = Body(...)
) -> AtletaOut:
    atleta_existe = (await db_session.execute(select(AtletaModel).filter_by(cpf=atleta_in.cpf))).scalars().first()
    if atleta_existe:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Atleta com cpf{atleta_in.cpf} já esta na base de dados",
        )
        
    nome_categoria = atleta_in.categoria.nome
    categoria = (
        (
            await db_session.execute(
                select(CategoriaModel).filter_by(nome=nome_categoria)
            )
        )
        .scalars()
        .first()
    )
    if not categoria:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"categoria {nome_categoria} não foi encontrada!!!",
        )

    nome_centro_treinamento = atleta_in.centro_treinamento.nome
    centro_treinamento = (
        (
            await db_session.execute(
                select(CentroTreinamentoModel).filter_by(nome=nome_centro_treinamento)
            )
        )
        .scalars()
        .first()
    )
    if not centro_treinamento:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"centro de treinamento: {nome_centro_treinamento} não foi encontrado!!!",
        )
        
    try:
        atleta_out = AtletaOut(
            id=uuid4(), create_at=datetime.utcnow(), **atleta_in.model_dump()
        )
        atleta_model = AtletaModel(
            **atleta_out.model_dump(exclude={"categoria", "centro_treinamento"})
        )
        atleta_model.categoria_id = categoria.pk_id
        atleta_model.centro_treinamento_id = centro_treinamento.pk_id
        
        db_session.add(atleta_model)
        await db_session.commit()
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ocorrou um erro ao inserir os dados no banco",
        )
    return atleta_out


@rounter.get(
    path="/",
    summary="consultar todos as atletas",
    status_code=status.HTTP_200_OK,
    response_model=list[AtletaOut],
)
async def query(db_session: DatabaseDependency) -> list[AtletaOut]:
    atletas: list[AtletaOut] = (await db_session.execute(select(AtletaModel))).scalars().all()  # type: ignore
    return [AtletaOut.model_validate(atleta) for atleta in atletas]


@rounter.get(
    path="/{id}",
    summary="consultar atleta por id",
    status_code=status.HTTP_200_OK,
    response_model=AtletaOut,
)
async def get_by_id(id: UUID4, db_session: DatabaseDependency) -> AtletaOut | dict:
    atleta: AtletaOut = (
        (await db_session.execute(select(AtletaModel).filter_by(id=id)))
        .scalars()
        .first()
    )  # type: ignore
    if not atleta:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"atleta não encontrada com o id: {id}",
        )
    return atleta

@rounter.patch(
    path="/{id}",
    summary="editar atleta por id",
    status_code=status.HTTP_200_OK,
    response_model=AtletaOut,
)

async def patch(id: UUID4, db_session: DatabaseDependency, atleta_up: AtletaUpdate):
    atleta: AtletaOut = (
        (await db_session.execute(select(AtletaModel).filter_by(id=id)))
        .scalars()
        .first()
    )  # type: ignore
    if not atleta:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"atleta não encontrada com o id: {id}",
        )
    atleta_update = atleta_up.model_dump(exclude_unset=True)
    for key, value in atleta_update.items():
        setattr(atleta, key, value)
    await db_session.refresh(atleta)
    await db_session.commit()
    return atleta

@rounter.delete(
    path="/{id}",
    summary="teletar atleta por id",
    status_code=status.HTTP_204_NO_CONTENT,
    response_model=AtletaOut,
)


async def delete_by_id(id: UUID4, db_session: DatabaseDependency) -> None:
    atleta: AtletaOut = (
        (await db_session.execute(select(AtletaModel).filter_by(id=id)))
        .scalars()
        .first()
    )  # type: ignore
    if not atleta:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"atleta não encontrada com o id: {id}",
        )
    await db_session.delete(atleta)
    await db_session.commit()

