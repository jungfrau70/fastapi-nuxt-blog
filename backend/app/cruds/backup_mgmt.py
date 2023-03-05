from sqlalchemy.orm import Session
from app.cruds import models
from app.routers import schemas
from fastapi import HTTPException, status
from io import BytesIO

import pandas as pd
import numpy as np

Model = models.Backup
Schema = schemas.ShowBackup


def get_all(db: Session):
    records = db.query(Model).all()
    return records


def create(request: Schema, db: Session, current_user):
    new_record = Model(
        year=request.year,
        month=request.month,
        region=request.region,
        az=request.az,
        tenant=request.tenant,

        progress=request.progress,
        status=request.status,

        db_type=request.db_type,
        instance_name=request.instance_name,
        instance_ip=request.instance_ip,
        freq_full_archive=request.freq_full_archive,
        comment=request.comment,

        creator=current_user.id
    )
    db.add(new_record)
    db.commit()
    db.refresh(new_record)
    return new_record


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

        "db_type": request.db_type,
        "instance_name":  request.instance_name,
        "instance_ip":  request.instance_ip,
        "freq_full_archive":  request.freq_full_archive,
        "comment":  request.comment,

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
