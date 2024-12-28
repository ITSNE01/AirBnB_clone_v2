#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
import models
from sqlalchemy.orm import relationship
from sqlalchemy import Column, String
from models.city import City
import os


class State(BaseModel, Base):
    """ State class """
    __tablename__ = 'states'
    if os.getenv('HBNB_TYPE_STORAGE') == "db":
        name = Column(String(128), nullable=False)
        cities = relationship('City', backref='state', cascade='delete')
    else:
        name = ""

    if os.getenv('HBNB_TYPE_STORAGE') != 'db':
        @property
        def cities(self):
            city_list = []
            all_cities = models.storage.all(City).values()
            for city in all_cities:
                if city.state_id == self.id:
                    city_list.append(city)
            return city_list
