from typing import Annotated, Optional

from pydantic import Field, PositiveFloat

from workoutapi.categoria.schemas import CategoriaIn
from workoutapi.centro_treinamento.schemas import CentroTreinamentoAtleta
from workoutapi.contrib.schemas import BaseSchemas, OutMixin


class Atleta(BaseSchemas):
    nome: Annotated[
        str, Field(description="Nome do Atleta", examples=["Joao"], max_length=50)
    ]
    cpf: Annotated[
        str, Field(description="CPF do Atleta", examples=["32143423342"], max_length=11)
    ]
    idade: Annotated[int, Field(description="Idade do Atleta", examples=[25])]
    peso: Annotated[PositiveFloat, Field(description="Peso do Atleta", examples=[79.0])]
    altura: Annotated[
        PositiveFloat, Field(description="Altura do Atleta", examples=[1.89])
    ]
    sexo: Annotated[
        str, Field(description="Sexo do Atleta", examples=["M"], max_length=1)
    ]
    categoria: Annotated[CategoriaIn, Field(description='Categoria do Atleta', examples=['Skate'])]
    centro_treinamento: Annotated[CentroTreinamentoAtleta, Field(description='Centro Treinamento do Atleta', examples=['CT BULLS'])]


class AtletaIn(Atleta):
    pass


class AtletaOut(Atleta, OutMixin):
    pass

class AtletaUpdate(BaseSchemas):
    nome: Annotated[
        Optional[str], Field(None, description="Nome do Atleta", examples=["Joao"], max_length=50)
    ]
    idade: Annotated[Optional[int], Field(None, description="Idade do Atleta", examples=[25])]