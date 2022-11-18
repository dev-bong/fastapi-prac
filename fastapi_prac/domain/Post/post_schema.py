import datetime

from pydantic import BaseModel, validator

from domain.Comment.comment_schema import Comment

class Post(BaseModel):
    id: int
    subject: str
    content: str
    create_date: datetime.datetime
    comments: list[Comment] = []

    class Config:
        orm_mode = True


class PostCreate(BaseModel):
    subject: str
    content: str

    @validator("subject", "content")
    def not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError("빈 값은 허용되지 않습니다.")
        return v