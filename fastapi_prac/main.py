# import models
from env_inform import FRONT_URL

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
# from database import engine
from domain.Post import post_router
from domain.Comment import comment_router

app = FastAPI()
#models.Base.metadata.create_all(bind=engine)

origins = [
    FRONT_URL,
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(post_router.router)
app.include_router(comment_router.router)