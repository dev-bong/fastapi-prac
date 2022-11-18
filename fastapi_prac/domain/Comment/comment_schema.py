import datetime

from pydantic import BaseModel, validator


class CommentCreate(BaseModel):
    content: str

    @validator("content")
    def not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError("빈 값은 허용되지 않습니다.")
        return v


class Comment(BaseModel):
    id: int
    content: str
    create_date: datetime.datetime

    class Config:
        orm_mode = True
