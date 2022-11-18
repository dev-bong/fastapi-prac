import datetime

from pydantic import BaseModel

from domain.Comment.comment_schema import Comment

class Post(BaseModel):
    id: int
    subject: str
    content: str
    create_date: datetime.datetime
    comments: list[Comment] = []

    class Config:
        orm_mode = True