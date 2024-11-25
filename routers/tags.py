from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.database import SessionLocal
from db import models, schemas

router = APIRouter(prefix="/tags", tags=["Tags"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=schemas.StandardResponse)
def create_tag(tag: schemas.TagCreate, db: Session = Depends(get_db)):
    new_tag = models.Tag(tag=tag.tag)
    db.add(new_tag)
    db.commit()
    db.refresh(new_tag)
    tag_response = schemas.TagResponse.model_validate(new_tag)
    return schemas.StandardResponse(data=tag_response)


@router.get("/", response_model=schemas.StandardResponse)
def list_tags(db: Session = Depends(get_db)):
    tags = db.query(models.Tag).all()
    tag_responses = [schemas.TagResponse.model_validate(t) for t in tags]
    return schemas.StandardResponse(data=tag_responses)
