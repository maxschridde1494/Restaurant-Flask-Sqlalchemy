import os
import sys

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy import create_engine
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
engine = create_engine('sqlite:///restaurantapplication.db')
Base.metadata.create_all(engine) #instantiates all Table objects as tables in database - engine is 
								 #the connection to the database


class User(Base):
	__tablename__='users' 

	id = Column(Integer, primary_key=True)
	name = Column(String(50), nullable=False)
	fullname = Column(String(50))
	password = Column(String(12))

	def __repr__(self):
		return "<User(name='%s', fullname='%s', password='%s' )>" % (self.name, self.fullname, self.password)

	def serialize(self):
		return {
			"name": self.name,
			"fullname": self.fullname,
			"password": self.password
		}

class Restaurant(Base):
	__tablename__ = 'restaurant'

	id = Column(Integer, primary_key=True)
	name = Column(String(50), nullable=False)

	def serialize(self):
		return {
			'name': self.name,
			'id': self.id
		}

class MenuItem(Base):
	__tablename__ = 'menu_item'

	id = Column(Integer, primary_key = True)
	name = Column(String(80), nullable = False)
	course = Column(String(250))
	description = Column(String(250))
	price = Column(String(8))
	restaurant_id = Column(Integer, ForeignKey('restaurant.id'))
	restaurant = relationship(Restaurant)

	def serialize(self):
		return {
			'name': self.name,
			'id': self.id,
			'course': self.course,
			'description': self.description,
			'price': self.price,
			'restaurant_id': self.restaurant_id
		}

