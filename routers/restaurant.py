from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.database import SessionLocal
from db import models, schemas
from utils.random_picker import pick_random

router = APIRouter(prefix="/restaurants", tags=["Restaurants"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=schemas.StandardResponse)
def add_restaurant(restaurant: schemas.RestaurantCreate, db: Session = Depends(get_db)):
    new_restaurant = models.Restaurant(
        **restaurant.model_dump(),
        pending=0  # Default to inactive
    )
    db.add(new_restaurant)
    db.commit()
    db.refresh(new_restaurant)
    restaurant_response = schemas.RestaurantResponse.model_validate(new_restaurant)
    return schemas.StandardResponse(data=restaurant_response)

@router.get("/random", response_model=schemas.StandardResponse)
def pick_restaurant(category: str = None, city: str = None, db: Session = Depends(get_db)):
    try:
        restaurant = pick_random(db, category, city)
        return schemas.StandardResponse(data=restaurant)
    except HTTPException as e:
        return schemas.StandardResponse(respCode=e.status_code, message=e.detail)


@router.get("/all", response_model=schemas.StandardResponse)
def list_restaurants(db: Session = Depends(get_db)):
    restaurants = db.query(models.Restaurant).filter(models.Restaurant.pending == 1).all()
    restaurant_responses = [schemas.RestaurantResponse.model_validate(r) for r in restaurants]
    return schemas.StandardResponse(data=restaurant_responses)

@router.get("/inactive", response_model=schemas.StandardResponse)
def list_inactive_restaurants(db: Session = Depends(get_db)):
    restaurants = db.query(models.Restaurant).filter(models.Restaurant.pending == 0).all()
    restaurant_responses = [schemas.RestaurantResponse.model_validate(r) for r in restaurants]
    return schemas.StandardResponse(data=restaurant_responses)

@router.get("/all-status", response_model=schemas.StandardResponse)
def list_all_restaurants(db: Session = Depends(get_db)):
    restaurants = db.query(models.Restaurant).all()
    restaurant_responses = [schemas.RestaurantResponse.model_validate(r) for r in restaurants]
    return schemas.StandardResponse(data=restaurant_responses)

@router.get("/categories", response_model=schemas.StandardResponse)
def list_categories(db: Session = Depends(get_db)):
    # Query distinct categories and flatten the results
    categories = db.query(models.Restaurant.Category.distinct()).all()
    categories_list = [category[0] for category in categories]
    print(categories_list)
    return schemas.StandardResponse(data=categories_list)


@router.get("/{restaurant_id}/tags", response_model=schemas.StandardResponse)
def get_restaurant_tags(restaurant_id: int, db: Session = Depends(get_db)):
    restaurant = db.query(models.Restaurant).filter(models.Restaurant.id == restaurant_id).first()
    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")

    tags = [schemas.TagResponse.model_validate(tag) for tag in restaurant.tags]
    return schemas.StandardResponse(data=tags)


@router.put("/{restaurant_id}/status", response_model=schemas.StandardResponse)
def switch_status(restaurant_id: int, db: Session = Depends(get_db)):
    restaurant = db.query(models.Restaurant).filter(models.Restaurant.id == restaurant_id).first()
    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")

    # Toggle status
    restaurant.pending = 1 if restaurant.pending == 0 else 0
    db.commit()
    db.refresh(restaurant)
    return schemas.StandardResponse(data={"id": restaurant.id, "pending": restaurant.pending})
