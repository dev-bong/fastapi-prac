from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette import status

from database import get_db
from domain.Post import post_schema, post_crud
from domain.User.user_router import get_current_user
from models import User

router = APIRouter(
    prefix="/api/post",
)


@router.get("/list", response_model=post_schema.PostList)
def post_list(db: Session = Depends(get_db), page: int = 0, size: int = 10):
    total, _post_list = post_crud.get_post_list(db, skip=page, limit=size)
    return {"total": total, "post_list": _post_list}


@router.get("/detail/{post_id}", response_model=post_schema.Post)
def post_detail(post_id: int, db: Session = Depends(get_db)):
    post = post_crud.get_post(db, post_id=post_id, just_get=True)
    return post


@router.post("/create", status_code=status.HTTP_204_NO_CONTENT)
def post_create(
    _post_create: post_schema.PostCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    post_crud.create_post(db=db, post_create=_post_create, user=current_user)
