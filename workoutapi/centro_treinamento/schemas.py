from typing import Annotated

from pydantic import UUID4, Field

from workoutapi.contrib.schemas import BaseSchemas


class CentroTreinamento(BaseSchemas):
    nome: Annotated[
        str,
        Field(
            description="Nome do Centro de Treinamentos",
            examples=["CT BULLS"],
            max_length=20,
        ),
    ]
    endereco: Annotated[
        str,
        Field(
            description="Endetereço do Centro de Treinamentos",
            examples=["Rua 51, 1223, Bairro Da Laranja"],
            max_length=60,
        ),
    ]
    propietario: Annotated[
        str,
        Field(
            description="Propietario do Centro de Treinamentos",
            examples=["Jonas"],
            max_length=30,
        ),
    ]


class CentroTreinamentoIn(CentroTreinamento):
    pass


class CentroTreinamentoOut(CentroTreinamento):
    id: Annotated[UUID4, Field(description="Indentificador do centro de treinamentos")]


class CentroTreinamentoAtleta(BaseSchemas):
    nome: Annotated[
        str,
        Field(
            description="Nome do Centro de Treinamentos",
            examples=["CT BULLS"],
            max_length=20,
        ),
    ]