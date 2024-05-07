from fastapi import FastAPI, APIRouter
from patients_app import models
from settings import engine
from users.api.router import router as users_router
from patients_app.api.router import router as patients_router
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

origins = [
    'http://localhost:3000'
]


app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"]
)

app.include_router(users_router)
app.include_router(patients_router)

models.Base.metadata.create_all(engine)
