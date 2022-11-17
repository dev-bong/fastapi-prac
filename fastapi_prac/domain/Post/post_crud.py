from models import Post
from sqlalchemy.orm import Session

def get_post_list(db: Session):
    post_list = db.query(Post).order_by(Post.create_date.desc()).all()
    return post_list