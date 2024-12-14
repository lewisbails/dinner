from pydantic import BaseModel

class CatalogueItem(BaseModel):
    name: str
    advertised_price: int

class Dinner(BaseModel):
    name: str
    catalogue_ingredients: list[CatalogueItem]
    extra_ingredients: list[str]

class Dinners(BaseModel):
    ideas: list[Dinner]