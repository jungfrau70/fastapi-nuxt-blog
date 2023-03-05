from fastapi import Depends, FastAPI, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from app.auth import main as auths
from app.users import main as users
from app.blogs import main as blogs, sub as blogs_sub

from app.routers import discussion_topic, incident_handling, issue_mgmt, problem_mgmt, change_mgmt, request_mgmt, asset_mgmt_database, asset_mgmt_kubernetes, asset_mgmt_instance, asset_mgmt_license, capacity_mgmt, backup_mgmt, preventive, vulnerability
# from app.routers import user, auth, blog
from app.cruds import models
from app.db.session import engine
# from app.settings.configs import database
# import os

# from fastapi import FastAPI, Request
# from fastapi.responses import PlainTextResponse
# from starlette.exceptions import HTTPException as StarletteHTTPException
# from fastapi.middleware.cors import CORSMiddleware
# from fastapi.staticfiles import StaticFiles
# from dotenv import load_dotenv

app = FastAPI()

models.Base.metadata.create_all(engine)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auths.app)
app.include_router(users.app)
app.include_router(blogs.app)
app.include_router(blogs_sub.app)

app.include_router(discussion_topic.router)
app.include_router(incident_handling.router)
app.include_router(issue_mgmt.router)
app.include_router(problem_mgmt.router)
app.include_router(change_mgmt.router)
app.include_router(request_mgmt.router)
app.include_router(asset_mgmt_database.router)
app.include_router(asset_mgmt_kubernetes.router)
app.include_router(asset_mgmt_instance.router)
app.include_router(capacity_mgmt.router)
app.include_router(backup_mgmt.router)
app.include_router(vulnerability.router)
app.include_router(preventive.router)
app.include_router(asset_mgmt_license.router)
# app.include_router(report.router)
