import pathlib

from starlette import status
from starlette.requests import Request
from starlette.responses import JSONResponse

from src.routers.sensordata import router as equipments_router

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError

load_dotenv(dotenv_path=pathlib.Path(__file__).parent.resolve())


origins = ["*"]


def create_app():
    app = FastAPI()

    # Adicionando middleware CORS para demonstração
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,  # Liberando acesso de qualquer origem para demonstração
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    routers = [
        equipments_router,
        # Novas rotas podem adicionadas conforme demanda
    ]

    for router in routers:
        app.include_router(router)

    return app


app = create_app()


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    message = exc.errors()[0].get("msg")
    message = message.replace("Input", exc.errors()[0].get("loc")[1].capitalize())
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, content={"detail": message}
    )
