from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from database import get_db
from domain.Comment import comment_schema, comment_crud
from domain.Post import post_crud

router = APIRouter(
    prefix="/api/comment",
)


@router.post("/create/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def comment_create(
    post_id: int,
    _comment_create: comment_schema.CommentCreate,
    db: Session = Depends(get_db),
):

    # create comment
    post = post_crud.get_post(db, post_id=post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    comment_crud.create_comment(db, post=post, comment_create=_comment_create)