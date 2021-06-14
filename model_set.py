from pydantic import BaseModel

class ImageSet(BaseModel):
    id: bool
    age: bool
    img: str

