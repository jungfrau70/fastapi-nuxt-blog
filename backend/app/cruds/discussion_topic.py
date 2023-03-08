from sqlalchemy.orm import Session
from app.cruds import models
from app.routers import schemas
from fastapi import HTTPException, status, File, UploadFile, BackgroundTasks
from io import BytesIO, StringIO

import pandas as pd
import numpy as np
import csv
import codecs

Model = models.Discussion
Schema = schemas.ShowDiscussion


def get_all(db: Session):
    records = db.query(Model).all()
    return records

from datetime import datetime
def create(request: Schema, db: Session, current_user):
    # print(request.__dict__)
    # date_posted = datetime.now()
    # new_record = Model(**request.dict(), creator = current_user, created_at=date_posted)
    # db.add(new_record)
    # db.commit()
    # db.refresh(new_record)
    # return new_record

    # record.create(request.__dict__)
    # create(request.__dict__)
    new_record = Model(
        year=request.year,
        month=request.month,
        region=request.region,
        az=request.az,
        tenant=request.tenant,

        progress=request.progress,
        status=request.status,

        title = request.title,
        description=request.description,

        creator=current_user.id
    )
    db.add(new_record)
    db.commit()
    db.refresh(new_record)
    return new_record

#     user = get_user_from_token(token, db)    
#     record  = db.query(Item).filter(Item.id == id)
#     if not record.first():
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"record with the id {id} does not exists")
#     if record.first().owner_id == user.id:    
#         record.update(request.__dict__)
#         db.commit()
#         return {"message": f"Details for Item ID {id} has been successfully updated"}
#     else:        
#         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
#                         detail="You are not authorized")  

def upload_csv(file, db: Session):
    contents = file.file.read()
    data = BytesIO(contents)
    df = pd.read_csv(data)
    data.close()
    file.file.close()
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]

    df['region'] = df['region'].fillna(np.nan).replace([np.nan], ['NA'])

    df['year'] = df['year'].fillna(np.nan).replace([np.nan], 0)
    df['month'] = df['month'].fillna(np.nan).replace([np.nan], 0)
    df['az'] = df['az'].fillna(np.nan).replace([np.nan], 0)

    df['year'] = df['year'].astype(int)
    df['month'] = df['month'].astype(int)
    df['az'] = df['az'].astype(int)

    try:
        db.query(Model).delete()
        dicts = df.to_dict(orient='records')
        db.bulk_insert_mappings(Model, dicts)
        db.commit()
    except Exception as e:
        print(e)
        print("Sorry, some error has occurred!")

    return f"uploaded {file.filename}"


def destroy(id: int, db: Session):
    record = db.query(Model).filter(Model.id == id)

    if not record.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"record with id {id} not found")

    # record.delete(synchronize_session=False)
    db.query(Model).filter(Model.id == id).delete()
    db.commit()
    return 'done'


def update(id: int, request, db: Session):
    record = db.query(Model).filter(Model.id == id).first()
    if not record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"record with id {id} not found")

    db.query(Model).filter(Model.id == id).update({

        "year": request.year,
        "month": request.month,
        "region": request.region,
        "az": request.az,
        "tenant": request.tenant,

        "progress": request.progress,
        "status": request.status,

        # "title": request.title,
        "discussion_topic": request.discussion_topic,

    })
    db.commit()
    db.refresh(record)
    return 'updated'


def show(id: int, db: Session):
    record = db.query(Model).filter(Model.id == id).first()
    if not record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"record with the id {id} is not available")
    return record
