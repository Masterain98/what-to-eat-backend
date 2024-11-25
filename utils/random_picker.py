import random
from sqlalchemy.orm import Session
from db.models import Restaurant
from fastapi import HTTPException

def pick_random(db: Session, category=None, city=None):
    query = db.query(Restaurant)
    if category:
        query = query.filter(Restaurant.Category == category)
    if city:
        query = query.filter(Restaurant.City == city)
    restaurants = query.all()
    if not restaurants:
        raise HTTPException(status_code=404, detail="No restaurants found")
    return random.choice(restaurants)
