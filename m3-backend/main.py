import logging

from fastapi import FastAPI, Request

from fastapi.responses import JSONResponse

from api.routes import router

from config import APP_ENV


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


app = FastAPI(

    title="SIH 2026 Inspection Backend",

    description="Backend API for product label inspection and compliance processing.",

    version="1.0.0"

)


@app.get("/")

def home():

    return {

        "message": "Backend is working!"

    }


@app.get("/health")

def health():

    return {

        "status": "ok"

    }


@app.exception_handler(Exception)
async def general_exception_handler(

    request: Request,

    exc: Exception

):

    logger.error(

        "Unhandled exception on %s %s: %s",

        request.method,

        request.url.path,

        exc,

        exc_info=True

    )

    return JSONResponse(

        status_code=500,

        content={

            "detail": "Internal server error"

        }

    )


app.include_router(router)