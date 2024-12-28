#!/usr/bin/python3
"""Amenity Module for HBNB project."""

from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship


class Amenity(BaseModel, Base):
    """Class representing an Amenity."""

    __tablename__ = 'amenities'

    # Class attributes
    name = Column(String(128), nullable=False)
    
    # Many-to-Many relationship with Place through the place_amenity table
    place_amenities = relationship("Place", secondary="place_amenity", back_populates="amenities")

