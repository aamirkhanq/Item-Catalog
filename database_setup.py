import sys, datetime

from sqlalchemy import Column, ForeignKey, Integer, String, DateTime

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import relationship

from sqlalchemy import create_engine

Base = declarative_base()

class Category(Base):
    __tablename__ = 'categories'
    name = Column(String(80), nullable = False)
    id = Column(Integer, primary_key = True)

class Item(Base):
    __tablename__ = 'items'
    name = Column(String(80), nullable = False)
    id = Column(Integer, primary_key = True)
    description = Column(String(250))
    category_id = Column(Integer, ForeignKey('categories.id'))
    categories = relationship(Category)
    #created_date = Column(DateTime, default = datetime.datetime.utcnow)

    @property
    def serialize(self):
        #Returns object data in easily serializable format
        return {
            'id' : self.id,
            'name' : self.name,
            'description' : self.description,
            }
engine = create_engine('sqlite:///itemcatalog.db')
Base.metadata.create_all(engine)

