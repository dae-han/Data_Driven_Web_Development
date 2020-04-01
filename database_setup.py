## 1. Configuration (start)
## Used to import all neccesary modules
import os

# 'sys' provides a number of functions and variables that can be used to manipulate different parts of the Python run-time environment
import sys

# This is for mapper code
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine

# 'declarative_base' instance is used to inherit all the features of sqlalchemy
Base = declarative_base()

## 2. Class
## Used to represent our data as Python objects
## Has 'table' and 'mapper' code
class Restaurant(Base):

    ## 3. Table
    ## Represent specific table in our database
    __tablename__ = 'restaurant'

    ## 4. Mapper
    ## Connects the columns of our table to class that represents it
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)

class MenuItem(Base):
    __tablename__ = 'menu_item'


    name =Column(String(80), nullable = False)
    id = Column(Integer, primary_key = True)
    description = Column(String(250))
    price = Column(String(8))
    course = Column(String(250))
    restaurant_id = Column(Integer,ForeignKey('restaurant.id'))
    restaurant = relationship(Restaurant)

#We added this serialize function to be able to send JSON objects in a serializable format
    @property
    def serialize(self):

       return {
           'name'         : self.name,
           'description'         : self.description,
           'id'         : self.id,
           'price'         : self.price,
           'course'         : self.course,
       }

## 1-2. Configuration (end)
# Create (or connects) the database and addes tables and columns
engine = create_engine('sqlite:///restaurantmenu.db')


Base.metadata.create_all(engine)
