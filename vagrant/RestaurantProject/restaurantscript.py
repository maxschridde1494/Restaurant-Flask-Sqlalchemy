from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem, User
from sqlalchemy.orm import sessionmaker
engine = create_engine('sqlite:///restaurantapplication.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()