from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field, field_validator

from constants.location import Location
from constants.roles import Roles


class User(BaseModel):
    email: str
    fullName: str = Field(min_length=1 )
    password: str = Field(min_length=8, max_length=20)
    passwordRepeat: str = Field(min_length=8, max_length=20)
    roles: list[Roles]
    verified: Optional[bool] = None
    banned: Optional[bool] = None

    @field_validator("passwordRepeat")
    def check_passwordRepeat(cls, value, info):
        if value != info.data["password"]:
            raise ValueError('Пароли не совпадают')
        return value


class Genre(BaseModel):
    name: str = Field(min_length=1)


class Movie(BaseModel):
    id: int
    name: str = Field(min_length=1)
    genre: Genre
    description: str = Field(min_length=1)
    genreId: int
    imageUrl: Optional[str] = None
    price: int = Field(ge=1)
    rating: float = Field(..., ge=0, le=5)
    location: Location
    published: bool
    createdAt: datetime


class MoviesPage(BaseModel):
    movies: list[Movie]
    count: int = Field(ge=1)
    page: int = Field(ge=1)
    pageSize: int = Field(ge=1)
    pageCount: int = Field(ge=1)


class MovieCreateModel(BaseModel):
    name: str = Field(min_length=1)
    imageUrl: str
    price: int = Field(ge=1)
    description: str = Field(min_length=1)
    location: Location
    published: bool
    genreId: int

class MoviePatchModel(BaseModel):
    name: Optional[str] = Field(None, min_length=1)
    description: Optional[str] = Field(None, min_length=1)
    price: Optional[int] = Field(None, ge=1)
    location: Optional[Location] = None
    imageUrl: Optional[str] = None
    published: Optional[bool] = None