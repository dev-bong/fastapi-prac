from fastapi import APIRouter, Depends, HTTPException
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
    post = post_crud.get_post(db, post_id=post_id)
    return post


@router.post("/create", status_code=status.HTTP_204_NO_CONTENT)
def post_create(
    _post_create: post_schema.PostCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    post_crud.create_post(db=db, post_create=_post_create, user=current_user)


@router.put("/update", status_code=status.HTTP_204_NO_CONTENT)
def post_update(
    _post_update: post_schema.PostUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    db_post = post_crud.get_post(db, post_id=_post_update.post_id)
    if not db_post:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="데이터를 찾을수 없습니다."  # ? 404?
        )
    if current_user.id != db_post.user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="수정 권한이 없습니다."  # ? 403?
        )
    post_crud.update_post(db=db, db_post=db_post, post_update=_post_update)


@router.delete("/delete", status_code=status.HTTP_204_NO_CONTENT)
def post_delete(
    _post_delete: post_schema.PostDelete,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    db_post = post_crud.get_post(db, post_id=_post_delete.post_id)
    if not db_post:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="데이터를 찾을수 없습니다."  # ? 404?
        )
    if current_user.id != db_post.user.id:
        if current_user.username == "master-bong": #? 운영자일 경우 다른사람 게시글도 삭제 가능
            pass
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="삭제 권한이 없습니다."  # ? 403?
            )
    post_crud.delete_post(db=db, db_post=db_post)
