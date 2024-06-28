from typing import Annotated

from pydantic import UUID4, Field

from workoutapi.contrib.schemas import BaseSchemas


class Categoria(BaseSchemas):
    nome: Annotated[
        str, Field(description="Nome da Categoria", examples=["Natação"], max_length=10)
    ]


class CategoriaIn(Categoria):
    pass


class CategoriaOut(Categoria):
    id: Annotated[UUID4, Field(description="Indentificador da categoria")]
