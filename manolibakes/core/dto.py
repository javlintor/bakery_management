from pydantic import BaseModel, Field


class OrderDTO(BaseModel):
    id: int = Field(description='Bread id')
    name: str = Field(description='Bread name')
    number: int = Field(description='Number of breads')
