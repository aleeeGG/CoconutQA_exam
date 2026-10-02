from sqlalchemy import Column, String, Boolean, DateTime, Integer, Float, ForeignKey
from sqlalchemy.orm import declarative_base
from typing import Dict, Any

Base = declarative_base()

class GenreDBModel(Base):
    __tablename__ = 'genres'

    id = Column(Integer, primary_key=True)
    name = Column(String)

    def to_dict(self) -> Dict[str, Any]:
        return {
            'id': self.id,
            'name': self.name
        }

    def __repr__(self):
        return f"<Genre(id='{self.id}', name='{self.name}')>"