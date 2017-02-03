import os
import sys

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

from sqlalchemy.orm import sessionmaker


Base = declarative_base() #tells sqlalchemy that classes correspond to table in DB

class Restaurant(Base):
	__tablename__ = 'restaurant' #signifies variable used to represent table
	
	name = Column(String(80), nullable = False) #equivalent to NOT NULL in SQL
	id = Column(Integer, primary_key = True)

	@property
	def serialize(self):
		#Returns object data in easily serializeable format
		return {
			'name': self.name,
			'id': self.id
		}

class MenuItem(Base):
	__tablename__ = 'menu_item'
	
	name = Column(String(80), nullable = False)
	id = Column(Integer, primary_key = True)
	course = Column(String(250))
	description = Column(String(250))
	price = Column(String(8))
	restaurant_id = Column(Integer, ForeignKey('restaurant.id'))
	restaurant = relationship(Restaurant)

	@property
	def serialize(self):
		#Returns object data in easily serializeable format
		return {
			'name': self.name,
			'description': self.description,
			'id': self.id,
			'price': self.price,
			'course': self.course
		}

def deleteTableData(table):
	engine = create_engine('sqlite:///restaurantmenu.db')
	Base.metadata.bind = engine
	DBSession = sessionmaker(bind=engine)
	session = DBSession()
	data = session.query(table).all()
	for instance in data:
		session.delete(instance)
	session.commit()

####End of File####
engine = create_engine('sqlite:///restaurantmenu.db') #instantiate create_engine object
Base.metadata.create_all(engine) #adds classes as new tables in DB