from fastapi import FastAPI

from workoutapi.rounters import api_rounter

app = FastAPI(title='Projeto WorkoutAPI')
app.include_router(api_rounter)
