import os

from dotenv import load_dotenv

load_dotenv(dotenv_path="dev.env")

# Database Setting
DB_ENGINE = os.environ.get("DB_ENGINE")
DB_HOST = os.environ.get("DB_HOST")
USERNAME = os.environ.get("DB_USERNAME")
PASSWORD = os.environ.get("DB_PASSWORD")
DB_NAME = os.environ.get("DB_NAME")

ADMIN_DEFAULT_PASSWORD = os.environ.get("DEFAULT_PASSWORD")

# Authentication Setting
JWT_SECRET = os.environ.get("JWT_SECRET")
JWT_ALGORITHM = os.environ.get("JWT_ALGORITHM")
JWT_TOKEN_DURATION = os.environ.get("JWT_TOKEN_DURATION")
TENANT_ID = os.environ.get("TENANT_ID")
APP_CLIENT_ID = os.environ.get("APP_CLIENT_ID")
OPENAPI_CLIENT_ID = os.environ.get("OPENAPI_CLIENT_ID")
OPENAPI_CLIENT_SECRET = os.environ.get("OPENAPI_CLIENT_SECRET")
