import boto3
import os
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from app.users.models import User
import socket
from dotenv import load_dotenv

load_dotenv(dotenv_path="app/settings/.env")

TITLE = "Lenz Backend"
VERSION = "0.0.1"
DESCRIPTION = """
this is Lenz Project
this is not for production
"""
NAME = "Ian Jung"
EMAIL = "inhwan.jung@gmail.com"

POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_SERVER = os.getenv(
    "POSTGRES_SERVER", socket.gethostbyname(socket.gethostname()))
POSTGRES_PORT = os.getenv("POSTGRES_PORT", 5432)
POSTGRES_DATABASE = os.getenv("POSTGRES_DATABASE", "mydb")

DATABASE_URL = f"postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DATABASE}"
# require hashed_password columns
USER_MODEL = User

SECRET_KEY: str = os.getenv("SECRET_KEY")
JWT_ALGORITHM: str = os.getenv("ALGORITHM")
JWT_EXPIRRE_KEY = os.getenv("JWT_EXPIRREKEY", "exp")
JWT_ACCESS_TOKEN_EXPIRE_MINUTES = int(
    os.getenv('JWT_ACCESS_TOKEN_EXPIRE_MINUTES', 30))
PWD_CONTEXT = CryptContext(schemes=["bcrypt"], deprecated="auto")
OAUTH2_SCHEME = OAuth2PasswordBearer(tokenUrl="/auth/token")

AWS_ACCESS_KEY_ID = os.getenv('aws_access_key', '')
AWS_SECRET_ACCESS_KEY = os.getenv('aws_secret_access_key', '')
AWS_BUCKET_NAME = os.getenv('bucket_name', '')
S3_URL = os.getenv('s3_URL', '')

aws_session = boto3.Session(
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
)

HOSTNAME = os.getenv('HOSTNAME', 'http://0.0.0.0/')
SENDGRID_API_KEY = os.environ.get('SENDGRID_API_KEY', '')
FROM_EMAIL = os.getenv("NOTIFICATION_EMAIL_ADDRESS", "")
POST_NOFICATION_TEMPLATE = 'app/notifications/templates/post_notification.json'
