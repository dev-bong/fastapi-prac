from fastapi import APIRouter

from database import SessionLocal
from models import Post

router = APIRouter(
    prefix="/api/post",
)

@router.get("/list")
def post_list():
    db = SessionLocal()
    _question_list = db.query(Post).order_by(Post.create_date.desc()).all()
    db.close()
    return _question_list