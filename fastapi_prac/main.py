import os

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

app = FastAPI()
front_url = os.environ.get("EXTERNAL_FRONT_URL", "http://127.0.0.1:5173")

origins = [
    front_url,
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/hello")
async def root():
    return {"message": "Test msg"}