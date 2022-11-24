from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from database import get_db
from domain.Comment import comment_schema, comment_crud
from domain.Post import post_crud
from domain.User.user_router import get_current_user
from models import User

router = APIRouter(
    prefix="/api/comment",
)


@router.post("/create/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def comment_create(
    post_id: int,
    _comment_create: comment_schema.CommentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    # create comment
    post = post_crud.get_post(db, post_id=post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    comment_crud.create_comment(
        db, post=post, comment_create=_comment_create, user=current_user
    )


@router.get("/detail/{comment_id}", response_model=comment_schema.Comment)
def comment_detail(comment_id: int, db: Session = Depends(get_db)):
    comment = comment_crud.get_comment(db, comment_id=comment_id)
    return comment
