from typing import List
from fastapi import Depends, APIRouter, HTTPException
from sqlalchemy.orm import Session
from . import models, schemas, crud
from settings.database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = APIRouter()


@app.get("/category/", response_model=List[schemas.Category], tags=['post_property'])
def read_categories(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    query = crud.get_category_query(db, skip=skip, limit=limit)
    if len(query) == 0:
        raise HTTPException(status_code=400, detail="Category does not exist")
    return query


@app.post("/category/", response_model=schemas.Category, tags=['post_property'])
def create_category(category: schemas.CreateCategory, db: Session = Depends(get_db)):
    instance = crud.get_category(db, category.name)
    if instance:
        raise HTTPException(status_code=400, detail="Category already registered")
    return crud.create_category(db, category)


@app.get("/series/", response_model=List[schemas.Series], tags=['post_property'])
def read_series(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    query = crud.get_series_query(db, skip=skip, limit=limit)
    if len(query) == 0:
        raise HTTPException(status_code=400, detail="Series does not exist")
    return query


@app.post("/series/", response_model=schemas.Series, tags=['post_property'])
def create_series(series: schemas.CreateSeries, db: Session = Depends(get_db)):
    instance = crud.get_series(db, series.name)
    if instance:
        raise HTTPException(status_code=400, detail="Series already registered")
    return crud.create_series(db, series)


@app.get("/tag/", response_model=List[schemas.Tag], tags=['post_property'])
def read_tag(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    query = crud.get_tag_query(db, skip=skip, limit=limit)
    if len(query) == 0:
        raise HTTPException(status_code=400, detail="Tag does not exist")
    return query


@app.post("/tag/", response_model=schemas.Tag, tags=['post_property'])
def create_tag(tag: schemas.CreateTag, db: Session = Depends(get_db)):
    instance = crud.get_tag(db, tag.name)
    if instance:
        raise HTTPException(status_code=400, detail="Tag already registered")
    return crud.create_tag(db, tag)
