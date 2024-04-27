from pydantic import BaseModel, Field


class OrderDTO(BaseModel):
    id: int = Field('Bread id')
    name: str = Field('Bread name')
    number: int = Field('Number of breads')
