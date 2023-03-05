from sqlalchemy.orm import Session
from app.cruds import models
from app.routers import schemas
from fastapi import HTTPException, status, File, UploadFile, BackgroundTasks
from io import BytesIO, StringIO

import pandas as pd
import numpy as np
import csv
import codecs

Model = models.Kubernetes
Schema = schemas.ShowKubernetes


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

        status=request.status,
        cluster_name=request.cluster_name,
        node_type=request.node_type,
        node_name=request.node_name,
        node_ips=request.node_ips,
        api_vip=request.api_vip,
        flavor=request.flavor,
        network_zone=request.network_zone,
        contacts=request.contacts,
        k8s_version=request.k8s_version,
        monitoring_agent=request.monitoring_agent,

        api_cert_expired_date=request.api_cert_expired_date,
        ca_cert_expired_date=request.ca_cert_expired_date,
        etcd_cert_expired_date=request.etcd_cert_expired_date,

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

    df['api_cert_expired_date'] = df['api_cert_expired_date'].fillna(
        np.nan).replace([np.nan], ['1900-01-01'])
    df['ca_cert_expired_date'] = df['ca_cert_expired_date'].fillna(
        np.nan).replace([np.nan], ['1900-01-01'])
    df['etcd_cert_expired_date'] = df['etcd_cert_expired_date'].fillna(
        np.nan).replace([np.nan], ['1900-01-01'])

    df['api_cert_expired_date'] = pd.to_datetime(df['api_cert_expired_date'])
    df['ca_cert_expired_date'] = pd.to_datetime(df['ca_cert_expired_date'])
    df['etcd_cert_expired_date'] = pd.to_datetime(df['etcd_cert_expired_date'])

    try:
        db.query(Model).delete()
        dicts = df.to_dict(orient='records')
        db.bulk_insert_mappings(Model, dicts)
        db.commit()
    except Exception as e:
        print(e)
        print("Sorry, some error has occurred!")

    return f"uploaded {file.filename}"

# def upload_csv(file, db: Session):
#     contents = file.file.read()
#     data = BytesIO(contents)
#     df = pd.read_csv(file.file, na_filter = False)
#     file.file.close()

#     df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
#     df.info()

#     df['year'] = df['year'].fillna(np.nan).replace([np.nan], 0)
#     df['month'] = df['month'].fillna(np.nan).replace([np.nan], 0)
#     df['az'] = df['az'].fillna(np.nan).replace([np.nan], 0)

#     df['year'] = df['year'].astype(int)
#     df['month'] = df['month'].astype(int)
#     df['az'] = df['az'].astype(int)

#     df['api_cert_expired_date'] = df['api_cert_expired_date'].fillna(np.na).replace([np.nan], ['1900-01-01'])
#     df['ca_cert_expired_date'] = df['ca_cert_expired_date'].fillna(np.nan).replace([np.nan], ['1900-01-01'])
#     df['etcd_cert_expired_date'] = df['etcd_cert_expired_date'].fillna(np.nan).replace([np.nan], ['1900-01-01'])

#     df['api_cert_expired_date'] = pd.to_datetime(df['api_cert_expired_date'])
#     df['ca_cert_expired_date'] = pd.to_datetime(df['ca_cert_expired_date'])
#     df['etcd_cert_expired_date'] = pd.to_datetime(df['etcd_cert_expired_date'])

#     try:
#         db.query(Model).delete()
#         dicts = df.to_dict(orient='records')
#         db.bulk_insert_mappings(Model, dicts)
#         db.commit()
#     except Exception as e:
#         print(e)
#         print("Sorry, some error has occurred!")

#     return "uploaded"


def destroy(id: int, db: Session):
    record = db.query(Model).filter(Model.id == id)

    if not record.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"record with id {id} not found")

    record.delete(synchronize_session=False)
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

        "status": request.status,
        "cluster_name": request.cluster_name,
        "node_type": request.node_type,
        "node_name": request.node_name,
        "node_ips": request.node_ips,
        "api_vip": request.api_vip,
        "flavor": request.flavor,
        "network_zone": request.network_zone,
        "contacts": request.contacts,
        "k8s_version": request.k8s_version,
        "monitoring_agent": request.monitoring_agent,

        "api_cert_expired_date": request.api_cert_expired_date,
        "ca_cert_expired_date": request.ca_cert_expired_date,
        "etcd_cert_expired_date": request.etcd_cert_expired_date,

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
