from datetime import datetime

from sqlalchemy.orm import Session

from domain.Comment.comment_schema import CommentCreate
from models import Post, Comment, User


def create_comment(db: Session, post: Post, comment_create: CommentCreate, user: User):
    db_comment = Comment(
        post=post,
        content=comment_create.content,
        create_date=datetime.now(),
        user=user,
    )
    db.add(db_comment)
    db.commit()


def get_comment(db: Session, comment_id: int):
    return db.query(Comment).get(comment_id)


def delete_comment(db: Session, db_comment: Comment):
    db.delete(db_comment)
    db.commit()
