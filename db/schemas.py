from pydantic import BaseModel
from typing import Optional, List, Union


class TagBase(BaseModel):
    tag: str

class TagCreate(TagBase):
    pass

class TagResponse(TagBase):
    id: int

    model_config = {"from_attributes": True}

class RestaurantCreate(BaseModel):
    Name: str
    Maps: str
    Category: str
    City: str

class RestaurantResponse(BaseModel):
    id: int
    Name: str
    Maps: str
    Category: str
    City: str

    # Enable model validation from ORM attributes
    model_config = {"from_attributes": True}

class StandardResponse(BaseModel):
    respCode: int = 0
    message: str = "ok"
    data: Optional[Union[RestaurantResponse, List[RestaurantResponse], str, int, None, dict, List[str]]] = None
