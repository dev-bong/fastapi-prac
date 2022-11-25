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


@router.delete("/delete", status_code=status.HTTP_204_NO_CONTENT)
def answer_delete(
    _comment_delete: comment_schema.CommentDelete,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    db_comment = comment_crud.get_comment(db, comment_id=_comment_delete.comment_id)
    if not db_comment:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="데이터를 찾을수 없습니다."  # ? 404?
        )
    if current_user.id != db_comment.user.id:
        if current_user.username == "master-bong":  # ? 운영자일 경우 다른사람 게시글도 삭제 가능
            pass
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="삭제 권한이 없습니다."  # ? 403?
            )
    comment_crud.delete_comment(db=db, db_comment=db_comment)
