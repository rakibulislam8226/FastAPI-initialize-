import ast
import logging
import os

from dotenv import load_dotenv


load_dotenv()

# NOTE: see additional setup of logging for `uvicorn`.
logging.basicConfig(level=logging.DEBUG,
                    format="%(levelname)s:%(filename)s:%(lineno)04d:%(funcName)s:%(message)s")

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class Config:
    """
    Configuration for apps.
    """

    ENV = os.getenv("ENV", "prod")
    DEBUG = ast.literal_eval(os.getenv("DEBUG", "False"))
    # SECRET_KEY = os.getenv("SECRET_KEY")

    APP_HOST = os.getenv("APP_HOST", "0.0.0.0")
    APP_PORT = int(os.getenv("PORT", "8000"))

    API_ROUTER_PREFIX = "/api"

    # Database
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_PORT = int(os.getenv("DB_PORT", "5432"))
    DB_DATABASE = os.getenv("DB_NAME", "fastapi")
    DB_USER = os.getenv("DB_USER", "postgres")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "postgres")

    DB_DIALECT_DRIVER = "postgresql+asyncpg"
    DATABASE_URL = f"{DB_DIALECT_DRIVER}://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_DATABASE}"

    ECHO_SQL = ast.literal_eval(os.getenv("ECHO_SQL", "True"))
    POOL_RECYCLE_SEC = 3600 * 5  # 5 min

    # CORS middleware configs
    CORS_ALLOW_CREDENTIALS = True
    CORS_ORIGIN_WHITELIST = (
        "http://localhost",
        "http://localhost:8000",
        "http://localhost:8001",
    )
    CORS_ALLOW_METHODS = ["*"]
    CORS_ALLOW_HEADERS = ["*"]
