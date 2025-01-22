#!/usr/bin/python3
""" Place Module for HBNB project """

from models.base_model import BaseModel, Base
from sqlalchemy import Column, Integer, Float, String, ForeignKey, Table
from sqlalchemy.orm import relationship
import os

# Create a Many-to-Many relationship table for 'Place' and 'Amenity'
place_amenity = Table(
    'place_amenity', Base.metadata,
    Column('place_id', String(60), ForeignKey('places.id'), primary_key=True, nullable=False),
    Column('amenity_id', String(60), ForeignKey('amenities.id'), primary_key=True, nullable=False)
)


class Place(BaseModel, Base):
    """A place to stay"""

    __tablename__ = 'places'

    # Database columns
    city_id = Column(String(60), ForeignKey('cities.id'), nullable=False)
    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    name = Column(String(128), nullable=False)
    description = Column(String(1024))
    number_rooms = Column(Integer, default=0, nullable=False)
    number_bathrooms = Column(Integer, default=0, nullable=False)
    max_guest = Column(Integer, default=0, nullable=False)
    price_by_night = Column(Integer, default=0, nullable=False)
    latitude = Column(Float)
    longitude = Column(Float)

    # Many-to-Many relationship with 'Amenity' through the 'place_amenity' table
    amenities = relationship("Amenity", secondary=place_amenity, back_populates="place_amenities", viewonly=False)

    # Relationship with Review model
    reviews = relationship('Review', backref='place', cascade='delete')

    @property
    def amenity_ids(self):
        """Returns a list of Amenity IDs associated with this place."""
        return [amenity.id for amenity in self.amenities]

    @amenity_ids.setter
    def amenity_ids(self, amenity_obj):
        """Handles appending Amenity objects to the amenities list."""
        if isinstance(amenity_obj, Amenity):
            self.amenities.append(amenity_obj)

