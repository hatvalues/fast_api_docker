from pydantic import BaseModel, Field, EmailStr

class BlogPost(BaseModel):
    id: int = Field(default=None)
    title: str = Field(...)
    content: str = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "title": "My New Blog Post",
                "content": "The content of my new blog post..."
            }
        }