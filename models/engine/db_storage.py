#!/usr/bin/python3
"""
Script that creates a new engine linked to the MySQL database.
"""
from models.base_model import Base
from sqlalchemy import create_engine
from os import getenv
from sqlalchemy.orm import sessionmaker, scoped_session
from models.state import State
from models.city import City
from models.place import Place
from models.user import User
from models.amenity import Amenity
from models.review import Review


class DBStorage:
    __engine = None
    __session = None

    def __init__(self):
        if getenv("HBNB_ENV") == 'test':
            Base.metadata.drop_all(self.__engine)

        self.__engine = create_engine(
            f'mysql+mysqldb://{getenv("HBNB_MYSQL_USER")}:'
            f'{getenv("HBNB_MYSQL_PWD")}@'
            f'{getenv("HBNB_MYSQL_HOST")}/{getenv("HBNB_MYSQL_DB")}',
            pool_pre_ping=True
        )

    def all(self, cls=None):
        """
        Returns a dictionary of models currently in storage.
        Args:
            cls (type, optional): A class type to filter the results.
        Returns:
            dict: A dictionary of models, optionally filtered by specified cls.
        """
        objects = {}
        all_classes = (User, State, City, Amenity, Place, Review)

        if cls is None:
            for class_type in all_classes:
                query = self.__session.query(class_type)
                for obj in query.all():
                    obj_key = '{}.{}'.format(obj.__class__.__name__, obj.id)
                    objects[obj_key] = obj
        else:
            query = self.__session.query(cls)
            for obj in query.all():
                obj_key = f'{obj.__class__.__name__}.{obj.id}'
                objects[obj_key] = obj
        return objects

    def new(self, obj):
        """
        Add the object to the current database session.
        """
        self.__session.add(obj)

    def save(self):
        """
        Commit all changes of the current database session.
        """
        self.__session.commit()

    def delete(self, obj=None):
        """
        Delete from the current database session.
        """
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """Loads storage database"""
        Base.metadata.create_all(self.__engine)
        SessionFactory = sessionmaker(
            bind=self.__engine,
            expire_on_commit=False
        )
        self.__session = scoped_session(SessionFactory)()

    def close(self):
        """Closes the storage engine."""
        self.__session.close()
