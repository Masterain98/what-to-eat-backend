from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from db.database import Base

class Restaurant(Base):
    __tablename__ = "restaurant"

    id = Column(Integer, primary_key=True, index=True)
    Name = Column(String, nullable=False)
    Maps = Column(String, nullable=False)
    Category = Column(String, nullable=False)
    City = Column(String, nullable=False)
    pending = Column(Integer, default=0)

    # Define relationship with tags
    tags = relationship("Tag", secondary="restaurant_tag", back_populates="restaurants")


class Tag(Base):
    __tablename__ = "tag"

    id = Column(Integer, primary_key=True, index=True)
    tag = Column(String, nullable=False)

    # Define relationship with restaurants
    restaurants = relationship("Restaurant", secondary="restaurant_tag", back_populates="tags")


class RestaurantTag(Base):
    __tablename__ = "restaurant_tag"

    restaurant = Column(Integer, ForeignKey("restaurant.id"), primary_key=True)
    tag = Column(Integer, ForeignKey("tag.id"), primary_key=True)
