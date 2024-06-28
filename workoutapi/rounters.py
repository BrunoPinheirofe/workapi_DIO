from fastapi import APIRouter

from workoutapi.atleta.controller import rounter as atleta
from workoutapi.categoria.controller import rounter as categoria
from workoutapi.centro_treinamento.controller import rounter as centro_treinamentos
api_rounter = APIRouter()


api_rounter.include_router(atleta, prefix='/atletas', tags=['atletas'])
api_rounter.include_router(categoria, prefix='/categorias', tags=['categorias'])
api_rounter.include_router(centro_treinamentos, prefix='/centro_treinamentos', tags=['centro_treinamentos'])
