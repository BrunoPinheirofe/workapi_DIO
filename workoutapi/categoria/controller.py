from uuid import uuid4

from fastapi import APIRouter, Body, HTTPException, status
from pydantic import UUID4
from sqlalchemy.future import select

from workoutapi.categoria.models import CategoriaModel
from workoutapi.categoria.schemas import CategoriaIn, CategoriaOut
from workoutapi.contrib.dependencies import DatabaseDependency

rounter = APIRouter()


@rounter.post(
    path='/',
    summary='cadastrar nova categoria',
    status_code=status.HTTP_201_CREATED,
    response_model=CategoriaOut,
)
async def post(
    db_session: DatabaseDependency, categoria_in: CategoriaIn = Body(...)
) -> CategoriaOut:

    categoria_out = CategoriaOut(id=uuid4(), **categoria_in.model_dump())
    categoria_model = CategoriaModel(**categoria_out.model_dump())
    db_session.add(categoria_model)
    await db_session.commit()
    return categoria_out


@rounter.get(
    path='/',
    summary='consultar todas as categoria',
    status_code=status.HTTP_200_OK,
    response_model=list[CategoriaOut],
)
async def query(db_session: DatabaseDependency) -> list[CategoriaOut]:
    categorias: list[CategoriaOut] = (await db_session.execute(select(CategoriaModel))).scalars().all()  # type: ignore
    return categorias


@rounter.get(
    path='/{id}',
    summary='consultar categoria por id',
    status_code=status.HTTP_200_OK,
    response_model=CategoriaOut
)
async def get_by_id(id: UUID4, db_session: DatabaseDependency) -> CategoriaOut | dict:
    categoria: CategoriaOut = (
        await db_session.execute(
        select(CategoriaModel).filter_by(id=id))
        ).scalars().first()  # type: ignore
    if not categoria:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f'categoria não encontrada com o id: {id}'
            )
    return categoria
