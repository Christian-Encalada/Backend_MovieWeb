from pydantic import BaseModel

class TagBase(BaseModel):
    movie_id: int
    tag: str

class TagCreate(TagBase):
    pass

class Tag(TagBase):
    tag_id: int

    class Config:
        from_attributes = True