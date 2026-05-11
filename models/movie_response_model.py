from pydantic import BaseModel
from typing import Optional
from typing import List

class GenreModel(BaseModel):
    name: str


class MovieResponseModel(BaseModel):
    id: int
    name: str
    price: int
    description: str
    imageUrl: Optional[str]
    location: str
    published: bool
    rating: float
    genreId: int
    genre: GenreModel

class MoviesListResponseModel(BaseModel):
    movies: List[MovieResponseModel]
    count: int
    page: int
    pageSize: int
    pageCount: int