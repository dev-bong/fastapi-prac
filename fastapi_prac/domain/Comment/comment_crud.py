from datetime import datetime

from sqlalchemy.orm import Session

from domain.Comment.comment_schema import CommentCreate
from models import Post, Comment


def create_comment(db: Session, post: Post, comment_create: CommentCreate):
    db_comment = Comment(
        post=post, content=comment_create.content, create_date=datetime.utcnow()
    )
    db.add(db_comment)
    db.commit()
