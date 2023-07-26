#!/usr/bin/python3
""" Place Module for HBNB project """
from models.base_model import BaseModel, Base
import models
from os import getenv
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, Float, String, ForeignKey, Table

place_amenity = Table('place_amenity', Base.metadata,
                      Column('place_id',
                             String(60),
                             ForeignKey('places.id'),
                             nullable=False),
                      Column('amenity_id',
                             String(60, collation='latin1_swedish_ci'),
                             ForeignKey('amenities.id'),
                             nullable=False))


class Place(BaseModel, Base):
    """ A place to stay """
    __tablename__ = 'places'
    city_id = Column(String(60, collation='latin1_swedish_ci'),
                     ForeignKey('cities.id'), nullable=False)
    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    name = Column(String(128), nullable=False)
    description = Column(String(1024))
    number_rooms = Column(Integer, default=0, nullable=False)
    number_bathrooms = Column(Integer, default=0, nullable=False)
    max_guest = Column(Integer, default=0, nullable=False)
    price_by_night = Column(Integer, default=0, nullable=False)
    latitude = Column(Float)
    longitude = Column(Float)
    reviews = relationship('models.review.Review', backref='place',
                           cascade='delete')
    amenities = relationship('models.amenity.Amenity', secondary=place_amenity,
                             viewonly=False)
    amenity_ids = []

    if getenv("HBNB_TYPE_STORAGE") == "db":
        @property
        def reviews(self):
            """ Place reviews """
            rv = models.storage.all(models.review.Review).values()
            return {re for re in rv if re.place_id == self.id}

        @property
        def amenities(self):
            """ Place amenities """
            ob = models.storage.all(models.amenity.Amenity).values()
            return [obj for obj in ob if obj.id in self.amenity_ids]

        @amenities.setter
        def amenities(self, value):
            """ Amenities setter """
            if type(value) is models.amenity.Amenity:
                self.amenity_ids.append(value.id)
