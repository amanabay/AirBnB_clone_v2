#!/usr/bin/python3
"""Class to manage db storage for hbnb clone"""
from os import getenv
from sqlalchemy import (create_engine)
from sqlalchemy.orm import sessionmaker, scoped_session
from models.base_model import Base
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


class DBStorage:
    """SQL database storage"""
    __engine = None
    __session = None

    def __init__(self):
        """Create engine and connect to database"""
        user = getenv("HBNB_MYSQL_USER")
        pwd = getenv("HBNB_MYSQL_PWD")
        host = getenv("HBNB_MYSQL_HOST")
        db = getenv("HBNB_MYSQL_DB")

        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.format(
            user, pwd, host, db), pool_pre_ping=True)

        if getenv("HBNB_ENV") == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):

        dictionary = {}

        if cls:
            if type(cls) is str:
                cls = eval(cls)
            result = self.__session.query(cls)

            dictionary = {"{}.{}".format(type(row).__name__,
                                         row.id): row for row in result}
        else:
            class_list = [State, City, User, Place, Review, Amenity]

            for c in class_list:
                result = self.__session.query(c)

                dictionary = {"{}.{}".format(type(row).__name__,
                                             row.id): row for row in result}
        return dictionary

    def new(self, obj):
        """Add object to the current database session"""
        self.__session.add(obj)

    def save(self):
        """Commit all changes of the current database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """Delete from the current database session obj if not None"""
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """Create current database session from the engine
        using a sessionmaker"""
        self.__session = Base.metadata.create_all(self.__engine)
        factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(factory)
        self.__session = Session()

    def close(self):
        """Close session"""
        self.__session.close()
