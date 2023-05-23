import logging

import uvicorn
from fastapi import FastAPI
from fastapi_sqlalchemy import DBSessionMiddleware
from starlette.middleware.cors import CORSMiddleware

from config import Config
import db


def init_app(settings=Config) -> FastAPI:
    """
    Initialize and configure FastAPI app.
    """

    app = FastAPI(
        title="FastAPI Starting Structure",
        description="",
        version="1.0.0",
    )

    app.add_middleware(DBSessionMiddleware, db_url=settings.DATABASE_URL)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=Config.CORS_ORIGIN_WHITELIST,
        allow_credentials=Config.CORS_ALLOW_CREDENTIALS,
        allow_methods=Config.CORS_ALLOW_METHODS,
        allow_headers=Config.CORS_ALLOW_HEADERS,
    )

    # Startup events
    @app.on_event("startup")
    async def startup():
        logger = logging.getLogger("uvicorn.access")
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
        logger.addHandler(handler)

    # Include routers / configure routers

    # from api.views.affiliates import router as affiliate_router
    # app.include_router(affiliate_router)

    # testing by passing welcome message
    @app.get('/')
    async def welcome():
        return {"message": "Welcome to FastAPI starting."}

    return app


app = init_app(settings=Config)

log_config = uvicorn.config.LOGGING_CONFIG
log_config["formatters"]["access"]["fmt"] = "%(asctime)s - %(levelname)s - %(message)s"


if __name__ == "__main__":
    uvicorn.run(
        "app:app",
        port=int(Config.APP_PORT),
        host=Config.APP_HOST,
        log_config=log_config,
        reload=True
    )
