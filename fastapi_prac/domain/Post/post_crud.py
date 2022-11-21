from datetime import datetime
from datetime import timedelta

from domain.Post.post_schema import PostCreate
from models import Post
from sqlalchemy.orm import Session


def get_post_list(db: Session, skip: int = 0, limit: int = 10):
    _post_list = db.query(Post).order_by(Post.create_date.desc()).all()

    total = len(_post_list)
    #post_list = _post_list.offset(skip).limit(limit).all()
    post_list = _post_list[skip * limit : (skip + 1) * limit]

    # 한국 시차 적용
    for post in post_list:
        post.create_date += timedelta(hours=9)

    return total, post_list


def get_post(db: Session, post_id: int, just_get=False):
    post = db.query(Post).get(post_id)

    # 한국 시차 적용 #? just_get? : comment 생성을 위해 조회할때는 시차 적용 X
    if just_get:
        post.create_date += timedelta(hours=9)
        for comment in post.comments:
            comment.create_date += timedelta(hours=9)

    return post


def create_post(db: Session, post_create: PostCreate):
    db_post = Post(
        subject=post_create.subject,
        content=post_create.content,
        create_date=datetime.utcnow(),
    )
    db.add(db_post)
    db.commit()
