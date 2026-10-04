import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from config import (
    CORS_ORIGINS,
    LOCALHOST_ORIGIN_REGEX,
    TILES_DIR,
)
from routers import characteristics, population, vector_tiles


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("census_api")


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_origin_regex=LOCALHOST_ORIGIN_REGEX,
    allow_methods=["GET"],
    allow_headers=["*"],
)


if TILES_DIR.is_dir():
    app.mount(
        "/tiles_output",
        StaticFiles(directory=TILES_DIR),
        name="tiles_output",
    )
else:
    logger.warning(
        "Tiles directory not found, not mounting: %s",
        TILES_DIR,
    )


app.include_router(characteristics.router, prefix="/api")
app.include_router(population.router, prefix="/api")
app.include_router(vector_tiles.router, prefix="/api")