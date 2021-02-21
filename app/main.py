import logging

import uvicorn
from fastapi import FastAPI

from app.api import router
# from app.db import models
# from app.db.database import engine
from app.logger.costum_logging import CustomizeLogger

# from sqlalchemy.schema import CreateSchema

logger = logging.getLogger(__name__)


def create_app() -> FastAPI:
    app = FastAPI(title='Two phase transactions', debug=False)
    logger = CustomizeLogger.make_logger()
    app.logger = logger
    app.include_router(router)
    return app


app = create_app()


# @app.on_event("startup")
# async def startup_event():
#     schemas = ['db1', 'db2', 'db3']
#     for schema in schemas:
#         if not engine.dialect.has_schema(engine, schema):
#             engine.execute(CreateSchema(schema))
#     models.Base.metadata.create_all(bind=engine)
#     logger.info("STARTED")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
