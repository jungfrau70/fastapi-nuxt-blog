from app.db import session
from typing import List, Union
from fastapi import APIRouter, Depends, status, HTTPException, Request, Form, UploadFile, File
from fastapi.responses import HTMLResponse, RedirectResponse
from pandas_ods_reader import read_ods

# from config import database
from app.auth.authentications import get_current_active_user
from app.routers import schemas
from app.cruds import problem_mgmt
# from utils import oauth2
from sqlalchemy.orm import Session
# from cruds import models
from sqlalchemy.sql import func
# from datetime import datetime

router = APIRouter(
    prefix="/problem",
    tags=['Problem Management']
)


get_db = session.get_db


SchemaShow = schemas.ShowProblem
Schema = schemas.Problem


@router.get('/all', response_model=List[SchemaShow])
# def all(db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
def all(db: Session = Depends(get_db)):
    return problem_mgmt.get_all(db)


@router.get('/{id}', status_code=200, response_model=Schema)
# def show(id:int, db: Session = Depends(get_db),current_user: schemas.User = Depends(oauth2.get_current_user)):
def show(id: int, db: Session = Depends(get_db)):
    return problem_mgmt.show(id, db)


@router.post('/', status_code=status.HTTP_201_CREATED,)
# def create(request: schemas.Blog, db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
def create(request: Schema, db: Session = Depends(get_db), current_user=Depends(get_current_active_user)):
    return problem_mgmt.create(request, db, current_user)


@router.post('/uploadfile', status_code=status.HTTP_201_CREATED,)
async def upload_file(file: Union[UploadFile, None] = None, db: Session = Depends(get_db)):
    if file.filename.lower().endswith(('.csv')):
        return problem_mgmt.upload_csv(file, db)
    else:
        return {"message": "No csv upload file sent"}


@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
# def destroy(id:int, db: Session = Depends(get_db),current_user: schemas.User = Depends(oauth2.get_current_user)):
def destroy(id: int, db: Session = Depends(get_db)):
    return problem_mgmt.destroy(id, db)


@router.put('/{id}', status_code=status.HTTP_202_ACCEPTED)
# def update(id:int, request: schemas.Blog, db: Session = Depends(get_db),current_user: schemas.User = Depends(oauth2.get_current_user)):
def update(id: int, request: Schema, db: Session = Depends(get_db)):
    return problem_mgmt.update(id, request, db)
