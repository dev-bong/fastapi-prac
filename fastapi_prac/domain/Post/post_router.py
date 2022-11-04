from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from models import Post

router = APIRouter(
    prefix="/api/post",
)

@router.get("/list")
def post_list(db: Session = Depends(get_db)):
    _question_list = db.query(Post).order_by(Post.create_date.desc()).all()
    return _question_list