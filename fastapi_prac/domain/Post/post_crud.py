from datetime import datetime

from domain.Post.post_schema import PostCreate, PostUpdate
from models import Post, User
from sqlalchemy.orm import Session


def get_post_list(db: Session, skip: int = 0, limit: int = 10):
    _post_list = db.query(Post).order_by(Post.create_date.desc()).all()

    total = len(_post_list)
    post_list = _post_list[skip * limit : (skip + 1) * limit]

    return total, post_list


def get_post(db: Session, post_id: int):
    post = db.query(Post).get(post_id)
    return post


def create_post(db: Session, post_create: PostCreate, user: User):
    db_post = Post(
        subject=post_create.subject,
        content=post_create.content,
        create_date=datetime.now(),
        user=user,
    )
    db.add(db_post)
    db.commit()


def update_post(db: Session, db_post: Post, post_update: PostUpdate):
    db_post.subject = post_update.subject
    db_post.content = post_update.content
    db_post.modify_date = datetime.now()
    db.add(db_post)
    db.commit()


def delete_post(db: Session, db_post: Post):
    db.delete(db_post)
    db.commit()
