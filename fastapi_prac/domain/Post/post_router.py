from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from domain.Post import post_schema, post_crud

router = APIRouter(
    prefix="/api/post",
)

@router.get("/list", response_model=list[post_schema.Post])
def post_list(db: Session = Depends(get_db)):
    _post_list = post_crud.get_post_list(db)
    return _post_list